#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import json
import os
from dateutil import parser


class QueueEntry(object):
    def __init__(self, file_name, progress, remove_after):
        self.file_name = file_name
        self.progress = progress if isinstance(progress, float) else int(progress)
        self.remove_after = remove_after \
            if isinstance(remove_after, datetime.date) \
            else parser.parse(remove_after).date()

    def __repr__(self):
        return '<QueueEntry %s progress=%.2f,remove_after=%s>' % (
            self.file_name,
            self.progress,
            self.remove_after
        )


class QueueFactory(object):
    def from_handle(self, fp):
        return [self.entry_from_row(row) for row in (json.load(fp))]

    def to_handle(self, queue, fp):
        fp.seek(0)
        fp.truncate()
        json.dump([self.row_from_entry(entry) for entry in queue], fp)

    @staticmethod
    def entry_from_row(row):
        return QueueEntry(row['file_name'], row['progress'], row['remove_after'])

    @staticmethod
    def row_from_entry(entry):
        return {
            'file_name': entry.file_name,
            'progress': entry.progress,
            'remove_after': entry.remove_after.strftime('%Y-%m-%d')
        }


class WebdrasilException(Exception):
    pass


class WebdrasilDownloader(object):
    def __init__(self, queue_file):
        self.queue_factory = QueueFactory()

        self.queue_file = queue_file

        if not os.path.exists(queue_file):
            self.queue_factory.to_handle([], open(self.queue_file, 'w'))
        if not os.path.isfile(queue_file):
            raise WebdrasilException('Path "%s" passed as queue file is not a file' % queue_file)

    def schedule(self, file_name):
        fp = open(self.queue_file, 'r+')
        self._exclusive_lock(fp)
        queue = self.queue_factory.from_handle(fp)
        queue.append(QueueEntry(
            file_name,
            0,
            (datetime.date.today() + datetime.timedelta(6 * 365 / 12)).isoformat())
        )
        self.queue_factory.to_handle(queue, fp)
        self._release_lock(fp)
        fp.close()

    def remove(self, file_name):
        fp = open(self.queue_file, 'r+')
        self._exclusive_lock(fp)
        queue = [
            entry
            for entry in self.queue_factory.from_handle(fp)
            if entry.file_name != file_name
        ]
        self.queue_factory.to_handle(queue, fp)
        self._release_lock(fp)
        fp.close()

    def get_queue(self):
        fp = open(self.queue_file, 'r')
        self._shared_lock(fp)
        queue = self.queue_factory.from_handle(fp)
        self._release_lock(fp)
        fp.close()

        return queue

    def get_filtered(self, filter_callback):
        return [row for row in self.get_queue() if filter_callback(row)]

    def is_scheduled(self, file_name):
        return True if self.get_filtered(lambda entry: file_name == entry.file_name) else False

    def update_progress(self, file_name, new_progress):
        fp = open(self.queue_file, 'r+')
        self._exclusive_lock(fp)
        queue = self.queue_factory.from_handle(fp)
        for entry in queue:
            if entry.file_name == file_name:
                entry.progress = new_progress
        self.queue_factory.to_handle(queue, fp)
        self._release_lock(fp)
        fp.close()

    @staticmethod
    def _shared_lock(fp):
        import fcntl
        fcntl.flock(fp, fcntl.LOCK_SH)

    @staticmethod
    def _exclusive_lock(fp):
        import fcntl
        fcntl.flock(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)

    @staticmethod
    def _release_lock(fp):
        import fcntl
        fcntl.flock(fp, fcntl.LOCK_UN)


from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)

    return decorator
