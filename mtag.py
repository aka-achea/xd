#!/usr/bin/python3
#coding:utf-8
# tested in win

__version__ = 20200322

from mutagen.mp3 import MP3
from mutagen.id3 import ID3,TIT2,TALB,TPE1,TPE2,COMM,USLT,TCOM,TCON,TPOS,TDRC,TRCK,APIC,ID3NoHeaderError

# customized module
from mylog import mylogger,get_funcname
from config import logfile



def addtag(fname,m_song,m_album,m_artist,m_singer,
            m_cover,m_year='',m_trackid='',m_cd=''):
    '''Add Tag for MP3'''
    ml = mylogger(logfile,get_funcname()) 
    try:
        tags = ID3(fname)
    except ID3NoHeaderError:
        ml.dbg("Adding ID3 header on " + m_trackid)
        tags = ID3()
    tags["TIT2"] = TIT2(encoding=3, text=m_song)
    tags["TALB"] = TALB(encoding=3, text=m_album)
    tags["TPE2"] = TPE2(encoding=3, text=m_artist) #album artist
    #tags["COMM"] = COMM(encoding=3, lang=u'eng', desc='desc', text=u'mutagen comment')
    tags["TPE1"] = TPE1(encoding=3, text=m_singer) # singer
    #tags["TCOM"] = TCOM(encoding=3, text=u'mutagen Composer')
    #tags["TCON"] = TCON(encoding=3, text=u'mutagen Genre')
    tags["TDRC"] = TDRC(encoding=3, text=m_year)
    tags["TRCK"] = TRCK(encoding=3, text=str(m_trackid))
    tags["TPOS"] = TPOS(encoding=3, text=m_cd)
    if m_cover != '':
        with open(m_cover,'rb') as c:
                cover = c.read()  #prepare for tag
        tags["APIC"] = APIC(encoding=3, mime=u'image/png',type=3,desc=u'Cover',data=cover)
    tags.save(fname,v2_version=3)


def addcover(fname,m_cover):
    '''Add cover image to MP3'''
    l = mylogger(logfile,get_funcname()) 
    try:
        tags = ID3(fname)
    except ID3NoHeaderError:
        l.dbg('Adding ID3 header')
        tags = ID3()
    with open(m_cover,'rb') as c:
            cover = c.read()  #prepare for tag
    tags["APIC"] = APIC(encoding=3, mime=u'image/png',type=3,desc=u'Cover',data=cover)
    tags.save(fname,v2_version=3)


def readtag(fname):
    '''Read Tag info from MP3'''
    l = mylogger(logfile,get_funcname()) 
    tags = ID3(fname)
    title =str(tags["TIT2"])
    singer = str(tags['TPE1'])
    l.dbg(singer)
    l.dbg(title)
    return singer,title


if __name__=='__main__':
    fname = '1.mp3'
    m_song = 'song'
    m_album = 'album'
    m_artist = 'singer'
    m_singer = 'singer'    
    m_cover = '1.png'
    addtag(fname,m_song,m_album,m_artist,m_singer,m_cover)
