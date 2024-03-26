#!/bin/bash
VAR_ARGS=$1
## edited by script##
VMID=1001
VLAN=1001
TEMPLATE_ID=9000
NAME=0
DISK=0
IP=0
GW=0
USER="student"
PASSWORD=0
VCPU=1
MEMORY=0

case $VAR_ARGS in
    create)
        qm clone $TEMPLATE_ID $VMID --name $NAME --full
        qm disk resize $VMID scsi0 $DISK
            qm set $VMID --memory $MEMORY
            qm set $VMID --sockets 2
        qm set $VMID --vcpus $VCPU
        qm set $VMID --ipconfig0 ip=$IP,gw=$GW
        qm set $VMID --net0 virtio,bridge=vmbr0,tag=$VLAN
        qm set $VMID --nameserver '8.8.8.8'
        qm set $VMID --ciuser $USER
        qm set $VMID --cipassword $PASSWORD
        qm set $VMID --onboot 1
        qm start $VMID
        ;;
    delete)
        qm stop $VMID
        qm destroy $VMID
        ;;
    reset)
        qm stop $VMID
        qm destroy $VMID
        qm clone $TEMPLATE_ID $VMID --name $NAME --full
        qm disk resize $VMID scsi0 $DISK
            qm set $VMID --memory $MEMORY
            qm set $VMID --sockets 2
        qm set $VMID --vcpus $VCPU
        qm set $VMID --ipconfig0 ip=$IP,gw=$GW
        qm set $VMID --net0 virtio,bridge=vmbr0,tag=$VLAN
        qm set $VMID --nameserver '8.8.8.8'
        qm set $VMID --ciuser $USER
        qm set $VMID --cipassword $PASSWORD
        qm set $VMID --onboot 1
        qm start $VMID
        ;;
    *)
        echo "Usage: $0 create|delete|reset"
        exit 1
esac