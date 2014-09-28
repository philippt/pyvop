#!/bin/bash

NEW_HOSTNAME=$1

[ -z "$NEW_HOSTNAME" ] && (echo "Usage: $0 <new hostname>" && exit 1)
export NEW_HOSTNAME

export BOOTSTRAP_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

$BOOTSTRAP_ROOT/set-hostname.sh $NEW_HOSTNAME
$BOOTSTRAP_ROOT/install-essentials.sh

# pip
apt-get install -y build-essential python-dev python-pkg-resources python-setuptools
easy_install pip

# fabric
pip install fabric

# django
apt-get install -y python-django libmysqlclient-dev

pip install mysql-python

apt-get install -y memcached python-memcache