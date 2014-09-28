import pprint
import json
import re
import datetime
from dateutil.parser import parse
from django.template import Context, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response
from fabric.api import *
import memcache

mc = memcache.Client(['127.0.0.1:11211'], debug=0)


def index(request):
    print "foo!"
    return HttpResponse("the infamous foo index!")


def public(request):
    return HttpResponse("this is what the public gets to see!")


def read_machines(request=None):
    '''reads machines from a JSON file and applies filters from the request'''
    json_data = open('static/data/processing/machines.raw')
    result = json.load(json_data)
    if request:
        print request.GET.keys()
        if 'filter' in request.GET.keys():
            filter = request.GET['filter']
            regex = re.compile(filter)
            filtered = [x for x in result if 'name' in x and regex.match(x['name'])]
            result = filtered
    return result


def machines(request):
    machines = read_machines(request)
    return HttpResponse(json.dumps(machines), content_type="application/json")


def list(request):
    return render_to_response('foo/list.html', {'machines': read_machines(request)})


def machine(request, name):
    host_name = 'philippt@%s' % name
    multi_result = execute(get_status, hosts=[host_name])
    s = multi_result[host_name]
    s['name'] = name
    return render_to_response('foo/machine.html', s)


def map(request):
    machines = read_machines(request)
    need_data = []
    result = {}
    
    for m in machines:
        key = str(m['name'])
        cached = mc.get(key)
        if cached:
            print "[cache] hit: %s -> %s" % (key, cached)
            m['status'] = cached
    
    targets = []
    for m in machines:
        if 'status' not in m:
            print "[cache] miss : %s" % m['name']
            targets.append(m['name'])
            
    if len(targets) > 0:
        with_user = ['philippt@%s' % t for t in targets]    
        multi_result = execute(get_status, hosts=with_user)
        
        for userhost, result in multi_result.iteritems():
            user, host = userhost.split('@')
            
            the_machine = [m for m in machines if m['name'] == host][0]
            the_machine['status'] = result

            mc_key = str(host)
            print "[cache] write: %s" % mc_key
            mc.set(mc_key, result)
                        
    return render_to_response('foo/map.html', {'machines': machines})


@parallel
def get_status():
    s = {
         'timestamp': datetime.datetime.utcnow().strftime("%s"),
         'date': run("date"), 
         'hostname': run("hostname")
    }
    
    try:
        run("ls /var/maint/reserve")
        s['maint_file_found'] = True
    except:
        s['maint_file_found'] = False

    last_puppet_log = run("tail /var/log/puppet.log | grep -E 'Skipping|Finished' | tail -n1")
    # Sep 28 11:31:21 philippt01 puppet-agent[11661]: Skipping run of Puppet configuration client; administratively disabled (Reason: 'philippt reserve until 2014-09-22 07:38:08 (comment: testing pbuilder)');
    # Sep 28 18:25:23 philippt puppet-agent[19932]: Finished catalog run in 5.95 seconds
                       # timestamp                       hostname
    matched = re.search('(\w+\s+\d+\s+(?:\d{2}|\:){5})\s+(\S+)\s+(\S+)\[(\d+)\]\:\s+(Skipping|Finished)', last_puppet_log)
    s['last_puppet_log'] = last_puppet_log
    if matched:
        groups = matched.groups()
        last_puppet_run = parse(groups[0])
        s['puppet_run_at'] = last_puppet_run.isoformat() #.strftime('%s')
        
        #with settings(warn_only=True):
        #    s['minutes_since_last_puppet_run'] = (parse(s['date']) - last_puppet_run) / 60
        s['puppet_status'] = groups[4]

    print "got status : %s" % s
    return s 
    
def status(request, name):
    host_name = 'philippt@%s' % name
    multi_result = execute(get_status, hosts=[host_name])
    s = multi_result[host_name]
    return HttpResponse(json.dumps(s), content_type="application/json")
