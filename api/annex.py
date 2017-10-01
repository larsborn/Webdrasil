import subprocess


class AnnexException(Exception):
    pass


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
        if err:
            raise AnnexException(err)
        return out

    def get(self, file_name):
        return self._run('get', file_name)

    def drop(self, file_name):
        return self._run('drop', file_name)
