from os import listdir
from os.path import isdir, join, sep as path_sep, exists, islink

from flask import Flask, request, jsonify

from lib.web import InvalidUsage

from lib.annex import Annex

app = Flask(__name__)
app.config['YGGDRASIL_DIR'] = [u'home', u'annex', u'Yggdrasil']


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def _sanitize_basedir(arg):
    current_folder = app.config['YGGDRASIL_DIR'][:]
    for part in arg.split(path_sep):
        if not part:
            continue
        if part not in listdir(path_sep + join(*current_folder)):
            raise InvalidUsage('Folder does not exist', 404)
        current_folder.append(part)
        if not isdir(path_sep + join(*current_folder)):
            raise InvalidUsage('Folder does not exist', 404)
    return path_sep + join(*current_folder)


@app.route("/api/download", methods=['POST'])
def download():
    file_to_download = request.args.get('file', '')
    i = file_to_download.rfind('/')
    if i == -1:
        raise InvalidUsage('Cannot split path', 400)
    base_dir = _sanitize_basedir(file_to_download[:i])
    if not base_dir:
        raise InvalidUsage('Unknown error', 400)
    file_to_download = join(base_dir, file_to_download[i + 1:])

    if not islink(file_to_download):
        raise InvalidUsage('File does not exist', 404)

    fp = open('/home/annex/webdrasil_tag', 'wb')
    fp.write(file_to_download)
    fp.close()
    return jsonify({})


@app.route("/api/list", methods=['GET'])
def list_dir():
    annex = Annex()

    base_folder = _sanitize_basedir(request.args.get('dir', ''))
    ret = []
    for filename in listdir(base_folder):
        if filename.startswith('.'): continue
        full_filename = join(base_folder, filename)

        # determine file status
        file_status = None
        if islink(full_filename):
            tags = annex.get_tags(full_filename)
            if exists(full_filename):
                file_status = 'EXISTS'
            else:
                if 'webdrasil' in tags:
                    file_status = 'IN_PROGRESS'
                else:
                    file_status = 'MISSING'

        ret.append({
            'filename': filename,
            'is_dir':
                isdir(full_filename),
            'is_empty': isdir(full_filename) and len(listdir(full_filename)) == 0,
            'is_symlink': islink(full_filename),
            'file_status': file_status,
        })
    resp = jsonify(ret)
    resp.headers['Access-Control-Allow-Origin'] = '*'  # comment in, for API debugging from client
    return resp


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)  # use this instead while developing
    # app.run(host='127.0.0.1', port=8080)
