#!/usr/bin/python
# Help:
# Simple script to handle bulk creation and deletion of zfs snapshots
#
# Creation:
# creates snapshots in the following format rpool0/root@20130910-1130
#     python py_snapshot.py rpool0/root
#
# creates daily snapshots
#     python py_snapshot.py --by-time=daily rpool/root
#
# Deletion:
# This only works for snapshots that were created with this script or snapshots with the correct
# naming convention.
#
# deletes all snapshots older than 90 hours for rpool0/root and tank/important_files:
#     python py_snapshot.py --action destroy --time-to-keep=90 rpool0/root tank/important_files
#
# deletes all daily snapshots older than 7 days
#     python py_snapshot.py --action destroy --time-to-keep=7 --by-time=daily rpool/root
#

import commands
import subprocess
import time
import os
import argparse
import datetime

def create_snapshot(snapshot_name):
    print "Snapshotting -> %s as %s" % (zfs_share, snapshot_name)
    commands.getoutput("zfs snapshot %s" % (snapshot_name))

def destroy_snapshot(snapshot_name):
    print "Removing snapshot -> %s" % (snapshot_name)
    commands.getoutput("zfs destroy %s" % (snapshot_name))

def current_snapshots(zfs_share):
    snaps = commands.getoutput("zfs list -H -t snapshot | awk '{print $1}' | grep %s" % (zfs_share))
    return snaps.split("\n")

def time_stamp(stamp_type):
    if stamp_type == 'hourly':
        time_format = "%Y%m%d-%H%M"
    elif stamp_type == 'daily':
        time_format = "%Y%m%d"
    elif stamp_type == 'weekly':
        time_format = "%Y%m-week%U"
    else:
        print "timestamp not supported"
    return time.strftime(time_format)

def strip_time_stamp(stamp_type, snapshot):
    if stamp_type == 'hourly':
        time_format = "%Y%m%d-%H%M"
    elif stamp_type == 'daily':
        time_format = "%Y%m%d"
    elif stamp_type == 'weekly':
        time_format = "%Y%m-week%U"
    else:
        print "timestamp not supported"
    return datetime.datetime.strptime(snapshot.split("@")[1], time_format)


parser = argparse.ArgumentParser(description='ZFS bulk snapshot tool')
parser.add_argument('--action', type=str, default='create',
                    help='remove or create defaults to %(default)s')
parser.add_argument('--time-to-keep', type=int, default=30,
                    help='delete snapshots after these many days defaults to %(default)s')
parser.add_argument('--by-time', type=str, default='hourly',
                    help='snapshot using hourly, daily, or weekly defaults to %(default)s')
parser.add_argument('zfs_shares', type=str, nargs='+',
                    help='a list of zfs shares eg. pool0/test pool0/test1')
args = parser.parse_args()

for zfs_share in args.zfs_shares:
    if args.action == 'destroy':
        for snapshot in current_snapshots(zfs_share):
            if snapshot == None or snapshot == '':
                continue
            try:
                snapshot_date = strip_time_stamp(args.by_time, snapshot)
            except:
                continue

            if args.by_time == 'hourly':
                ttk = datetime.timedelta(hours = args.time_to_keep)
            elif args.by_time == 'daily':
                ttk = datetime.timedelta(days = args.time_to_keep)
            elif args.by_time == 'weekly':
                ttk = datetime.timedelta(weeks = args.time_to_keep)

            if (datetime.datetime.now() - snapshot_date) >= ttk:
                destroy_snapshot(snapshot)
    elif args.action == 'create':
        create_snapshot("%s@%s" % (zfs_share, time_stamp(args.by_time)))
    else:
        print "Action not supported"
