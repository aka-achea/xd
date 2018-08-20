#!/usr/bin/python
#coding:utf-8
# Python3

from decry import decry
from modstr import modificate
from bs4 import BeautifulSoup
from openlink import oplink

import mylog as ml
logfilelevel = 10 # Debug
logfile = 'E:\\app.log'

def get_location_one(song_id):
    funcname = 'xd_xml.get_location_one'
    l = ml.mylogger(logfile,logfilelevel,funcname)
    url = 'http://www.xiami.com/widget/xml-single/sid/%s'
    url = url.replace('%s', song_id)
    # url = 'file:///E://xml.xml'
    page = oplink(url)
    l.debug(page[1])
    bsObj = BeautifulSoup(page[0],"html.parser") #;print(bsObj)
    location = bsObj.find("location")
    location = str(location)[19:-14]
    if location == '':
        l.debug('Track not published')
        SongDic = {}
    else:           
        l.debug('Raw Location: '+location)
        location = decry(location)
        song = bsObj.find("song_name")
        song = modificate(str(song)[20:-15])
        singer = bsObj.find("artist_name")
        singer = modificate(str(singer)[22:-17])     
        album = bsObj.find("album_name")
        album = modificate(str(album)[21:-16])
        cover = bsObj.find('album_cover')
        cover = 'http:'+str(cover)[22:-17]
        SongDic = {'location':location,'song':song,'cover':cover,\
                    'artist':singer,'singer':singer,'album':album}
        l.debug(SongDic)
    return SongDic


def get_location_album(song_id):
    funcname = 'xd_xml.get_location_album'
    l = ml.mylogger(logfile,logfilelevel,funcname)
    url = 'http://www.xiami.com/widget/xml-single/sid/%s'
    url = url.replace('%s', song_id)
    # url = 'file:///E://xml.xml'
    page = oplink(url)
    l.debug(page[1])
    bsObj = BeautifulSoup(page[0],"html.parser") #;print(bsObj)
    location = bsObj.find("location")
    location = str(location)[19:-14] 
    if location == '':
        l.debug('Track not published')
        SongDic = {}
    else:           
        l.debug('Raw Location: '+location)
        location = decry(location)
        song = bsObj.find("song_name")
        song = modificate(str(song)[20:-15])
        singer = bsObj.find("artist_name")
        singer = modificate(str(singer)[22:-17])     
        SongDic = {'location':location,'song':song,'singer':singer}
        l.debug(SongDic)
    return SongDic


if __name__=='__main__':
     
    song_id = str(1804018687)
    d = get_location_one(song_id)    
    d = get_location_album(song_id)
    