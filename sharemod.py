#!/usr/bin/python3
#coding:utf-8
# tested in win

import os, fnmatch, shutil,configparser

# customized module
from mylog import get_funcname,mylogger

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
logfile = config['log']['logfile']
logfilelevel = int(config['log']['logfilelevel'])


def modstr(text):
    # base on version 20181127
    l = mylogger(logfile,logfilelevel,get_funcname()) 
    #file_name = re.sub(r'\s*:\s*', u' - ', file_name)    # for FAT file system
    text = str(text)    
    before = text
    text = text.replace('?', u'？')      # for FAT file system
    text = text.replace('/', u'／')
    text = text.replace('|', '')
    text = text.replace(':', u'∶')    # for FAT file system
    text = text.replace('*', u'×')
    text = text.replace('&amp;', u'&')
    text = text.replace('&#039;', u'\'')
    #text = text.replace('\'', u'＇')
    text = text.replace('\\', u'＼')
    text = text.replace('"', u'＂')
    #text = text.replace('\'', u'＇')
    text = text.strip()
    #file_name = file_name.replace('$', '\\$')    # for command, see issue #7
    after = text
    if before != after :
        l.debug("Before modify: "+before)
        l.debug("After modify: "+after)
    return text

def create_folder(workfolder,aDict):
    l = mylogger(logfile,logfilelevel,get_funcname()) 
    album = aDict['album']
    artist = aDict['artist']
    year = aDict['year']
    albumdir = artist+' - '+year+' - '+album
    l.info('Create folder: '+albumdir)
    os.chdir(workfolder)
    albumfulldir = os.path.join(workfolder,albumdir)
    if not os.path.exists(albumfulldir):
        os.makedirs(albumfulldir)
        os.chdir(albumfulldir)
    else:
        l.warning('---- Album folder already exists !')
        os.chdir(albumfulldir)
    return albumdir

def clean_f(path):
    for f in os.listdir(path):
        if fnmatch.fnmatch(f,'*.tmp'):
            os.remove(f)

def count_f(path):
    c = 0
    for f in os.listdir(path):        
        if fnmatch.fnmatch(f,'*.mp3'): c += 1
    return c
                
def f_move(src,dst): # fs version: 20181230
    l = mylogger(logfile,logfilelevel,get_funcname()) 
    if os.path.exists(dst):
        print(dst)
        print('DST: '+str(os.path.getsize(dst)))
        print('SRC: '+str(os.path.getsize(src)))
        if os.path.getsize(dst) < os.path.getsize(src):
            l.warning('Replace small one')
            os.remove(dst)
            shutil.move(src,dst)
        else:
            l.warning("Already have big one")
            os.remove(src)
    else:
        shutil.move(src,dst)


if __name__=='__main__':
    text1 = 'ル・デ'
    modstr(text1)
    print(text1)

