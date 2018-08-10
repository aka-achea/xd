#!/usr/bin/python
#coding:utf-8
# Python3

import mylog as l


logfilelevel = 10 # Debug
logfile = 'E:\\app.log'
l.setup(logfile,logfilelevel)    
l.debug('This is Debug')
l.info('This is info')
l.warning("this is warning")
l.error("this is error ")
l.critical("this is critical ")

