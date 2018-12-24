#!/usr/bin/python
#coding:utf-8
# Python3

# import sys,os
# from mylog import mylogger as ml

# logfilelevel = 10 # Debug
# logfile = 'E:\\app.log'
# l = ml(logfile,logfilelevel,__name__) 


import argparse,os,time

# Customized module
from xd_dl import dl_cd,dl_one



def xd():
    parser = argparse.ArgumentParser(description = 'Xiami download tool')

    parser.add_argument('-s','--song',help='Download single song ')
    parser.add_argument('-c','--cd',help='Download CD',action='store_true')
    parser.add_argument('-a','--artist',help='Download all CD of artist')
    parser.add_argument('-f','--favorite',help='Download favorite list')
    parser.add_argument('-t','--top',help='Download top songs')
    args = parser.parse_args()

    if args.song:
        print('Begin download single song')
        link = args.song
        print(link)

    elif args.cd == True:
        print('Begin download CD')

        workfolder = 'L:\\XM'
        ldir = 'L:\\XM'
        for w in os.listdir(ldir):
            if os.path.basename(w)[-4:] == 'html':
                print(w)
                w = os.path.join(ldir,w)
                web = 'file:///'+w
                # print(web)
                dl_cd(web,workfolder)
                os.remove(w)
                print('Remove '+w)
                time.sleep(60)
    
    
    elif args.artist:
        print('Begin download all CD of artist')
        link = args.artist
        print(link)

    elif args.favorite:
        print('Begin download all CD of artist')
        link = args.favorite
        print(link)

    else:
        parser.print_help()

if __name__ == "__main__":
    try:
        xd()
    except KeyboardInterrupt:
        print('ctrl + c')

















