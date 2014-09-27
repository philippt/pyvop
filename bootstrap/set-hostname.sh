#!/bin/bash

NEWHOSTNAME=$1

if [ -z "$NEWHOSTNAME" ]; then
    echo "Usage: $0 <new host name>"
    exit 1;
fi

hostname $NEWHOSTNAME
hostname > /etc/hostname
cat /etc/hosts | sed -e "s/^127\.0\.1\.1.*/127.0.0.1\t$NEWHOSTNAME.lan\t$NEWHOSTNAME/g" > /etc/hosts.new
mv /etc/hosts.new /etc/hosts
cat /etc/resolv.conf | sed -e "s/localdomain/lan/g" > /etc/resolv.conf.new
mv /etc/resolv.conf.new /etc/resolv.conf

echo -e "\nnew hostname : `hostname -f`\n"
