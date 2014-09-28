import boto
import json
import sys
import pprint


ec2 = vpc = None
cache = {}


def connect():
    global ec2, vpc
    vpc = boto.connect_vpc()
    ec2 = boto.connect_ec2()


def subnet_by_id(subnet_id):
    if subnet_id in cache:
        return cache[subnet_id]
    else:       
        cache[subnet_id] = vpc.get_all_subnets(subnet_id)[0].tags['Name']
        return cache[subnet_id] 


def fetch_instances():
    conn = boto.connect_ec2()
    
    result = []
    for reservation in conn.get_all_instances():
        for instance in reservation.instances:
            result.append({
                           'id': instance.id,
                           'name': instance.tags['Name'],
                           'subnet': subnet_by_id(instance.subnet_id),
                           'groups': [g.name for g in instance.groups]
                           })
    return result

        
def main():
    connect()
    json.dump(fetch_instances(), sys.stdout)
        
if __name__ == '__main__':
    sys.exit(main())