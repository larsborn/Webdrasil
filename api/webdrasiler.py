from lib.annex import Annex
from os.path import join, normpath, islink, isfile

FIFO = '/home/annex/webdrasil_tag'

annex = Annex()
with open(FIFO) as fifo:
    while True:
        line = fifo.readline().strip()
        if line:
            path = normpath(join(annex.yggdrasil_root, line))
            if path.startswith(annex.yggdrasil_root) and (islink(path) or isfile(path)):
                annex.set_metadata(path, 'in_webdrasil', '1')
