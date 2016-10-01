#!/usr/bin/python
import os, subprocess, sys

if sys.platform == 'win32':
    bin = 'Scripts'
else:
    bin = 'bin'

subprocess.call(['python', 'virtualenv.py', 'flask'])
subprocess.call([os.path.join('flask', bin, 'pip'), 'install', 'flask==0.1', '-i','http://pypi.douban.com/simple', '--trusted-host', 'pypi.douban.com'])
subprocess.call([os.path.join('flask', bin, 'pip'), 'install', 'requests', '-i', 'http://pypi.douban.com/simple', '--trusted-host', 'pypi.douban.com'])
subprocess.call([os.path.join('flask', bin, 'pip'), 'install', 'flask-bootstrap', '-i', 'http://pypi.douban.com/simple', '--trusted-host', 'pypi.douban.com'])
subprocess.call([os.path.join('flask', bin, 'pip'), 'install', 'supervisor', '-i', 'http://pypi.douban.com/simple', '--trusted-host', 'pypi.douban.com'])
subprocess.call([os.path.join('flask', bin, 'pip'), 'install', 'rq', '-i','http://pypi.douban.com/simple', '--trusted-host', 'pypi.douban.com'])
subprocess.call([os.path.join('flask', bin, 'pip'), 'install', 'rq-dashboard', '-i', 'http://pypi.douban.com/simple', '--trusted-host', 'pypi.douban.com'])
subprocess.call([os.path.join('flask', bin, 'pip'), 'install', 'redis', '-i', 'http://pypi.douban.com/simple', '--trusted-host', 'pypi.douban.com'])
subprocess.call([os.path.join('flask', bin, 'pip'), 'install', 'flask-wtf', '-i' , 'http://pypi.douban.com/simple', '--trusted-host', 'pypi.douban.com'])
subprocess.call([os.path.join('flask', bin, 'pip'), 'install', 'flask-login', '-i' ,'http://pypi.douban.com/simple', '--trusted-host', 'pypi.douban.com'])
