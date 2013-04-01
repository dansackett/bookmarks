from fabric.api import env, run, cd, local, sudo

APP_PATH = '/home/dansackett/webapps/bookmarking/bookmarks/'

env.use_ssh_config = True
env.hosts = [
    'dansackett@75.126.24.88',
]


def deploy():
    # test()
    push()
    with cd(APP_PATH):
        run('git pull origin master')
        run('python2.7 manage.py collectstatic')
        run('pip install -r reqs/base.txt')
        run('python2.7 manage.py syncdb')
        run('python2.7 manage.py migrate')
    restart()


def restart():
    run('/home/dansackett/webapps/bookmarking/apache2/bin/restart')


def push():
    local('git push origin master')


def test():
    local('py.test')
