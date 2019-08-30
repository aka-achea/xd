#!/usr/bin/python3
#coding:utf-8
#version: 20190828
#tested in win


import os
import configparser


# customized module
from mylog import get_funcname,mylogger

if os.path.exists(r'L:\MUSIC\xd.ini'):  
    confile = r'L:\MUSIC\xd.ini'
else:
    confile = r'E:\MUSIC\xd.ini'
        

config = configparser.ConfigParser()
config.read(confile)
topdir = config['arch']['topdir']
archdir = config['arch']['archdir']
dldir = config['arch']['dldir']
evadir = config['arch']['evadir']
coverdir = config['arch']['coverdir']
musicure = config['arch']['musicure']
inventory = config['arch']['inventory']
albumlist = config['arch']['albumlist']
db = config['arch']['db']
logfile = config['log']['logfile']
# logfilelevel = int(config['log']['logfilelevel'])

