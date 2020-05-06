#!/usr/bin/python3
#coding:utf-8
__version__ = 20200506

import os
from mylog import mylogger,get_funcname



logfilelevel = 10

topdir = r'M:\Music'
dldir = os.path.join(topdir,'_DL')
archdir = os.path.join(topdir,'_Archived')
evadir = os.path.join(topdir,'_')
inventory = os.path.join(topdir,'MI.txt')
albumlist = os.path.join(topdir,'album.txt')
db = os.path.join(topdir,'music.db')
logfile = os.path.join(topdir,'xd.log')

coverdir = r'O:\LifeTrack\CD'
musicure = r'O:\MusiCure'
