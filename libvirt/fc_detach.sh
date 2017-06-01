#!/usr/bin/env bash

echo ---------------------------------------------
echo Cleaning up FC HBAs for $1

echo virsh nodedev-detach pci_0000_XX_XX_X
ssh -i ~/.ssh/jenkins_key root@$1 "lspci | grep -i Fib | awk '{print \$1}' | sed 's/[:.]/_/g' | xargs -n 1 -I {} virsh nodedev-dettach pci_0000_{}"

echo virsh nodedev-reset pci_0000_XX_XX_X
ssh -i ~/.ssh/jenkins_key root@$1 "lspci | grep -i Fib | awk '{print \$1}' | sed 's/[:.]/_/g' | xargs -n 1 -I {} virsh nodedev-reset pci_0000_{}"

echo virsh nodedev-reatach pci_0000_XX_XX_X
ssh -i ~/.ssh/jenkins_key root@$1 "lspci | grep -i Fib | awk '{print \$1}' | sed 's/[:.]/_/g' | xargs -n 1 -I {} virsh nodedev-reattach pci_0000_{}"

echo unbinding and rebinding to qla2xx
ssh -i ~/.ssh/jenkins_key root@$1 "lspci | grep -i Fib | awk '{print \$1}' | xargs -n 1 -I {} bash -c \"echo 0000:{} > /sys/bus/pci/drivers/qla2xxx/unbind && echo 0000:{} > /sys/bus/pci/drivers/qla2xxx/bind\"" 

ssh -i ~/.ssh/jenkins_key root@$1 "qaucli -pr fc -g"

echo --------------------------------------------
