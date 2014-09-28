#!/bin/bash

echo "+++ install-essentials.sh +++"
apt-get update
apt-get install -y apt-transport-https
apt-get install -y curl wget git vim less dnsutils
