zfs_scripts
===========

Random scripts we use to help manage ZFS on Omnios.

py_snapshot.py
--------------

Makes creation and deletion of multiple snapshots simple, by default it
does snapshots with the hourly format.  ex: 20140128-0550

The daily format removes the hour and minute and the weekly format replaces
-hourminute with the word week followed by the week of the year.

The following will take a snapshot using the daily timestamp:
```
python py_snapshot.py --by-time=daily tank/test
```

to destroy all dailies past 7 days you would execute the following:
```
python py_snapshot.py --by-time=daily --action=destroy --time-to-keep=7 tank/test
```
