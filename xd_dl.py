#!/usr/bin/python
#coding:utf-8
# Python3



# from html.parser import HTMLParser

import wget,os,time
from xd_ana import ana_cd
from xd_xml import get_location_one, get_location_album
from comm import create_folder, clean_f,count_f
from tag import addtag
import mylog as ml

logfilelevel = 10 # Debug
logfile = 'E:\\app.log'

workfolder = 'F:\\XM'


def dl_one(weburl): 
    funcname = 'xd_dl.dl_one'
    l = ml.mylogger(logfile,logfilelevel,funcname)  
    songid = str(weburl.split('/')[-1])
    l.debug(songid)
    os.chdir(workfolder)
    SongDic = get_location_one(songid)
    songname = SongDic['artist']+' - '+SongDic['song']
    l.info(songname)
    mp3 = songname+'.mp3'
    m_cover = songname+'.png'
    if os.path.isfile(mp3):
        l.warning("Track download already")
    else:
        wget.download(SongDic['location'],out=mp3)
    if os.path.isfile(m_cover): 
        pass
    else:
        wget.download(SongDic['cover'],out=m_cover)
    fname = mp3
    m_song = SongDic['song']
    m_album = SongDic['album']
    m_artist = SongDic['artist']
    m_singer = SongDic['singer']  
    addtag(fname,m_song,m_album,m_artist,m_singer,m_cover)
    os.remove(m_cover)
    

def dl_album(web):
    funcname = 'xd_dl.dl_album'
    l = ml.mylogger(logfile,logfilelevel,funcname) 
    aDict = ana_cd(web)
    albumdir = create_folder(workfolder,aDict)
    albumfulldir = workfolder +"\\"+albumdir
    l.debug(albumfulldir)
    os.chdir(albumfulldir)
    # download cover
    m_cover = albumdir+'.png'
    l.debug(m_cover)    
    if os.path.isfile(m_cover):
        l.warning('---- Small cover download already !') 
    else:
        l.info('Download small cover')
        wget.download(aDict['scover'],out=m_cover)
        print('\n') 
    cover = albumdir+'.jpg'
    if os.path.isfile(cover):
        l.warning('---- Big Cover download already !') 
    else:
        l.info('Download big cover')
        wget.download(aDict['bcover'],out=cover)
        print('\n') 

    for i in range(aDict['Discs']):
        CD = str(i+1)
        tracknum = aDict[CD]
        for t in range(tracknum):
            if t < 10: t = '0'+str(t+1)
            songid = aDict[CD,t]
            l.debug('Download Disc '+str(CD)+' track '+str(t)+' id '+songid)
            SongDic = get_location_album(songid)
            if SongDic == {}:
                l.error('Disc '+str(CD)+' track '+str(t)+' not published')
            else:
                songname = SongDic['singer']+' - '+SongDic['song']
                l.info(str(CD)+'.'+str(t)+'.'+songname)
                mp3 = songname+'.mp3'
                l.debug(mp3)
                if os.path.isfile(mp3):
                    l.warning('---- Track download already !') 
                else:
                    try:
                        wget.download(SongDic['location'],out=mp3) 
                        print('\n')   
                    except urllib.error.ContentTooShortError:
                        l.error("Content incomplete -> retry")
                        wget.download(SongDic['location'],out=mp3) 
                        print('\n')
                fname = albumfulldir+'\\'+mp3
                m_song = SongDic['song']
                m_singer = SongDic['singer']
                m_album = aDict['album']
                m_artist = aDict['artist']
                m_year = aDict['year']
                m_cd = str(CD)
                m_trackid = str(t)
                addtag(fname,m_song,m_album,m_artist,m_singer,m_cover,\
                        m_year,m_trackid,m_cd) 
        c = count_f(albumfulldir)
        if c == int(tracknum) :
            l.info('Disc '+CD+' Download complete')
        else:
            l.error('Some track download fail')

    clean_f(albumfulldir)



if __name__=='__main__':
    # dl_one('https://www.xiami.com/song/1776199944')

    web = 'file:///E://1.html'
    dl_album(web)
    

    