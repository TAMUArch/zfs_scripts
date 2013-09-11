#!/usr/local/bin/python
# Help:
# Simple script to handle bulk creation and deletion of zfs snapshots
#
# Creation:
# creates snapshots in the following format rpool0/root@20130910-1130
#     python py_snapshot.py rpool0/root
#
# Deletion:
# This only works for snapshots that were created with this script or snapshots with the correct
# naming convention.
#
# deletes all snapshots older than 90 days for rpool0/root and tank/important_files:
#     python py_snapshot.py --action destroy --time-to-keep 90 rpool0/root tank/important_files


import commands
import subprocess
import time
import os
import argparse
import datetime

def create_snapshot(zfs_snapshot):
    print "Snapshotting -> %s" % (zfs_share)
    commands.getoutput("zfs snapshot %s" % (zfs_snapshot))

def destroy_snapshot(zfs_snapshot):
    print "Removing snapshot -> %s" % (zfs_snapshot)
    commands.getoutput("zfs destroy %s" % (zfs_snapshot))

def current_snapshots(zfs_share):
    snaps =  commands.getoutput("zfs list -H -t snapshot | awk '{print $1}' | grep %s" % (zfs_share))
    print snaps
    return snaps.split("\n")

parser = argparse.ArgumentParser(description='ZFS Snapshotting Wrapper')
parser.add_argument('--action', type=str, default='create',
                    help='remove or create defaults to %(default)s')
parser.add_argument('--time-to-keep', metavar='DAYS', type=int, default=30,
                    help='delete snapshots after these many days default: %(default)s')
parser.add_argument('zfs_shares', type=str, nargs='+',
                    help='a list of zfs shares eg. pool0/test pool0/test1')
args = parser.parse_args()
timestamp = time.strftime("%Y%m%d-%H%M")

for zfs_share in args.zfs_shares:
    if args.action == 'destroy':
        for snapshot in current_snapshots(zfs_share):
            if snapshot == None or snapshot == '':
                break
	    snapshot_date = datetime.datetime.strptime(snapshot.split("@")[1], "%Y%m%d-%H%M") 
            if (datetime.datetime.now() - snapshot_date) >= datetime.timedelta(days = args.time_to_keep):
                destroy_snapshot(snapshot)
    elif args.action == 'create':
        create_snapshot("%s@%s" % (zfs_share, timestamp))
    else:
        print "Action not supported"
