#!/usr/bin/env python

import subprocess

def  pkg_contents(p):
     return subprocess.check_call(["explodepkg", p])

def  main():
     print 'hello'
     pkg_contents("slack.tgz")
