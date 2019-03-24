#!/usr/bin/python3
#coding:utf-8
# tested in win



import argparse
import re
import os
import time
import sys
import configparser

# Customized module
from qd_dl import qdl_album,qdl_song
from mylog import get_funcname,mylogger
from sharemod import logfile,dldir
from mytool import mywait

def main():
    ml = mylogger(logfile,get_funcname()) 
    parser = argparse.ArgumentParser(description = 'Music download tool')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-s','--song',help='Download single song',action='store_true')
    group.add_argument('-c','--cds',help='Download CD Link',action='store_true')
    group.add_argument('-a','--artist',help='Download all CD of artist')
    group.add_argument('-f','--favorite',help='Download favorite list')
    group.add_argument('-t','--top',help='Download top songs')
    args = parser.parse_args()

    if args.song:
        link = input('>>')
        ml.info('Begin download single song')
        if re.findall('qq',link.split('/')[2]):       
            ml.debug(f"Download from QQMusic {link}")
            qdl_song(link)
        elif re.findall('xiami',link.split('/')[2]):
            ml.debug(f'Download from Xiami {link}')
        else:
            ml.error('Pls check link')       

    elif args.cds:
        link = input('>>')
        ml.info('Begin download CDs')
        if re.findall('qq',link.split('/')[2]):       
            ml.debug(f"Download from QQMusic {link}")
            qdl_album(link)
        elif re.findall('xiami',link.split('/')[2]):
            ml.debug(f'Download from Xiami {link}')
        else:
            ml.error('Pls check link')

       
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
    if os.path.exists(logfile):
        os.remove(logfile)
    try:
        main()
    except KeyboardInterrupt:
        print('ctrl + c')
