import json
import subprocess

from lib.web import InvalidUsage


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
        print '[running] %s' % ' '.join(commands)

        p = subprocess.Popen(commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if err:
            raise InvalidUsage(err, 400)
        return out

    def get_tags(self, filename):
        # TODO use --json and parse result
        tags = []
        for line in self._run('metadata', filename).split('\n'):
            line = line.strip()
            if not line.startswith('tag='):
                continue
            tags.append(line[4:])

        return tags

    def add_tag(self, filename, tag):
        self._run('metadata', '--tag', tag, filename)

    def remove_tag(self, filename, tag):
        self._run('metadata', '--untag', tag, filename)

    def set_metadata(self, filename, field, value):
        self._run('metadata', '-s', '%s=%s' % (field, value), filename)

    def remove_metadata(self, filename, field, value):
        self._run('metadata', '-s', '%s-=%s' % (field, value), filename)

    def get_metadata(self, filename):
        result = self._run('metadata', '--json', filename)
        while ',,' in result:
            result = result.replace(',,', ',')  # git annex returns invalid JSON where fields are missing
        return json.loads(result)

    def find(self, *criteria):
        args = ['find']
        args += criteria
        args.append(self.yggdrasil_root)
        return self._run(*args)

    def drop(self, filename):
        print 'git annex drop not implemented: %s' % filename
