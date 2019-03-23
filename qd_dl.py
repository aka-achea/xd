#!/usr/bin/python3
#coding:utf-8
# tested in win

import os
import shutil
import random
import time

# customized module
from openlink import op_requests
from qd_ana import qd_album,qd_song
from sharemod import logfile,logfilelevel,\
    dldir,count_f,clean_f,create_folder
from mtag import addtag,addcover
from mylog import get_funcname,mylogger
import myget

# logfilelevel = 10 # Debug
# logfile = 'E:\\app.log'

# quality = {'M500':{'mp3':'99'},
#             'M800':{'mp3':'99'},
#             'F000':{'flac':'99'},
#             'C400':{'m4a':'66'} #999
#             }

quality = { 1:['M500','.mp3','66'], # work, 99
            2:['M800','.mp3','53'],
            3:['F000','.flac','99'], 
            4:['C400','.m4a','66'], # work
            5:['A000','.ape','64']            
            }


def get_vkeyguid(songmid,q=1):
    ml = mylogger(logfile,logfilelevel,get_funcname()) 
    guid = int(random.random() * 2147483647) * int(time.time() * 1000) % 10000000000
    url = 'http://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg'
    qly = quality[q][0]
    t = quality[q][1]
    para = {'loginUin':'0',
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
            'guid':guid
            }
    req = op_requests(url,para)
    j = req.json()
    vkey = j['data']['items'][0]['vkey']
    ml.debug(vkey)
    return vkey,guid

def get_dlurl(vkey,guid,songmid,q=1):
    ml = mylogger(logfile,logfilelevel,get_funcname()) 
    qly = quality[q][0]
    t = quality[q][1]
    tag = quality[q][2]
    vkey,guid = get_vkeyguid(songmid)
    # url = 'http://dl.stream.qqmusic.qq.com/%s?vkey=%s&guid=%s&uin=0&fromtag=%s' % (qly+songmid+t,vkey,guid,tag)
    url = f'http://dl.stream.qqmusic.qq.com/{qly+songmid+t}?vkey={vkey}&guid={guid}&uin=0&fromtag={tag}'
    ml.debug(url)
    return url

    # para = {'guid':'6179861260',
    #         'vkey':vkey,
    #         'fromtag':tag
    #         }
    # l.debug(para)
    # content = op_requests(url,para).content
    # with open(mp3,'wb') as f:
    #     f.write(content)
        #f.close()

def dl_song(weblink,q=1,dlfolder=dldir):
    ml = mylogger(logfile,logfilelevel,get_funcname()) 
    sDict = qd_song(weblink)
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

# mulitiple discs?
def dl_album(weblink,q=1,dlfolder = dldir): 
    ml = mylogger(logfile,logfilelevel,get_funcname()) 
    aDict = qd_album(weblink)
    albumdir = create_folder(dlfolder,aDict)
    albumfulldir = os.path.join(dlfolder,albumdir)
    os.chdir(albumfulldir)
    cover = albumdir+'.jpg'
    m_cover = albumdir+'.png'
    if os.path.isfile(cover):
        ml.warning('---- Cover download already !') 
    else:
        myget.dl(aDict['cover'],out=cover)
        shutil.copyfile(cover,m_cover)

    m_artist = aDict['artist']
    m_year = aDict['year']
    m_album = aDict['album']
    
    tracknum = aDict['TrackNum']
    for s in range(1,tracknum+1):
        m_song = aDict[s][1]
        m_singer = m_artist
        mp3 = m_artist+' - '+m_song +quality[q][1]
        m_trackid = str(s) 
        ml.info('Download '+str(s)+'. '+aDict[s][1]) 
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

    c = count_f(albumfulldir)
    if c == int(tracknum) :
        ml.info('Disc Download complete')
        try:
            os.remove(m_cover)
        except FileNotFoundError:
            pass
    else:
        ml.error('Some track download fail')    

    clean_f(albumfulldir)
    ml.info('Download Complete:  '+albumdir)
        
if __name__=='__main__':
    # songmid = '003B7qBz1OKVw4'
    # url = get_dlurl(songmid)
    # myget.dl('a.m4a',url)

    # dl(vkey,songmid,quality['3'][0],quality['3'][1],quality['3'][2])
    # # print(quality['1'][0])

    # page = 'file:///E://1.html'
    # dl_album(page,2)
    alink = 'https://y.qq.com/n/yqq/album/004etZu245Ug8n.html#stat=y_new.song.header.albumname'
    dl_album(alink)

    # weblink = 'https://y.qq.com/n/yqq/song/003lVR2n4O9XtI.html'
    # dl_song(weblink)
