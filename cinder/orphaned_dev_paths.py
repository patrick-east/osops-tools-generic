#!/usr/bin/env python

import argparse
import sys
import purestorage
import re
import subprocess
import time

def clean_orphan_luns(array_name, hostname, dry_run):
    array = purestorage.FlashArray(array_name, username='pureuser', password='pureuser')
    pure_ports = array.list_ports()
    targets = set()
    for p in pure_ports:
        if p['iqn']:
            targets.add(p['iqn'])
    print "Found targets for array: %s" % targets
    connections = array.list_host_connections(hostname)
    in_use_luns = [c['lun'] for c in connections]
    print "Found in-use LUNS for host: %s" % in_use_luns
    lun_ls_output = subprocess.check_output("ls -la /dev/disk/by-path", shell=True)
    orphans = []
    for line in lun_ls_output.split('\n'):
        print "Processing ls output line: '%s'" % line
        for t in targets:
            if t in line:
                print "Found target: %s" % t
                is_orphan = True
                for real_lun in in_use_luns:
                    if re.search('lun-%s\s' % real_lun, line):
                        print "Found in-use LUN %s" % real_lun
                        is_orphan = False
                        break
                if is_orphan:
                    print "Found orphan lun: " + line
                    parts = line.split(' -> ')
                    raw_device = parts[1]
                    device = raw_device[len('../../'):]
                    lun = parts[0].split('lun-')[1]
                    orphans.append({
                        "ls-output": line,
                        "device": device,
                        "lun": lun,
                    })
    print "Final list of orphans discovered:"
    for o in orphans:
        print "--> %s" % o
    
    if len(orphans) == 0:
        print "No orphans found!\n\nDone!\n"
        sys.exit(0)
    
    print "\n!! Removing orphans !!\n"
    for orphan in orphans:
        cmd = ['sh', '-c', "echo 1 > /sys/block/%s/device/delete" % orphan['device']]
        print "Calling: %s" % cmd
        if not dry_run:
            subprocess.call(cmd)
        else:
            print "--> Dry-run, skipping device delete!"
    
    print "Waiting a few seconds for udev and others to do their thing..."
    time.sleep(5)
    
    cmd = ['iscsiadm', '-m', 'session', '--rescan']
    print "Calling: %s" % cmd
    if not dry_run:
            subprocess.call(cmd)
    else:
        print "--> Dry-run, skipping iscsi rescan!"
        
    print "Waiting again for a few seconds..."
    time.sleep(5)
     
    cmd = ['multipath', '-r']
    print "Calling: %s" % cmd
    if not dry_run:
            subprocess.call(cmd)
    else:
        print "--> Dry-run, skipping multipath rebuild!"
    
    print "\nDone!\n"
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a new cluster of VMs')
    parser.add_argument('array', help='The array IP or FQDN to clean up connections from')
    parser.add_argument('hostname', help='The hostname to clear connections from')
    parser.add_argument('--dry-run', dest='dry_run', action='store_true', help='If set this script will only do logging of actions that would be done')
    
    args = parser.parse_args()
    clean_orphan_luns(args.array, args.hostname, args.dry_run)
