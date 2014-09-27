from __future__ import with_statement
from fabric.api import local, settings, abort, run, cd
from fabric.contrib.console import confirm

def hello(name="world"):
    print("Hello %s!" % name)


def init_github():
    print("+++ init_github +++")
    local("git init")
    local("touch README.md && git add README.md")
    local("git commit -m 'first commit'")
    local("git push -u origin master")


def deploy():
    print("+++ deploy +++")
    code_dir = '/srv/django/pyfoo'
    with cd(code_dir):
        run("git pull")
        run("touch app.wsgi")