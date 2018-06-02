#!/usr/bin/env bash

echo ---------------------------------------------
echo Cleaning up orphaned dev paths for $1 and $2

ARRAY=$1
HOST=$2

set -xe
scp ./orphaned_dev_paths.py root@${HOST}:/root/
ssh root@${HOST} /root/orphaned_dev_paths.py "${ARRAY}" "${HOST}"
set +xe

echo --------------------------------------------
