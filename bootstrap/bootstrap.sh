#!/bin/bash

NEW_HOSTNAME=$1

[ -z "$NEW_HOSTNAME" ] && (echo "Usage: $0 <new hostname>" && exit 1)
export NEW_HOSTNAME

export BOOTSTRAP_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

$BOOTSTRAP_ROOT/install-essentials.sh
$BOOTSTRAP_ROOT/set-hostname.sh $NEW_HOSTNAME
