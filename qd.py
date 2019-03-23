#!/usr/bin/python3
#coding:utf-8
# tested in win



import argparse
import os
import time
import sys
import configparser

# Customized module
from qd_dl import dl_album,dl_song
from mylog import get_funcname,mylogger
from sharemod import logfile,logfilelevel,dldir
from mytool import mywait

def qd():
    ml = mylogger(logfile,logfilelevel,get_funcname()) 
    parser = argparse.ArgumentParser(description = 'QQ Music download tool')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-s','--song',help='Download single song ')
    group.add_argument('-c','--cds',help='Download CD Link')
    group.add_argument('-a','--artist',help='Download all CD of artist')
    group.add_argument('-f','--favorite',help='Download favorite list')
    group.add_argument('-t','--top',help='Download top songs')
    args = parser.parse_args()

    if args.song:
        ml.info('Begin download single song')
        link = args.song
        ml.debug(link)
        dl_song(link)

    elif args.cds:
        ml.info('Begin download CDs')
        link = args.cds
        ml.debug(link)
        dl_album(link)
       
    elif args.artist:
        ml.info('Begin download all CD of artist')
        link = args.artist
        ml.info(link)

    elif args.favorite:
        ml.info('Begin download all CD of artist')
        link = args.favorite
        ml.info(link)

    else:
        parser.print_help()

if __name__ == "__main__":
    try:
        qd()
    except KeyboardInterrupt:
        print('ctrl + c')
