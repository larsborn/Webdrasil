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
        print ' '.join(commands)

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