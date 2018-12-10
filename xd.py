#!/usr/bin/python
#coding:utf-8
# Python3

# import sys,os
# from mylog import mylogger as ml

# logfilelevel = 10 # Debug
# logfile = 'E:\\app.log'
# l = ml(logfile,logfilelevel,__name__) 


import argparse

# Customized module
from xd_dl import dl_cd,dl_one



def xd():
    parser = argparse.ArgumentParser(description = 'Xiami download tool')

    parser.add_argument('-s','--song',help='Download single song ')
    parser.add_argument('-c','--cd',help='Download CD')
    parser.add_argument('-a','--artist',help='Download all CD of artist')
    parser.add_argument('-f','--favorite',help='Download favorite list')
    parser.add_argument('-t','--top',help='Download top songs')
    args = parser.parse_args()

    if args.song:
        print('Begin download single song')
        link = args.song
        print(link)

    if args.cd:
        print('Begin download CD')
        link = args.cd
        print(link)

    if args.artist:
        print('Begin download all CD of artist')
        link = args.artist
        print(link)

    if args.favorite:
        print('Begin download all CD of artist')
        link = args.favorite
        print(link)

if __name__ == "__main__":
    xd()

















