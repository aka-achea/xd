#!/usr/bin/python
#coding:utf-8
# Python3

import os

import mylog as ml
logfilelevel = 10 # Debug
logfile = 'E:\\app.log'

def modstr(text):
    funcname = 'comm.modstr'    
    l = ml.mylogger(logfile,logfilelevel,funcname)     
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
    funcname = 'comm.create_folder'
    l = ml.mylogger(logfile,logfilelevel,funcname)
    album = aDict['album']
    artist = aDict['artist']
    year = aDict['year']
    albumdir = artist+' - '+year+' - '+album
    l.info('Create folder: '+albumdir)
    os.chdir(workfolder)
    albumfulldir = workfolder +"\\"+albumdir
    if not os.path.exists(albumfulldir):
        os.makedirs(albumfulldir)
        os.chdir(albumfulldir)
    else:
        l.error('---- Album folder already exists !')
        os.chdir(albumfulldir)
    return albumdir


if __name__=='__main__':
    text1 = 'ル・デ'
    modstr(text1)
    print(text1)
   
   
