#!/usr/bin/python3
#coding:utf-8
# tested in win
# version: 20190924

import os
import shutil
import random
import time

# customized module
from openlink import op_requests,ran_header
from qm_ana import ana_album,ana_song
from config import logfile,dldir
from myfs import count_f,clean_f
from mp3archive import create_folder
from mtag import addtag,addcover
from mylog import get_funcname,mylogger
import myget

# quality = {'M500':{'mp3':'99'},
#             'M800':{'mp3':'99'},
#             'F000':{'flac':'99'},
#             'C400':{'m4a':'66'} #999
#             }

quality = { 
    1:['M500','.mp3','66'], # work, 99
    2:['M800','.mp3','53'],
    3:['F000','.flac','99'], 
    4:['C400','.m4a','66'], # work
    5:['A000','.ape','64']            
            }

ref = 'https://y.qq.com'

def get_vkeyguid(songmid,q=1):
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
    req = op_requests(url,header=ran_header(ref=ref),para=para,verify=False)
    # print(req.content)
    j = req.json()
    vkey = j['data']['items'][0]['vkey']
    ml.debug(f'vkey:{vkey}')
    return vkey,guid


def get_dlurl(vkey,guid,songmid,q=1):
    ml = mylogger(logfile,get_funcname()) 
    qly = quality[q][0]
    t = quality[q][1]
    tag = quality[q][2]
    # vkey,guid = get_vkeyguid(songmid)
    # url = 'http://dl.stream.qqmusic.qq.com/%s?vkey=%s&guid=%s&uin=0&fromtag=%s' % (qly+songmid+t,vkey,guid,tag)
    url = f'http://dl.stream.qqmusic.qq.com/{qly+songmid+t}?vkey={vkey}&guid={guid}&uin=0&fromtag={tag}'
    ml.debug(url)
    return url


def qdl_song(weblink,q=1,dlfolder=dldir):
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

# mulitiple discs?
def qdl_album(weblink,q=1,dlfolder=dldir): 
    ml = mylogger(logfile,get_funcname()) 
    aDict = ana_album(weblink)
    m_artist = aDict['artist']
    m_year = aDict['year']
    m_album = aDict['album']
    albumdir = f'{m_artist} - {m_album}'
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
            myget.dl(dlurl,mp3)
            addtag(mp3,m_song,m_album,m_artist,m_singer,m_cover,m_year,m_trackid)   

            # if SongDic == {}:
            #     l.error('Track '+str(s)+' not published')
            # else:
            #     songname = SongDic['singer']+' - '+SongDic['song']
            #     l.info(str(s)+'.'+songname)
            #     mp3 = songname+'.mp3'
            #     l.debug(mp3)
            #     if os.path.isfile(mp3):
            #         l.error('---- Track download already !') 
            #     else:
            #         myget.dl(SongDic['location'],out=mp3) 
            #         print('\n')                         
            #     fname = albumfulldir+'\\'+mp3
            #     m_song = SongDic['song']
            #     m_singer = SongDic['singer']
            #     m_album = aDict['album']
            #     m_artist = aDict['artist']
            #     m_year = aDict['year']
            #     m_trackid = str(s)

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
    



 
