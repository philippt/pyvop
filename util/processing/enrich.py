import json
import yaml
import sys
import os
import subprocess
import pprint

RAW_FILE = os.path.dirname(os.path.abspath(__file__)) + '/../../static/data/processing/machines.raw'


def main():
    raw_data = open(RAW_FILE)
    loaded=json.load(raw_data)
    
    enriched = []
    for machine in loaded:
        output = subprocess.Popen(["./enc", machine['name']], stdout = subprocess.PIPE, stderr = subprocess.STDOUT).communicate()[0]
        enc_data = yaml.load(output)
        new_one = machine.copy()
        for k,v in enc_data['parameters'].iteritems():
            new_one[k] = v
        pprint.pprint(new_one)
        enriched.append(new_one)

    with open('machines.enriched', 'w') as outfile:
        json.dump(enriched, outfile)
    pprint.pprint(enriched)

if __name__ == '__main__':
    sys.exit(main())
