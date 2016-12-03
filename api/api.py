import json

from flask import Flask, request, Response, jsonify
import os
import subprocess

app = Flask(__name__)
app.config['YGGDRASIL_DIR'] = [u'home', u'annex', u'Yggdrasil']


class Annex(object):
    def __init__(self):
        self.git_executable = '/home/annex/git-annex.linux/git'  # TODO move to env variables
        self.yggdrasil_root = '/home/annex/Yggdrasil'  # TODO move to env variables

    def _run(self, *args):
        commands = [
            self.git_executable,
            '--git-dir=%s/.git' % self.yggdrasil_root,
            '--work-tree=%s' % self.yggdrasil_root,
            'annex'
        ]
        commands += args

        p = subprocess.Popen(commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        return out

    def get_file_tags(self, filename):
        tags = []
        for line in self._run('metadata', filename).split('\n'):
            line = line.strip()
            if not line.startswith('tag='):
                continue
            tags.append(line[4:])

        return tags


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route("/api/list", methods=['GET'])
def list_dir():
    current_folder = app.config['YGGDRASIL_DIR'][:]
    for part in request.args.get('dir', '').split(os.path.sep):
        if not part:
            continue
        if part not in os.listdir(os.path.sep + os.path.join(*current_folder)):
            raise InvalidUsage('Folder does not exist', 404)
        current_folder.append(part)
        if not os.path.isdir(os.path.sep + os.path.join(*current_folder)):
            raise InvalidUsage('Folder does not exist', 404)

    annex = Annex()

    ret = []
    base_folder = os.path.sep + os.path.join(*current_folder)
    for filename in os.listdir(base_folder):
        if filename.startswith('.'): continue

        full_filename = os.path.join(base_folder, filename)
        # determine file status
        file_status = None
        if os.path.islink(full_filename):
            tags = annex.get_file_tags(full_filename)
            if os.path.exists(full_filename):
                file_status = 'EXISTS'
            else:
                if 'webdrasil' in tags:
                    file_status = 'IN_PROGRESS'
                else:
                    file_status = 'MISSING'

        ret.append({
            'filename': filename,
            'is_dir': os.path.isdir(full_filename),
            'is_empty': os.path.isdir(full_filename) and len(os.listdir(full_filename)) == 0,
            'is_symlink': os.path.islink(full_filename),
            'file_status': file_status,
        })
    resp = jsonify(ret)
    resp.headers['Access-Control-Allow-Origin'] = '*'  # TODO remove
    return resp


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)  # TODO remove debug and move host and port to env vars
