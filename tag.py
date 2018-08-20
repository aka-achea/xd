#!/usr/bin/python
#coding:utf-8
# Python3

from mutagen.mp3 import MP3
from mutagen.id3 import ID3NoHeaderError, error # really need error?
from mutagen.id3 import ID3,TIT2,TALB,TPE1,TPE2,COMM,USLT,TCOM,TCON,TPOS,TDRC,TRCK,APIC

import mylog as ml
logfilelevel = 10 # Debug
logfile = 'E:\\app.log'
 

def addtag(fname,m_song,m_album,m_artist,m_singer,\
           m_cover,m_year='',m_trackid='',m_cd=''):
    l = ml.mylogger(logfile,logfilelevel,addtag.__name__) 
    try:
        tags = ID3(fname)
    except ID3NoHeaderError:
        l.debug("Adding ID3 header on " + m_trackid)
        tags = ID3()
    tags["TIT2"] = TIT2(encoding=3, text=m_song)
    tags["TALB"] = TALB(encoding=3, text=m_album)
    tags["TPE2"] = TPE2(encoding=3, text=m_artist) #album artist
    #tags["COMM"] = COMM(encoding=3, lang=u'eng', desc='desc', text=u'mutagen comment')
    tags["TPE1"] = TPE1(encoding=3, text=m_singer) # singer
    #tags["TCOM"] = TCOM(encoding=3, text=u'mutagen Composer')
    #tags["TCON"] = TCON(encoding=3, text=u'mutagen Genre')
    tags["TDRC"] = TDRC(encoding=3, text=m_year)
    tags["TRCK"] = TRCK(encoding=3, text=m_trackid)
    tags["TPOS"] = TPOS(encoding=3, text=m_cd)
    with open(m_cover,'rb') as c:
            cover = c.read()  #prepare for tag
    tags["APIC"] = APIC(encoding=3, mime=u'image/png',type=3,desc=u'Cover',data=cover)
    tags.save(fname,v2_version=3)

if __name__=='__main__':
    fname = '1.mp3'
    m_song = 'song'
    m_album = 'album'
    m_artist = 'singer'
    m_singer = 'singer'    
    m_cover = '1.png'
    addtag(fname,m_song,m_album,m_artist,m_singer,m_cover)
