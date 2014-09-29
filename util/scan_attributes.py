#!/usr/bin/env python

import sys
import json

RAW_FILE='machines.raw'


def scan(file_name):
    raw_data = open(file_name)
    loaded=json.load(raw_data)
    
    collected = {}
    
    for machine in loaded:
        for k,v in machine.iteritems():
            if k not in ['id','name']:
                if k not in collected:
                    collected[k] = []
                collected[k].append(v)
                
    counted = {}

    for k, values in collected.iteritems():
        print "%s : %d" % (k, len(values))
        counted[k] = {}
        all_values = []
        if k == 'groups':
            for groups in values:
                for group in groups:
                    all_values.append(group)
        else:
            all_values = values

        for v in all_values:
            old_value = 0
            if v in counted[k]:
                old_value = counted[k][v]
            counted[k][v] = old_value + 1

    return counted

def main():
    counted = scan(RAW_FILE)

    for k, counts in counted.iteritems():
        print k
        for v, count in counts.iteritems():
            print "  %s : %d" % (v, count)

if __name__ == '__main__':
    sys.exit(main())