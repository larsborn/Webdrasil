#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lib import WebdrasilDownloader
import os
from annex import Annex
from tendo import singleton

# ensure that only one downloader process is running at a time
me = singleton.SingleInstance()

yggdrasil_root = '/home/annex/Yggdrasil'  # TODO move to env
downloader = WebdrasilDownloader('/home/webdrasil/queue.json')  # TODO move to env

# get all tasks that are not completed (this assumes Singleton)
todo = downloader.get_filtered(lambda entry: entry.progress < 1)
if not todo: exit()

# remove tasks that do not have a symlink anymore
full_path = os.path.join(yggdrasil_root, todo[0].file_name)
if not os.path.islink(full_path):
    downloader.remove(todo[0].file_name)
    exit()

# perform download
Annex().get(todo[0].file_name)
downloader.update_progress(todo[0].file_name, 1)
