#!/usr/bin/python3
#coding:utf-8
#version: 20190729
# tested in win

import os
import fnmatch
import shutil
import configparser
import re
from PIL import Image

# customized module
from mylog import get_funcname,mylogger

if os.path.exists(r'L:\MUSIC\xd.ini'):  
    confile = r'L:\MUSIC\xd.ini'
else:
    confile = r'E:\MUSIC\xd.ini'
        
config = configparser.ConfigParser()
config.read(confile)
topdir = config['arch']['topdir']
archdir = config['arch']['archdir']
dldir = config['arch']['dldir']
evadir = config['arch']['evadir']
coverdir = config['arch']['coverdir']
musicure = config['arch']['musicure']
inventory =  config['arch']['inventory']
albumlist =  config['arch']['albumlist']
db =  config['arch']['db']
logfile = config['log']['logfile']
# logfilelevel = int(config['log']['logfilelevel'])


# def modstr(text):
#     # base on version 20181127
#     l = mylogger(logfile,get_funcname()) 
#     #file_name = re.sub(r'\s*:\s*', u' - ', file_name)    # for FAT file system
#     text = str(text)    
#     before = text
    
#     text = text.replace('?', u'？')      # for FAT file system
#     text = text.replace('/', u'／')
#     text = text.replace('|', '')
#     text = text.replace(':', u'∶')    # for FAT file system
#     text = text.replace('*', u'×')
#     text = text.replace('&amp;', u'&')
#     text = text.replace('&#039;', u'\'')
#     #text = text.replace('\'', u'＇')
#     text = text.replace('\\', u'＼')
#     text = text.replace('"', u'＂')
#     #text = text.replace('\'', u'＇')
#     text = text.strip()
#     #file_name = file_name.replace('$', '\\$')    # for command, see issue #7
#     after = text
#     if before != after :
#         l.debug("Before modify: "+before)
#         l.debug("After modify: "+after)
#     return text


def create_folder(workfolder,albumdir):
    '''Create Album folder'''
    ml = mylogger(logfile,get_funcname()) 
    # albumdir = aDict['fullname']
    ml.info('Create folder: '+albumdir)
    os.chdir(workfolder)
    albumfulldir = os.path.join(workfolder,albumdir)
    if not os.path.exists(albumfulldir):
        os.makedirs(albumfulldir)
    else:
        ml.warning('---- Album folder already exists !')
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


if __name__=='__main__':
    text1 = 'ル・デ'
    modstr(text1)
    print(text1)

