#!/bin/bash

echo "+++ install-essentials.sh +++"
apt-get update
apt-get install -y apt-transport-https
apt-get install -y curl wget git vim less dnsutils

# fabric
apt-get install -y build-essential python-dev python-pkg-resources python-setuptools
easy_install pip
pip install fabric
