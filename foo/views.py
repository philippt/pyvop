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
    json_data = open('static/data/machines.raw')
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
    
    for m in machines:
        key = str(m['name'])
        cached = mc.get(key)
        if cached and 'force' not in request.GET.keys():
            print "[cache] hit: %s -> %s" % (key, cached)
            m['status'] = cached
        else:
            print "[cache] miss : %s" % key
            need_data.append(key)
    
    result = {}

    if len(need_data) > 0:
        with_user = ['philippt@%s' % n for n in need_data]

        start_ts = datetime.datetime.now()
        multi_result = execute(get_status, hosts=with_user)
        
        for userhost, status in multi_result.iteritems():
            user, host = userhost.split('@')
            mc_key = str(host)

            print "[cache] write: %s" % mc_key
            result[mc_key] = status
            mc.set(mc_key, status)

        duration = (datetime.datetime.now() - start_ts).total_seconds()
        print "[stats] fetched %d in %d secs" % (len(multi_result.keys()), duration)

    for m in machines:
        if 'status' not in m:
            key = str(m['name'])
            if key in result:
                m['status'] = result[key]

    return render_to_response('foo/map.html', {'machines': machines})


@parallel(pool_size=15)
def get_status():
    s = {
         'timestamp': datetime.datetime.utcnow().strftime("%s"),
         'date': run("date"),
         'timezone': run("date +%Z"),
         'hostname': run("hostname")
    }
    
    s['maint_file_found'] = False
    try:
        run("ls /var/maint/reserve")
        s['maint_file_found'] = True
    except:
        foo = [a for a in 'papperlapapp']

    last_puppet_log = run("tail /var/log/puppet.log | grep -E 'Skipping|Finished' | tail -n1")
    # Sep 28 11:31:21 philippt01 puppet-agent[11661]: Skipping run of Puppet configuration client; administratively disabled (Reason: 'philippt reserve until 2014-09-22 07:38:08 (comment: testing pbuilder)');
    # Sep 28 18:25:23 philippt puppet-agent[19932]: Finished catalog run in 5.95 seconds
                       # timestamp                       hostname
    matched = re.search('(\w+\s+\d+\s+(?:\d{2}|\:){5})\s+(\S+)\s+(\S+)\[(\d+)\]\:\s+(Skipping|Finished)', last_puppet_log)
    s['last_puppet_log'] = last_puppet_log
    if matched:
        groups = matched.groups()
        last_puppet_run = parse(groups[0] + ' %s' % s['timezone'])
        s['puppet_run_at'] = last_puppet_run.isoformat()

        s['minutes_since_last_puppet_run'] = int((parse(s['date']) - last_puppet_run).total_seconds() / 60)
        s['puppet_status'] = groups[4]

    print "got status : %s" % s
    return s 
    
def status(request, name):
    host_name = 'philippt@%s' % name
    multi_result = execute(get_status, hosts=[host_name])
    s = multi_result[host_name]
    return HttpResponse(json.dumps(s), content_type="application/json")
