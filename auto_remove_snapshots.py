#!/usr/local/bin/python

import commands
import subprocess
import time
import os
import datetime

TIME_TO_KEEP = 30

now = datetime.datetime.now()

timestamp = time.strftime("%Y%m%d-%H%M")

zpools = ["pool0"]

for zfs_pool in zpools:
    snapshot_list = commands.getoutput("zfs list -H -t snapshot | awk '{print $1}' | grep %s" % zfs_pool)
    for snapshot in snapshot_list.split("\n")
        snapshot_date = datetime.datetime.strptime(snapshot.slit("@")[1], "%Y%m%d-%H-%M")
        if (now - snapshot_date) >= datetime.timedelta(days = TIME_TO_KEEP):
            print "Removing -> %s" % (snapshot)
            commands.getoutput("zfs destroy %s" % (snapshot))
