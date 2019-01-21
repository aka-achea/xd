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
from mylog import get_funcname,mylogger
from sharemod import logfile,logfilelevel,dldir
from mytool import mywait

def xd():
    l = mylogger(logfile,logfilelevel,get_funcname()) 
    parser = argparse.ArgumentParser(description = 'Xiami download tool')
    parser.add_argument('-s','--song',help='Download single song ')
    parser.add_argument('-c','--cds',help='Download CD',action='store_true')
    parser.add_argument('-a','--artist',help='Download all CD of artist')
    parser.add_argument('-f','--favorite',help='Download favorite list')
    parser.add_argument('-t','--top',help='Download top songs')
    args = parser.parse_args()

    if args.song:
        l.info('Begin download single song')
        link = args.song
        l.info(link)

    elif args.cds == True:
        l.info('Begin download CDs')
        for w in os.listdir(dldir):
            if os.path.basename(w)[-4:] == 'html':
                l.info(w)
                w = os.path.join(dldir,w)
                web = 'file:///'+w
                # l.info(web)
                dl_cd(web,dldir)
                os.remove(w)
                l.info('Remove '+w)
                mywait(60)

       
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

















