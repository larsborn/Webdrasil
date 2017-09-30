import datetime
import json
import os
import fcntl


class QueueEntry(object):
    def __init__(self, file_name, progress, should_stay_until):
        self.file_name = file_name
        self.progress = progress
        self.should_stay_until = should_stay_until


class QueueFactory(object):
    def from_handle(self, fp):
        return [self.entry_from_row(row) for row in (json.load(fp))]

    def to_handle(self, queue, fp):
        fp.seek(0)
        fp.truncate()
        json.dump([self.row_from_entry(entry) for entry in queue], fp)

    @staticmethod
    def entry_from_row(row):
        return QueueEntry(row['file_name'], row['progress'], row['should_stay_until'])

    @staticmethod
    def row_from_entry(entry):
        return {'file_name': entry.file_name, 'progress': entry.progress, 'should_stay_until': entry.should_stay_until}


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
        fcntl.flock(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
        queue = self.queue_factory.from_handle(fp)
        queue.append(QueueEntry(
            file_name,
            None,
            (datetime.date.today() + datetime.timedelta(6 * 365 / 12)).isoformat())
        )
        self.queue_factory.to_handle(queue, fp)
        fcntl.flock(fp, fcntl.LOCK_UN)
        fp.close()

    def remove(self, file_name):
        fp = open(self.queue_file, 'r+')
        fcntl.flock(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
        queue = [
            entry
            for entry in self.queue_factory.from_handle(fp)
            if entry.file_name != file_name
        ]
        self.queue_factory.to_handle(queue, fp)
        fcntl.flock(fp, fcntl.LOCK_UN)
        fp.close()

    def get_filtered(self, filter_callback):
        fp = open(self.queue_file, 'r')
        fcntl.flock(fp, fcntl.LOCK_SH)
        queue = self.queue_factory.from_handle(fp)
        fcntl.flock(fp, fcntl.LOCK_UN)
        fp.close()

        return [row for row in queue if filter_callback(row)]

    def is_scheduled(self, file_name):
        return True if self.get_filtered(lambda entry: file_name == entry.file_name) else False
