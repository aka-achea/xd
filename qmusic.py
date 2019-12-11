#!/usr/bin/python3
#coding:utf-8
# tested in win
__version__ = 20191125

import os
import shutil
import random
import time
import re
from bs4 import BeautifulSoup
from urllib.request import HTTPError
from html.parser import HTMLParser


# customized module
from openlink import op_requests,ran_header,op_simple
from config import logfile,dldir
from mp3archive import create_folder
from mtag import addtag,addcover
from myfs import count_f,clean_f
from mylog import get_funcname,mylogger
from mystr import fnamechecker as modstr
import myget
from mytool import mywait


quality = { 
    1:['M500','.mp3','66'], # work, 99
    2:['M800','.mp3','53'], # work, 99
    3:['F000','.flac','99'], 
    4:['C400','.m4a','66'], # work 999
    5:['A000','.ape','64']            
            }

ref = 'https://y.qq.com'
header = ran_header(ref=ref)


def get_vkeyguid(songmid,q=1):
    '''Get vkey and guid from songid'''
    ml = mylogger(logfile,get_funcname()) 
    guid = int(random.random()*2147483647)*int(time.time()*1000) % 10000000000
    ml.debug(f'GUID:{guid}')
    url = 'http://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg'
    qly = quality[q][0]
    t = quality[q][1]
    para = {
            'loginUin':'0',
            'hostUin':'0',
            'format':'json',
            'inCharset':'utf8',
            'outCharset':'utf-8',
            'notice':'0',
            'platform':'yqq',
            'needNewCode':'0',
            'cid':'205361747', #important 
            'uin':'0',
            'songmid':str(songmid),
            'filename':qly+str(songmid)+t,
            'guid':str(guid)
            }
    req = op_requests(url,header=header,para=para,verify=False)
    # print(req.content)
    j = req.json()
    vkey = j['data']['items'][0]['vkey']
    ml.debug(f'vkey:{vkey}')
    return vkey,guid


def get_dlurl(vkey,guid,songmid,q=1):
    '''Get mp3 download link'''
    ml = mylogger(logfile,get_funcname()) 
    qly = quality[q][0]
    t = quality[q][1]
    tag = quality[q][2]
    # vkey,guid = get_vkeyguid(songmid)
    # url = 'http://dl.stream.qqmusic.qq.com/%s?vkey=%s&guid=%s&uin=0&fromtag=%s' % (qly+songmid+t,vkey,guid,tag)
    url = f'http://dl.stream.qqmusic.qq.com/{qly+songmid+t}?vkey={vkey}&guid={guid}&uin=0&fromtag={tag}'
    ml.debug(url)
    return url


def ana_song(weblink):
    '''Analyze song page return song dictionary'''
    ml = mylogger(logfile,get_funcname()) 
    songmid = weblink.split('/')[-1]
    songmid = songmid.split('.')[0]
    ml.debug(songmid)
    html = op_simple(weblink)[0]
    bsObj = BeautifulSoup(html,"html.parser")

    artist_name = bsObj.find('div',{'class':'data__singer'})
    artist_name = artist_name.attrs['title']
    ml.debug(artist_name)

    song_name = bsObj.find('h1',{'class':'data__name_txt'})
    song_name = modstr(song_name.text.strip())
    ml.debug(song_name)

    cover = bsObj.find('img',{'class':'data__photo'})
    cover = 'http:'+cover.attrs['src']
    ml.debug('Cover link: '+cover)
    sDict = {'artist':artist_name,'song_name':song_name,
            'songmid':songmid,'cover':cover }
    ml.debug(sDict)
    return sDict


def qdl_song(weblink,q=1,dlfolder=dldir):
    '''Download Single song'''
    ml = mylogger(logfile,get_funcname()) 
    sDict = ana_song(weblink)
    songmid = sDict['songmid']
    vkey,guid = get_vkeyguid(songmid,q)
    dlurl = get_dlurl(vkey,guid,songmid,q)
    os.chdir(dldir)
    mp3 = sDict['artist']+' - '+sDict['song_name']+quality[q][1]
    fullmp3path = os.path.join(dldir,mp3)
    ml.debug(fullmp3path)
    ml.info(f"Download {sDict['artist']} - {sDict['song_name']}")
    myget.dl(dlurl,fullmp3path)
    fullcoverpath = os.path.join(dldir,'cover.png')
    myget.dl(sDict['cover'],fullcoverpath,pbar=None)
    addcover(mp3,fullcoverpath)   
    os.remove(fullcoverpath)
    # tag contained already


def ana_album(weblink): 
    '''Analyze QQ Music web page return album dict with song'''
    ml = mylogger(logfile,get_funcname()) 
    html = op_simple(weblink,header=header)[0]
    bsObj = BeautifulSoup(html,"html.parser") #;print(bsObj)
    album_name = bsObj.find('h1',{'class':'data__name_txt'})
    album_name = modstr(album_name.text)
    ml.debug(album_name)
    artist_name = bsObj.find('a',{'class':'js_singer data__singer_txt'})
    artist_name = modstr(artist_name.text)
    ml.debug(artist_name)
    year = bsObj.find(text = re.compile('^发行时间'))[5:9]
    ml.debug(year)
    cover = bsObj.find('img',{'id':'albumImg'})
    cover = 'http:'+cover.attrs['src']
    ml.debug('Cover link: '+cover)
    fullname = artist_name+' - '+year+' - '+album_name
    aDict = {'album':album_name,'artist':artist_name,'year':year,'cover':cover,'fullname':fullname }
    songs = bsObj.findAll('div',{'class':'songlist__number'})
    n = 0
    songtmp = [] # name duplicate check
    for i in songs:
        n += 1
        tracknumber = i.text
        ml.debug('Find track '+str(tracknumber))
        tmp = i.next_sibling.next_sibling
        si = tmp.find('span',{'class':'songlist__songname_txt'}).a
        songmid = si.attrs['href'].split('/')[-1][:-5]
        songname = si.text
        if songname in songtmp:
            songname = songname+'_'+tracknumber
        songtmp.append(songname)    
        ml.debug(songname)
        singers = tmp.parent.findAll('a',{'class':"singer_name"})
        if len(singers) > 1:
            s = list(map(lambda x:x.text , singers ))
            singer = ','.join(s) 
        else:
            singer = singers[0].text
        ml.debug(singer)
        si = [songmid,songname,singer]
        aDict[int(tracknumber)] = si
    aDict['TrackNum'] = n
    # ml.info(aDict)
    return aDict  # Album dictionary


# mulitiple discs?
def qdl_album(weblink,q=1,dlfolder=dldir): 
    '''QQ Music download'''
    ml = mylogger(logfile,get_funcname()) 
    aDict = ana_album(weblink)
    m_artist = aDict['artist']
    m_year = aDict['year']
    m_album = aDict['album']
    albumdir = f'{m_artist} - {m_year} - {m_album}'
    albumfulldir = create_folder(dlfolder,albumdir)
    cover = albumdir+'.jpg'
    m_cover = albumdir+'.png'
    if os.path.isfile(cover):
        ml.warning('---- Cover download already !') 
    else:
        myget.dl(aDict['cover'],out=cover)
        shutil.copyfile(cover,m_cover)
    
    tracknum = aDict['TrackNum']
    for s in range(1,tracknum+1):
        m_song = aDict[s][1]
        m_singer = aDict[s][2]
        mp3 = m_singer+' - '+m_song +quality[q][1]
        m_trackid = str(s) 
        ml.info(f'{str(s)}.{aDict[s][1]}') 
        if os.path.isfile(mp3):
            ml.warning('---- Track download already !') 
        else:
            songmid = aDict[s][0]
            vkey,guid = get_vkeyguid(songmid,q)
            dlurl = get_dlurl(vkey,guid,songmid,q)
            try:
                myget.dl(dlurl,mp3)
                addtag(mp3,m_song,m_album,m_artist,m_singer,m_cover,m_year,m_trackid)   
            except HTTPError as e:
                if '403' in str(e):
                    ml.error('Track download forbidden')
                else:
                    raise
            except ConnectionResetError as e:
                mywait(10)
                qdl_album(weblink,q=1,dlfolder=dldir)
    if count_f(albumfulldir,'mp3') == int(tracknum) :
        ml.info('Disc Download complete')
        try:
            os.remove(m_cover)
        except FileNotFoundError:
            pass
    else:
        ml.error('Some track download fail')    
    clean_f(albumfulldir,'tmp')
    ml.info('Download Complete:  '+albumdir)


def main():
    if os.path.exists(logfile):
        os.remove(logfile)
    while True:
        try:
            qdl_album(input('Link>>'),1)
        except KeyboardInterrupt:
            print('ctrl + c')  
            break  


if __name__=='__main__':
    main()



    # test get_vkeyguid,get_dlurl
    # songmid = '001e2BMO1ERkjz'
    # vkey,guid = get_vkeyguid(songmid)
    # url = get_dlurl(vkey,guid,songmid)
    # print(url)
    # myget.dl(url)


    # test qdl_song
    # weblink = 'https://y.qq.com/n/yqq/song/003lVR2n4O9XtI.html'
    # qdl_song(weblink)

    # test qdl_album
    # page = 'file:///E://1.html'
    # page = 'https://y.qq.com/n/yqq/album/0012smzU0w03JD.html'
    



 
