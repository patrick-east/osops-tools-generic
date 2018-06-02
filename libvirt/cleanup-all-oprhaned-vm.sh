#!/usr/bin/env bash

set -xe

NODES=($(ls ~/projects/cinder_jenkins_data/puppet/pc2/nodes | sed 's/\.pp//g'))

VIRSH_IDS=""
for SERVER in $(nova list --all-tenants | grep ACTIVE | awk '{print $2;}'); do
    VIRSH_IDS+="$(nova show ${SERVER} | grep 'OS-EXT-SRV-ATTR:instance_name' | awk '{print $4}')\n"
done


for NODE in "${NODES[@]}"; do
    echo "Cleaning orphaned VM's on ${NODE}"
    scp -i ~/.ssh/pure_root ./* root@${NODE}:/root/
    ssh -i ~/.ssh/pure_root root@${NODE} "VIRSH_IDS='${VIRSH_IDS}' /root/cleanup-orphaned-vms.sh"
done
