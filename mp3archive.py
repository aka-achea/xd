#!/usr/bin/python3
#coding:utf-8
# tested in win
__version__ = 20201210

import os
import re
import shutil
import argparse
import configparser
import sqlite3
import sys
from prettytable import from_db_cursor

# customized module
from config import logfile,inventory,topdir,archdir,evadir,musicure,coverdir,db,albumlist
from mtag import readtag
import myfs
from mylog import  mylogger,get_funcname

ml = mylogger(logfile) 

class database():  
    def create(self):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute('create table music (\
                        fullname varchar(200) primary key,\
                        artist varchar(100),\
                        year varchar(5),\
                        album varchar(100) )'
                        )
        cursor.close()
        conn.close()

    def insert(self,alist):
        ml = mylogger(logfile,get_funcname()) 
        conn = sqlite3.connect(db)
        cursor = conn.cursor()    
        ml.dbg(alist)    
        fullname = alist[0]
        artist = alist[1]
        year = alist[2]
        album = alist[3]    
        try:
            cursor.execute("insert into music values (?,?,?,?)",(fullname,artist,year,album))
        except sqlite3.Integrityerr as e:
            ml.err(e)
            ml.err('duplicate entry')
        cursor.close()
        conn.commit()
        conn.close()

    def query(self,q='',keyword=''):
        ml = mylogger(logfile,get_funcname()) 
        if q in ['fullname','artist','year','album']:
            cmd = 'select * from music where '+q+' like "%'+keyword+'%" order by artist' 
        elif keyword =='' and q =='':
            cmd = 'select * from music'
        else:
            ml.err('Missing keyword')
            sys.exit()
        conn = sqlite3.connect(db)
        cursor = conn.cursor()  
        ml.dbg(cmd)
        cursor.execute(cmd)
        num = len(cursor.fetchall())
        ml.dbg(num)
        if num == 0:
            ml.dbg('No Entry find')
            return False
        cursor.execute(cmd) # need to improve
        v = from_db_cursor(cursor)
        v.align['album']='l'
        cursor.close()
        conn.close()
        return v  


def build_albumlist(albumlist,coverdir):   
    '''Build CD inventory by scanning CD dir'''     
    with open(albumlist,'w',encoding='utf-8') as f:
        for fd in os.listdir(coverdir):
            if os.path.isdir(os.path.join(coverdir,fd)):
                for cover in os.listdir(os.path.join(coverdir,fd)):        
                    f.write(cover[:-4]+'\n')


def build_inventory(inventory,archdir):      
    '''Build Artist Inventory of archive folder'''  
    with open(inventory,'w',encoding='utf-8') as f:
        for p in os.listdir(archdir):
            pdir = os.path.join(archdir,p)
            for adir in os.listdir(pdir):
                if adir !=  '_VA':               
                    f.write(os.path.join(pdir,adir)+'\n')


# def find_art(artist,inventory,match=True):
#     '''Find artist path in inventory'''
#     p_art = []
#     if artist[-1] == '.':  # windows folder name cannot end with .
#         artist = artist[:-2] 
#     with open(inventory,'r',encoding='utf-8') as f:  
#         if match:
#             for i in f.readlines():
#                 if artist.upper() == i.strip().split('\\')[-1].upper():
#                     p_art = i.strip()
#                     # for n in os.listdir(p_art): print(n)
#                     return p_art
#         else:
#             for i in f.readlines():
#                 if artist.upper() in i.strip().split('\\')[-1].upper():
#                     p_art.append(i.strip())
#             return p_art
#     return 'No artist'


def find_art(artist,inventory,match=True):
    '''Find artist path in inventory'''
    p_art = []
    if artist[-1] == '.':  # windows folder name cannot end with .
        artist = artist[:-2] 
    with open(inventory,'r',encoding='utf-8') as f:          
        for i in f.readlines():
            if match:
                if artist.upper() == i.strip().split('\\')[-1].upper():
                    return i.strip()
            else:
                if artist.upper() in i.strip().split('\\')[-1].upper():
                    p_art.append(i.strip())
    return p_art if p_art != [] else 'No artist'


def rename_mp3(folder=topdir): 
    '''Rename MP3 based on ID3 tag'''
    ml = mylogger(logfile,get_funcname()) 
    for mp3 in os.listdir(folder):        
        p_mp3 = os.path.join(folder,mp3)
        if p_mp3[-3:].lower() == 'mp3':
            # l.info(mp3[:-3])
            d = readtag(p_mp3)
            singer = str(d[0])
            title = str(d[1])
            songname = singer+' - '+title+'.mp3'
            if mp3 != songname:
                ml.info(f'Change {mp3} ---> {songname}')
                src = p_mp3
                dst = os.path.join(folder,songname)
                ml.dbg(src)
                ml.dbg(dst)
                os.rename(src,dst)


def archive_cd(evadir,archdir):
    '''Archive album core function'''
    ml = mylogger(logfile)     
    for dirname in os.listdir(evadir):  
        al_src = os.path.join(evadir, dirname)             
        if os.path.isdir(al_src):
            ml.dbg(al_src)
            m = re.split('\s\-\s\d{4}\s\-\s',str(dirname))
            if len(m) == 2: #find album
                pic_src = os.path.join(evadir,dirname,dirname+'.jpg')
                ml.dbg('Cover from '+pic_src)
                pic_dst = os.path.join(evadir,dirname+'.jpg')
                ml.dbg('Cover to '+pic_dst)
                if os.path.exists(pic_dst) == False: 
                    shutil.copyfile(pic_src,pic_dst) 
                ml.info('Searching Artist: '+m[0])
                p_art = find_art(m[0],inventory)
                ml.dbg(p_art)
                if os.path.isdir(p_art):
                    # l.info(p_art)
                    ml.info('Archive '+dirname)
                    al_dst = p_art
                    ml.dbg(al_dst)                                
                elif os.path.isdir(os.path.join(evadir, m[0])):
                    ml.warn('Already prearchive -> move album '+dirname)
                    al_dst = os.path.join(evadir,m[0])
                else:
                    ml.warn('Prearchive '+m[0]+' -> move album '+dirname)
                    os.mkdir(os.path.join(evadir, m[0]))
                    al_dst = os.path.join(evadir, m[0])
                result = myfs.d_move(al_src,al_dst)
                ml.info(result)
                if os.path.isdir(os.path.join(al_dst,m[0])): 
                    ml.info("Archive complete") 


def move_mp3(topdir,musicure):
    '''Move MP3 from Topfolder to Musicure'''
    ml = mylogger(logfile,get_funcname())    
    for mp3 in os.listdir(topdir):
        if mp3[-3:].lower() == 'mp3':
            ml.info('Move --> '+mp3)
            src = os.path.join(topdir,mp3)
            dst = os.path.join(musicure,mp3)
            ml.dbg(f'{src} --> {dst}')
            shutil.move(src,dst)


def move_cover(evadir,coverdir):
    '''Move Cover to CoverFolder'''
    ml = mylogger(logfile,get_funcname())        
    for jpg in os.listdir(evadir):
        if jpg[-3:].lower() == 'jpg':
            ml.info('Move --> '+jpg)
            src = os.path.join(evadir,jpg)
            dst = os.path.join(coverdir,jpg)
            ml.info(f'{src} --> {dst}')
            shutil.move(src,dst)


def arch_cover(coverdir):
    '''move Cover to a-z, manuel check others'''
    ml = mylogger(logfile,get_funcname())
    for c in os.listdir(coverdir):
        src = os.path.join(coverdir,c)
        if os.path.isdir(src) == False:
            dd = os.path.join(coverdir,c[0])     
            if os.path.isdir(dd) == True:
                dst = os.path.join(dd,c)
                result = myfs.f_move(src,dst)
                ml.info(result)          


def evaluate_art(evadir,musicure):
    '''Evaluate Artist in temp evadir'''
    ml = mylogger(logfile,get_funcname())
    for art in os.listdir(evadir):
        if os.path.isdir(os.path.join(evadir,art)):
            ml.info('='*20)
            ml.warn(art)
            n = 0
            for dirpath, dirnames, files in os.walk(musicure):
                for name in files:
                    #bug name contain -
                    if str(name).split('-')[0].strip() == art:
                        ml.info(name)
                        n += 1
            if n == 0:    
                ml.warn('Zero !!! Track ---> Move to misc')
            else:
                albumnumber = len(os.listdir(os.path.join(evadir,art)))
                rate = str(n/albumnumber)[:4]                
                if float(rate) < 0.5:
                    ml.warn(f'Rate {rate} from {str(albumnumber)} Album --> One more CD to evaluate ')
                else:           
                    ml.info(f'Rate {rate} from {str(albumnumber)} Album --> Total {str(n)} Tracks') 


def create_folder(workfolder,albumdir):
    '''Create Album folder and switch to album folder'''
    # albumdir = aDict['fullname']
    ml = mylogger(__name__,logfile)
    ml.info('Create folder: '+albumdir)
    os.chdir(workfolder)
    albumfulldir = os.path.join(workfolder,albumdir)
    if not os.path.exists(albumfulldir):
        os.makedirs(albumfulldir)
    else:
        ml.warn('---- Album folder already exists !')
    os.chdir(albumfulldir)
    return albumfulldir


def find_album(album,match=True):
    '''Find Album in list'''
    with open(albumlist,'r',encoding='utf-8') as f:   
        if match == True:     
            for i in f.readlines():
                if album == i.strip():
                    return True
        else:
            for i in f.readlines():
                if album.upper() in i.strip().upper():
                    return i.strip()
    return False  


def compare_mp3folder():
    question = r'L:\Music\_Jazz\cc.txt'
    target = r'N:\MusiCure\t.txt'
    with open(target,'r') as t:
        tdict = { x.strip().split('\\')[-1]:x.strip() for x in t.readlines()} 
    with open(question,'r') as q:
        for x in q.readlines():
            s = x.strip().split('\\')[-1]
            if s in tdict.keys():
                print(x.strip())
                # print(tdict[s])
                # print(f_move(x.strip(),adict[a]))


def main():
    ml = mylogger(logfile,get_funcname()) 
    parser = argparse.ArgumentParser(description = 'Archive music tool')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a',action="store_true", help='Archive CD')
    group.add_argument('-e',action="store_true", help='Evaluate artist')
    group.add_argument('-r',action="store_true", help='Rename MP3')
    group.add_argument('-m',action="store_true", help='Move MP3')
    group.add_argument('-f',action="store_true", help='Find Artist')
    group.add_argument('-i',action="store_true", help='Update inventory and archive cover')
    args = parser.parse_args()

    if args.a :
        ml.info('Archive CD')
        build_inventory(inventory,archdir)
        archive_cd(evadir,archdir)
        move_cover(evadir,coverdir)
        build_albumlist(albumlist,coverdir)


    elif args.i:
        arch_cover(coverdir)
        build_inventory(inventory,archdir)
        build_albumlist(albumlist,coverdir)
        ml.info('Update Inventory Finish')  

    elif args.e:
        ml.info('Evaluate artist')
        evaluate_art(evadir,musicure)

    elif args.r:
        ml.info('Rename MP3')
        rename_mp3()

    elif args.m:
        ml.info('Move MP3')
        move_mp3(topdir,musicure)

    elif args.f:
        artist = input("Find Artist:  ")
        path = find_art(artist,inventory,match=False)
        for p in path:
            ml.info(p)

    else:
        parser.print_help()


if __name__ == "__main__":
    # if os.path.exists(logfile):
    #     os.remove(logfile)
    try:
        main()
    except KeyboardInterrupt:
        print('ctrl + c')