#!/usr/bin/python
#coding:utf-8
# Python3
# Version: 2018.10.22

# CRITICAL    50
# ERROR   40
# WARNING 30
# INFO    20
# DEBUG   10
# NOTSET  0


import logging,coloredlogs

class mylogger():
    def __init__(self,logfile,logfilelevel,funcname):
        self.funcname = funcname
        logging.basicConfig(level=logfilelevel,filename=logfile,filemode='w',
                            datefmt='%m-%d %H:%M:%S',
                            format='%(asctime)s <%(name)s>[%(levelname)s] %(message)s')
        self.logger = logging.getLogger(funcname)
        coloredlogs.DEFAULT_LEVEL_STYLES= {
                                        #'debug': {'color': 'magenta','bold': True},
                                        'info': {'color': 'green','bold': True},
                                        'warning': {'color': 'yellow','bold': True},
                                        'error': {'color': 'red','bold': True},
                                        'critical': {'color': 'magenta','bold': True}
                                            }
        coloredlogs.DEFAULT_LOG_FORMAT = '%(message)s'
        coloredlogs.install(level='info',logger=self.logger)  

    def debug(self,msg):
        self.logger.debug(msg)

    def info(self,msg):
        self.logger.info(msg)

    def warning(self,msg):
        self.logger.warning(msg)

    def error(self,msg):
        self.logger.error(msg)

    def critical(self,msg):
        self.logger.critical(msg)

    def verbose(self,msg):
        self.logger.debug(msg)

if __name__=='__main__': #Usage
    funcname = __name__
    logfilelevel = 10 # Debug
    logfile = 'E:\\app.log'
    l = mylogger(logfile,logfilelevel,funcname)    
    l.debug('This is Debug')
    l.info('ール・デ')
    l.error('error log')
    l.warning('warning log')
    l.critical("this is a critical message")
    l.verbose('vvvvv')
