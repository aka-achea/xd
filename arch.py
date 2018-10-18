#!/usr/bin/python
#coding:utf-8
# Python3


import os,re,shutil

import mylog as ml
logfilelevel = 10 # Debug
logfile = 'E:\\app.log'


def path_art(artist):
    topdir = 'F:\\mp3'
    p_art = ''
    for dirpath, dirnames, files in os.walk(topdir):
        for name in dirnames:
            # print(name)
            if name == artist:
                p_art = os.path.join(dirpath, name)
    return p_art #return last result


def archive_al():
    funcname = 'arch.archive_al'
    l = ml.mylogger(logfile,logfilelevel,funcname) 
    topdir = 'F:\\XM\\_'
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
                p_art = path_art(m[0])
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
                    l.info('Already prearchive -> move album '+dirname)
                    al_dst = os.path.join(topdir,m[0])
                    shutil.move(al_src,al_dst)
                else:
                    l.info('Prearchive '+m[0]+' -> move album '+dirname)
                    os.mkdir(os.path.join(topdir, m[0]))
                    al_dst = os.path.join(topdir,m[0])
                    shutil.move(al_src,al_dst)

            # album = str(dirname).split(" - ")
            # if len(album) == 3:
            #     print(album)
            # p_art = path_art(dirname)
            # if p_art  




if __name__=='__main__':
    # path = path_art("Funky DL")
    # print(path)
    archive_al()

