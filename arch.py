#!/usr/bin/python
#coding:utf-8
# Python3


import os,re,shutil,argparse,configparser

# customized module
from comm import readtag 
import mylog as ml


confile = 'E:\\xd.ini'
config = configparser.ConfigParser()
config.read(confile)
topdir = config['arch']['topdir']
archdir = config['arch']['archdir']
evadir = config['arch']['evadir']
coverdir = config['arch']['coverdir']
musicure = config['arch']['musicure']
logfile = config['log']['logfile']
logfilelevel = int(config['log']['logfilelevel'])

def find_art(topdir,artist):
    funcname = 'arch.find_art'
    l = ml.mylogger(logfile,logfilelevel,funcname) 
    p_art = ''
    for dirpath, dirnames, files in os.walk(topdir):
        for name in dirnames:
            l.debug(name)
            if name == artist:
                p_art = os.path.join(dirpath, name)
    return p_art #return last result


def rename_mp3(topdir):
    funcname = 'arch.rename_mp3'
    l = ml.mylogger(logfile,logfilelevel,funcname) 
    for mp3 in os.listdir(topdir):        
        p_mp3 = os.path.join(topdir,mp3)
        if p_mp3[-3:] == 'mp3':
            # print(mp3[:-3])
            d = readtag(p_mp3)
            singer = str(d[0])
            title = str(d[1])
            songname = singer+' - '+title+'.mp3'
            if mp3 != songname:
                l.info('Change '+mp3+'  --->  '+songname)
                src = p_mp3
                dst = os.path.join(topdir,songname)
                l.debug(src)
                l.debug(dst)
                os.rename(src,dst)


def archive_cd(evadir,archdir):
    funcname = 'arch.archive_cd'
    l = ml.mylogger(logfile,logfilelevel,funcname)     
    for dirname in os.listdir(evadir):  
        al_src = os.path.join(evadir, dirname)             
        if os.path.isdir(al_src) == True:
            l.debug(al_src)
            m = re.split('\s\-\s\d{4}\s\-\s',str(dirname))
            if len(m) == 2: #find album

                pic_src = os.path.join(evadir,dirname,dirname+'.jpg')
                l.debug(pic_src)
                pic_dst = os.path.join(evadir,dirname+'.jpg')
                l.debug(pic_dst)
                shutil.copyfile(pic_src,pic_dst)

                l.info('Searching Artist: '+m[0])
                p_art = find_art(archdir,m[0])
                l.debug(p_art)
                if os.path.isdir(p_art) == True :
                    # l.info(p_art)
                    l.info('Archive '+dirname)

                    al_dst = p_art
                    l.debug(al_dst)                   
                    shutil.move(al_src,al_dst)
                    if os.path.isdir(al_dst) == True: 
                        l.info("Archive complete")               
                elif os.path.isdir(os.path.join(evadir, m[0])) == True:
                    l.warning('Already prearchive -> move album '+dirname)
                    al_dst = os.path.join(evadir,m[0])
                    shutil.move(al_src,al_dst)
                else:
                    l.warning('Prearchive '+m[0]+' -> move album '+dirname)
                    os.mkdir(os.path.join(evadir, m[0]))
                    al_dst = os.path.join(evadir, m[0])
                    shutil.move(al_src,al_dst)


def move_mp3(topdir,musicure):
    funcname = 'arch.move_mp3'
    l = ml.mylogger(logfile,logfilelevel,funcname)    
    for mp3 in os.listdir(topdir):
        if mp3[-3:] == 'mp3':
            l.info('Move --> '+mp3)
            src = os.path.join(topdir,mp3)
            dst = os.path.join(musicure,mp3)
            l.debug(src)
            l.debug(dst)
            shutil.move(src,dst)


def move_cover(evadir,coverdir):
    funcname = 'arch.move_cover'
    l = ml.mylogger(logfile,logfilelevel,funcname)        
    for jpg in os.listdir(evadir):
        if jpg[-3:] == 'jpg':
            l.info('Move --> '+jpg)
            src = os.path.join(evadir,jpg)
            dst = os.path.join(coverdir,jpg)
            l.info(src)
            l.info(dst)
            shutil.move(src,dst)
#move a-z, manuel check others

def evaluate_art(topdir,musicure):
    funcname = 'arch.evaluate_art'
    l = ml.mylogger(logfile,logfilelevel,funcname)
    for art in os.listdir(topdir):
        if os.path.isdir(os.path.join(topdir,art)) == True:
            l.info('=========================')
            l.info('Evaluate '+art)
            n = 0
            for dirpath, dirnames, files in os.walk(musicure):
                for name in files:
                    #bug name contain -
                    if str(name).split('-')[0].strip() == art:
                        l.info(name)
                        n += 1
            if n == 0:    
                l.warning('Zero !!! Track ---> Move to misc')
            elif n == 1:
                l.warning('One more CD to evaluate')
            else:
                l.info('Total '+str(n)+' Tracks') 

def main():
    funcname = 'arch.main'
    l = ml.mylogger(logfile,logfilelevel,funcname) 
    parser = argparse.ArgumentParser(description = 'Archive music tool')
    parser.add_argument('-a',action="store_true", help='Archive CD')
    parser.add_argument('-e',action="store_true", help='Evaluate artist')
    parser.add_argument('-r',action="store_true", help='Rename MP3')
    parser.add_argument('-m',action="store_true", help='Move MP3')
    parser.add_argument('-f',action="store_true", help='Find Artist')

    args = parser.parse_args()

    if args.a :
        print('Archive CD')
        archive_cd(topdir,archdir)
        # move_cover(evadir,coverdir)

    if args.e:
        print('Evaluate artist')
        evaluate_art(evadir,musicure)

    if args.r:
        print('Rename MP3')
        rename_mp3(topdir)

    if args.m:
        print('Move MP3')
        move_mp3(topdir,musicure)

    if args.f:
        artist = input("Find Artist:  ")
        path = find_art(topdir,artist)
        l.info(path)

if __name__ == "__main__":
    main()

