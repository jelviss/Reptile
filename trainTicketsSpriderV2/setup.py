#!/usr/bin/python
import os, subprocess, sys
subprocess.call(['python', 'virtualenv.py', 'flask'])
if sys.platform == 'win32':
    bin = 'Scripts'
else:
    bin = 'bin'
subprocess.call([os.path.join('flask', bin, 'pip'), 'install', 'flask==0.10'])
subprocess.call([os.path.join('flask', bin, 'pip'), 'install', 'requests'])
subprocess.call([os.path.join('flask', bin, 'pip'), 'install', 'flask-bootstrap'])
subprocess.call([os.path.join('flask', bin, 'pip'), 'install', 'supervisor'])
subprocess.call([os.path.join('flask', bin, 'pip'), 'install', 'rq'])
subprocess.call([os.path.join('flask', bin, 'pip'), 'install', 'rq-dashboard'])
subprocess.call([os.path.join('flask', bin, 'pip'), 'install', 'redis'])
subprocess.call([os.path.join('flask', bin, 'pip'), 'install', 'flask-wtf'])
subprocess.call([os.path.join('flask', bin, 'pip'), 'install', 'flask-login'])
