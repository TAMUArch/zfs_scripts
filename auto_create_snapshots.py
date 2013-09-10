#!/usr/local/bin/python

import commands
import subprocess
import time
import os

timestamp = time.strftime("%Y%m%d-%H%M")

zfs_list = {"pool0": [ "django_media", "git_repo_data", "postgres_data" ]}

for zfs_pool in zfs_list:
    for zfs_filesystem in zfs_list[zfs_pool]:
        print "Snapshoting-> %s/%s" %(zfs_pool, zfs_filesystem)
        snapshot_name = %s/%s@%s" % (zfs_pool, zfs_filesystem, timestamp)
        commands.getoutput("zfs snapshot %s" % (snapshot_name))
