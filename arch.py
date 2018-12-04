#!/usr/bin/python
#coding:utf-8
# Python3


import os,re,shutil
from comm import readtag 

import mylog as ml
logfilelevel = 10 # Debug
logfile = 'E:\\app.log'


def path_art(topdir,artist):
    funcname = 'arch.path_art'
    l = ml.mylogger(logfile,logfilelevel,funcname) 
    p_art = ''
    for dirpath, dirnames, files in os.walk(topdir):
        for name in dirnames:
            # print(name)
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


def archive_album(topdir,archdir):
    funcname = 'arch.archive_album'
    l = ml.mylogger(logfile,logfilelevel,funcname)     
    for dirname in os.listdir(topdir):  
        al_src = os.path.join(topdir, dirname)             
        if os.path.isdir(al_src) == True:
            l.debug(al_src)
            m = re.split('\s\-\s\d{4}\s\-\s',str(dirname))
            if len(m) == 2: #find album

                pic_src = os.path.join(topdir, dirname,dirname+'.jpg')
                l.debug(pic_src)
                pic_dst = os.path.join(topdir,dirname+'.jpg')
                l.debug(pic_dst)
                shutil.copyfile(pic_src,pic_dst)

                l.info('Searching Artist: '+m[0])
                p_art = path_art(archdir,m[0])
                # l.info(p_art)
                if os.path.isdir(p_art) == True :
                    # l.info(p_art)
                    l.info('Archive '+dirname)

                    al_dst = p_art
                    l.debug(al_dst)                   
                    shutil.move(al_src,al_dst)
                    if os.path.isdir(al_dst) == True: 
                        l.info("Archive complete")               
                elif os.path.isdir(os.path.join(topdir, m[0])) == True:
                    l.warning('Already prearchive -> move album '+dirname)
                    al_dst = os.path.join(topdir,m[0])
                    shutil.move(al_src,al_dst)
                else:
                    l.warning('Prearchive '+m[0]+' -> move album '+dirname)
                    os.mkdir(os.path.join(topdir, m[0]))
                    al_dst = os.path.join(topdir,m[0])
                    shutil.move(al_src,al_dst)

            # album = str(dirname).split(" - ")
            # if len(album) == 3:
            #     print(album)
            # p_art = path_art(dirname)
            # if p_art  


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


def move_cover(topdir,coverdir):
    funcname = 'arch.move_cover'
    l = ml.mylogger(logfile,logfilelevel,funcname)
        
    for jpg in os.listdir(topdir):
        if jpg[-3:] == 'jpg':
            l.info('Move --> '+jpg)
            src = os.path.join(topdir,jpg)
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
                    if str(name).split('-')[0].strip() == art:
                        l.info(name)
                        n += 1
            if n == 0:    
                l.warning('Zero !!! Track ---> Move to misc')
                pass
            elif n == 1:
                l.warning('One more albume to evaluate')
            else:
                l.info('Total '+str(n)+' Track') 




if __name__=='__main__':
    archdir = 'F:\\Music\\_Archived'
    musicure = 'J:\\MusiCure'

    # path = path_art(topdir,"Funky DL")
    # print(path)

    # topdir = 'F:\\Music'
    # # rename_mp3(topdir)
    # move_mp3(topdir,musicure)

    topdir = 'F:\\Music\\_'
    coverdir = 'J:\\LifeTrack\\CD'
   

    # archive_album(topdir,archdir)
    # move_cover(topdir,coverdir)
    evaluate_art(topdir,musicure)



