#!/usr/bin/env python
# ~*~ coding: utf-8 ~*~

from threading import Thread
import os
import subprocess

try:
    from config import config as env_config, env

    CONFIG = env_config.get(env, 'default')()
except ImportError:
    CONFIG = type('_', (), {'__getattr__': None})()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

apps_dir = os.path.join(BASE_DIR, 'apps')


def start_django():
    http_host = CONFIG.HTTP_BIND_HOST or '127.0.0.1'
    http_port = CONFIG.HTTP_LISTEN_PORT or '8080'
    os.chdir(apps_dir)
    print('start django')
    #subprocess是python创建子进程的工具，其实和c中的fork出一个子进程，然后在子进程中运行exec执行另外一个进程很类似。
    #父进程等待子进程完成
    # #返回退出信息(returncode，相当于exit code)
    subprocess.call('python ./manage.py runserver %s:%s' % (http_host, http_port), shell=True)


def start_celery():
    os.chdir(apps_dir)
    os.environ.setdefault('C_FORCE_ROOT', '1')
    os.environ.setdefault('PYTHONOPTIMIZE', '1')
    print('start celery')
    subprocess.call('celery -A common worker -B -s /tmp/celerybeat-schedule -l debug', shell=True)


def main():
    t1 = Thread(target=start_django, args=())
    t2 = Thread(target=start_celery, args=())

    t1.start()
    t2.start()

    t1.join()
    t2.join()


if __name__ == '__main__':
    main()






