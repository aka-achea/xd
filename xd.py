#!/usr/bin/python
#coding:utf-8
# Python3

# import sys,os
# from mylog import mylogger as ml

# l = ml(logfile,logfilelevel,__name__) 

#bug: RecursionError: maximum recursion depth exceeded


import argparse,os,time,sys, configparser

# Customized module
from xd_dl import dl_cd,dl_one
from mylognew import get_funcname,mylogger

confile = 'L:\\MUSIC\\xd.ini'
config = configparser.ConfigParser()
config.read(confile)
topdir = config['arch']['topdir']
archdir = config['arch']['archdir']
evadir = config['arch']['evadir']
coverdir = config['arch']['coverdir']
musicure = config['arch']['musicure']
inventory =  config['arch']['inventory']
logfile = config['log']['logfile']
logfilelevel = int(config['log']['logfilelevel'])


def xd():
    l = mylogger(logfile,logfilelevel,get_funcname()) 
    parser = argparse.ArgumentParser(description = 'Xiami download tool')
    parser.add_argument('-s','--song',help='Download single song ')
    parser.add_argument('-c','--cd',help='Download CD',action='store_true')
    parser.add_argument('-a','--artist',help='Download all CD of artist')
    parser.add_argument('-f','--favorite',help='Download favorite list')
    parser.add_argument('-t','--top',help='Download top songs')
    args = parser.parse_args()

    if args.song:
        l.info('Begin download single song')
        link = args.song
        l.info(link)

    elif args.cd == True:
        l.info('Begin download CD')

        # workfolder = 'L:\\XM'
        ldir = r'L:\MUSIC\_DL'
        for w in os.listdir(ldir):
            if os.path.basename(w)[-4:] == 'html':
                l.info(w)
                w = os.path.join(ldir,w)
                web = 'file:///'+w
                # l.info(web)
                dl_cd(web,ldir)
                os.remove(w)
                l.info('Remove '+w)
                for i in range(60):
                    space = 2 if i < 10 else 1
                    sys.stdout.write('Wait'+' '*space+str(60-i)+'\r')
                    time.sleep(1)
   
    
    elif args.artist:
        l.info('Begin download all CD of artist')
        link = args.artist
        l.info(link)

    elif args.favorite:
        l.info('Begin download all CD of artist')
        link = args.favorite
        l.info(link)

    else:
        parser.print_help()

if __name__ == "__main__":
    try:
        xd()
    except KeyboardInterrupt:
        print('ctrl + c')

















