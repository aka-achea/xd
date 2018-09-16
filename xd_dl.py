#!/usr/bin/python
#coding:utf-8
# Python3



# from html.parser import HTMLParser

import wget,os,time
from xd_ana import xd_song, xd_album
from xd_xml import get_location_one, get_location_album
from comm import create_folder
from tag import addtag
import mylog as ml

logfilelevel = 10 # Debug
logfile = 'E:\\app.log'

workfolder = 'F:\\XM'


def dl_one(web): 
    funcname = 'xd_dl.dl_one'
    l = ml.mylogger(logfile,logfilelevel,funcname)  
    song_id = xd_song(web)
    l.debug(song_id)
    SongDic = get_location_one(song_id)
    os.chdir(workfolder)
    if SongDic == {}:
        l.error('Track not published')
    else:
        songname = SongDic['singer']+' - '+SongDic['song']
        l.info(songname)
        mp3 = songname+'.mp3'
        m_cover = songname+'.png'
        wget.download(SongDic['location'],out=mp3)
        wget.download(SongDic['cover'],out=m_cover)
        fname = mp3
        m_song = SongDic['song']
        m_album = SongDic['album']
        m_artist = SongDic['artist']
        m_singer = SongDic['singer']  
        addtag(fname,m_song,m_album,m_artist,m_singer,m_cover)

def dl_album(web):
    funcname = 'xd_dl.dl_album'
    l = ml.mylogger(logfile,logfilelevel,funcname) 
    aDict = xd_album(web)
    albumdir = create_folder(workfolder,aDict)
    albumfulldir = workfolder +"\\"+albumdir
    l.debug(albumfulldir)
    os.chdir(albumfulldir)
    # download cover
    m_cover = albumdir+'.png'
    l.debug(m_cover)    
    if os.path.isfile(m_cover):
        l.error('---- Small cover download already !') 
    else:
        l.info('Download small cover')
        wget.download(aDict['scover'],out=m_cover)
        print('\n') 
    cover = albumdir+'.jpg'
    if os.path.isfile(cover):
        l.error('---- Big Cover download already !') 
    else:
        l.info('Download big cover')
        wget.download(aDict['bcover'],out=cover)
        print('\n') 

    if 'Disc' in aDict:  # multi disc
        l.debug(aDict['Disc'])
        c = 1 ; t = 1
        for s in range(aDict['TrackNum']):
            try:
                song_id = (aDict[c,t])    
                l.debug('Download Disc '+str(c)+' track '+str(t)+' id '+aDict[c,t])
                SongDic = get_location_album(song_id)
                if SongDic == {}:
                    l.error('Disc '+str(c)+' track '+str(t)+' not published')
                else:
                    songname = SongDic['singer']+' - '+SongDic['song']
                    l.info(str(c)+'.'+str(t)+'.'+songname)
                    mp3 = songname+'.mp3'
                    l.debug(mp3)
                    if os.path.isfile(mp3):
                        l.error('---- Track download already !') 
                    else:
                        wget.download(SongDic['location'],out=mp3) 
                        print('\n')                         
                    fname = albumfulldir+'\\'+mp3
                    m_song = SongDic['song']
                    m_singer = SongDic['singer']
                    m_album = aDict['album']
                    m_artist = aDict['artist']
                    m_year = aDict['year']
                    m_cd = str(c)
                    m_trackid = str(t)
                    addtag(fname,m_song,m_album,m_artist,m_singer,m_cover,\
                            m_year,m_trackid,m_cd) 
                t = t+1

            except KeyError:
                c = c+1 ; t = 1
                song_id = (aDict[c,t])
                l.debug('Download Disc '+str(c)+' track '+str(t)+' id '+aDict[c,t]) 
                SongDic = get_location_album(song_id)
                if SongDic == {}:
                    l.error('Disc '+str(c)+' track '+str(t)+' not published')
                else:
                    songname = SongDic['singer']+' - '+SongDic['song']
                    l.info(str(c)+'.'+str(t)+'.'+songname)
                    mp3 = songname+'.mp3'
                    l.debug(mp3)
                    if os.path.isfile(mp3):
                        l.error('---- Track download already !') 
                    else:
                        wget.download(SongDic['location'],out=mp3) 
                        print('\n')                         
                    fname = albumfulldir+'\\'+mp3
                    m_song = SongDic['song']
                    m_singer = SongDic['singer']
                    m_album = aDict['album']
                    m_artist = aDict['artist']
                    m_year = aDict['year']
                    m_cd = str(c)
                    m_trackid = str(t)
                    addtag(fname,m_song,m_album,m_artist,m_singer,m_cover,\
                            m_year,m_trackid,m_cd) 
                t = t+1

    else:  # one disc
        for s in range(1,aDict['TrackNum']+1):
            song_id = aDict[s]
            l.debug('Download track number '+str(s)+' id '+aDict[s]) 
            SongDic = get_location_album(song_id)
            if SongDic == {}:
                l.error('Track '+str(s)+' not published')
            else:
                songname = SongDic['singer']+' - '+SongDic['song']
                l.info(str(s)+'.'+songname)
                mp3 = songname+'.mp3'
                l.debug(mp3)
                if os.path.isfile(mp3):
                    l.error('---- Track download already !') 
                    time.sleep(2)
                else:
                    wget.download(SongDic['location'],out=mp3) 
                    print('\n')                         
                fname = albumfulldir+'\\'+mp3
                m_song = SongDic['song']
                m_singer = SongDic['singer']
                m_album = aDict['album']
                m_artist = aDict['artist']
                m_year = aDict['year']
                m_trackid = str(s)
                addtag(fname,m_song,m_album,m_artist,m_singer,m_cover,\
                        m_year,m_trackid)   


if __name__=='__main__':
    # web = 'file:///E://1.html'
    # dl_one(web)

    web = 'file:///E://1.html'
    dl_album(web)
    

    