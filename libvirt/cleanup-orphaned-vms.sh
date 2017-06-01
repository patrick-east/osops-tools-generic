#!/usr/bin/env bash




if [ -z "$VIRSH_IDS" ]; then
    echo "VIRSH_IDS value not defined"
    exit 1
fi

for i in `virsh list --all | grep -E '^ [0-9-]+' | awk '{print $2;}'` ; do

    if [[ "${VIRSH_IDS}" != *"$i"* ]]; then
        echo -n "+ $i is NOT known to OpenStack, removing managedsave info... "
        [ ! -z "$1" ] && virsh managedsave-remove $i 1>/dev/null 2>&1
        echo -n "destroying VM... "
        [ ! -z "$1" ] && virsh destroy $i 1>/dev/null 2>&1
        echo -n "undefining VM... "
        [ ! -z "$1" ] && virsh undefine $i 1>/dev/null 2>&1
        echo DONE
    else
        echo "* $i is known to OpenStack, not removing."
    fi
done
