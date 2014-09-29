#!/usr/bin/env python

import sys
import pprint
import json
import sys
import os
# TODO hardcoded philippt-specific
PUPPET_PATH='%s/deviant/puppet' % os.environ['HOME']
sys.path.append(PUPPET_PATH)

from sparket import util

def read_sparket_machines():
    result = []
    sparket = util.load_sparket()
    for hostname, host in sparket.facilities['la'].hosts.iteritems():
        result.append({'type':'host','name':hostname})
        if 'vms' in host:
            for vmname, vm in host.vms.iteritems():
                result.append({'type':'vm','name':vmname})
    return result
    

def main():
    machines = read_sparket_machines()
    json.dump(machines, sys.stdout)

if __name__ == '__main__':
    sys.exit(main())