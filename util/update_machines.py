#!/usr/bin/env python

import sys
import os
import glob
import subprocess
import re
import pprint
import json


def main():
    fetcher_dir = os.path.dirname(os.path.abspath(__file__)) + '/fetch'
    print "working in %s" % fetcher_dir
    fetcher_re = re.compile('fetch_(.+)\.py$')
    fetched = []
    for candidate in os.listdir(fetcher_dir):
        matched = fetcher_re.match(candidate)
        if matched:
            ext = matched.groups()[0]
            full_name = fetcher_dir + '/' + candidate
            print "[%s] %s" % (ext, full_name)
            raw_data = subprocess.Popen(['python', full_name], stdout = subprocess.PIPE, stderr = subprocess.STDOUT).communicate()[0]            
            
            target_file = 'machines.%s' % ext
            with open(target_file, 'w') as outfile:
                outfile.write(raw_data)
                        
            loaded=json.loads(raw_data)
            for item in loaded:
                item['source'] = ext
            fetched = fetched + loaded
            print " -- > %s (%d)" % (target_file, len(loaded)) 
    
    with open('../processing/machines.raw', 'w') as outfile:
        json.dump(fetched, outfile)

if __name__ == '__main__':
    sys.exit(main())