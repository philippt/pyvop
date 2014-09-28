from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

import subprocess

#env.hosts.extend(['philippt@philippt01.da'])

def hello(name="world"):
    print("Hello %s!" % name)


def init_github():
    print("+++ init_github +++")
    local("git init")
    local("touch README.md && git add README.md")
    local("git commit -m 'first commit'")
    local("git remote add origin https://github.com/philippt/pyvop.git")
    local("git push -u origin master")


def install():
    #run("sudo apt-get install -y mysql-server")
    print "foo"
    

#@hosts('philippt@philippt01.da')
def maint_status():
    run("sudo maint")


def deploy():
    print("+++ deploy +++")
    code_dir = '/srv/django/pyfoo'
    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            run("git clone git@github.com:/philippt/pyvop.git %s" % code_dir)
    with cd(code_dir):
        run("git pull")
        run("touch app.wsgi")


def update_machines():
    work_dir = '.'
    fetcher_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fetch')
    for fetcher in glob.glob(os.path.join(fetcher_dir, '*.py')):
        output = subprocess.Popen([fetcher], stdout = subprocess.PIPE, stderr = subprocess.STDOUT).communicate()[0]
    #with cd()