#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import re

sys.path.append(os.path.join(os.path.dirname(__file__)))

from flask import Flask, request, jsonify
from lib import WebdrasilDownloader, crossdomain

app = Flask(__name__)
app.config['BASE_DIR'] = os.environ.get('BASE_DIR', None)
if app.config['BASE_DIR'] is None:
    raise Exception('BASE_DIR is mandatory')
if not os.path.exists(app.config["BASE_DIR"]):
    raise Exception(F'"{app.config["BASE_DIR"]}" does not exist')
if not os.path.isdir(app.config["BASE_DIR"]):
    raise Exception(F'"{app.config["BASE_DIR"]}" is not a directory')
app.config['QUEUE_FILE'] = os.environ.get('QUEUE_FILE_NAME', None)
if app.config['QUEUE_FILE'] is None:
    raise Exception('QUEUE_FILE is mandatory')
queue_dir = os.path.dirname(app.config['QUEUE_FILE'])
if not os.path.exists(queue_dir):
    raise Exception(F'"{queue_dir}" does not exist')
if not os.path.isdir(queue_dir):
    raise Exception(F'"{queue_dir}" is not a directory')


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


def sanitize_basedir(arg):
    current_parts = ['']
    for part in arg.split('/'):
        if not part:
            continue
        if part not in os.listdir(os.path.join(app.config['BASE_DIR'], *current_parts)):
            raise InvalidUsage('Path does not exist', 404)
        current_parts.append(part)
        if os.path.isdir(os.path.join(app.config['BASE_DIR'], *current_parts, part)):
            raise InvalidUsage('Folder does not exist', 404)
    return os.path.join(*current_parts)


@app.route("/api/download", methods=['POST'])
@crossdomain(origin='http://localhost:3000')
def download():
    file_to_download = request.args.get('file', '')
    i = file_to_download.rfind('/')
    if i == -1:
        raise InvalidUsage('Cannot split path', 400)
    local_dir = sanitize_basedir(file_to_download[:i])
    if not local_dir:
        raise InvalidUsage('Unknown error', 400)
    file_to_download = os.path.join(local_dir, file_to_download[i + 1:])

    full_path = os.path.join(app.config['BASE_DIR'], file_to_download)
    if not os.path.exists(full_path):
        raise InvalidUsage('File does not exist', 404)
    if not os.path.islink(full_path):
        raise InvalidUsage('File is not a link', 404)

    downloader = WebdrasilDownloader(app.config['QUEUE_FILE'])
    downloader.schedule(full_path)

    return jsonify({})


@app.route("/api/list", methods=['GET'])
@crossdomain(origin='http://localhost:3000')
def list_dir():
    local_dir = sanitize_basedir(request.args.get('dir', ''))
    base_dir = app.config['BASE_DIR']
    ret = []
    current_dir = os.path.join(base_dir, local_dir)
    for file_name in os.listdir(current_dir):
        if file_name.startswith('.'):
            continue
        local_path = os.path.join(local_dir, file_name)
        full_path = os.path.join(base_dir, current_dir, file_name)

        # determine file status
        file_status = None
        if os.path.islink(full_path):
            if os.path.exists(full_path):
                file_status = 'EXISTS'
            else:
                downloader = WebdrasilDownloader(app.config['QUEUE_FILE'])
                file_status = 'IN_PROGRESS' if downloader.is_scheduled(local_path) else 'MISSING'

        ret.append({
            'filename': file_name,
            'is_dir': os.path.isdir(full_path),
            'is_empty': os.path.isdir(full_path) and len(os.listdir(full_path)) == 0,
            'is_symlink': os.path.islink(full_path),
            'file_status': file_status,
        })
    return jsonify(ret)


if __name__ == "__main__":
    # app.run(host='127.0.0.1', port=8080, debug=True)  # use this instead while developing
    app.run(host='127.0.0.1', port=8080)
