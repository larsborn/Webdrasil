#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os import listdir
from os.path import isdir, join, sep as path_sep, exists, islink

from flask import Flask, request, jsonify
from lib import WebdrasilDownloader, crossdomain

app = Flask(__name__)
app.config['YGGDRASIL_DIR'] = [u'home', u'annex', u'Yggdrasil']  # TODO move to env
app.config['QUEUE_FILE'] = '/home/webdrasil/queue.json'  # TODO move to env


def base_dir_len():
    return len('/'.join(app.config['YGGDRASIL_DIR'])) + 2


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
        rv['message'] = self.message  # TODO don't output error to client in non-debugging mode
        return rv


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
@crossdomain(origin='http://localhost:3000')
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

    downloader = WebdrasilDownloader(app.config['QUEUE_FILE'])
    downloader.schedule(file_to_download[base_dir_len():])

    return jsonify({})


@app.route("/api/list", methods=['GET'])
@crossdomain(origin='http://localhost:3000')
def list_dir():
    downloader = WebdrasilDownloader(app.config['QUEUE_FILE'])

    base_folder = _sanitize_basedir(request.args.get('dir', ''))
    ret = []
    for filename in listdir(base_folder):
        if filename.startswith('.'):
            continue
        full_filename = join(base_folder, filename)

        # determine file status
        file_status = None
        if islink(full_filename):
            if exists(full_filename):
                file_status = 'EXISTS'
            else:
                file_status = 'IN_PROGRESS' if downloader.is_scheduled(full_filename[base_dir_len():]) else 'MISSING'

        ret.append({
            'filename': filename,
            'is_dir': isdir(full_filename),
            'is_empty': isdir(full_filename) and len(listdir(full_filename)) == 0,
            'is_symlink': islink(full_filename),
            'file_status': file_status,
        })
    resp = jsonify(ret)
    return resp


if __name__ == "__main__":
    # app.run(host='127.0.0.1', port=8080, debug=True)  # use this instead while developing
    app.run(host='127.0.0.1', port=8080)
