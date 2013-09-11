#!/usr/local/bin/python

import commands
import subprocess
import time
import os
import argparse

def create_snapshot(zfs_snapshot):
    print "Snapshotting -> %s" % (zfs_share)
    commands.getoutput("zfs snapshot %s" % (snapshot_name))

def destroy_snapshot(zfs_snapshot):
    print "Removing snapshot -> %s" % zfs_share
    commands.getoutput("zfs destroy %s" % (snapshot_name))

def current_snapshots():
  snaps =  commands.geetoutput("zfs list -H -t snapshot | awk '{print $1}'")
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
      for snapshot in current_snapshots():
        snapshot_date = datetime.datetime.strptime(snapshot.slit("@")[1], "%Y%m%d-%H%M")
        if (datetime.datetime.now() - snapshot_date) >= datetime.timedelta(days = args.time_to_keep):
          destroy_snapshot(snapshot)
    elif args.action == 'create':
      create_snapshot("%(zfs_share)s@%(timestamp)s")
    else:
      print "Action not supported"
