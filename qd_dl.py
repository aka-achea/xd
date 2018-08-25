#!/usr/bin/python
#coding:utf-8
# Python3

import os
from openlink import oprqs
from qd_ana import qd_album
from comm import create_folder

import mylog as ml
logfilelevel = 10 # Debug
logfile = 'E:\\app.log'

# quantity = {'M500':{'mp3':'99'},
#             'M800':{'mp3':'99'},
#             'F000':{'flac':'99'},
#             'C400':{'m4a':'66'} #999
#             }

quantity = {'1':['M500','.mp3','99'],
            '2':['M800','.mp3','99'],
            '3':['F000','.flac','99'],
            '4':['C400','m4a','66'],
            '5':['A000','.ape']            
            }


workfolder  = 'e:\\'
path = 'e:\\'

def get_vkey(songmid):
    funcname = 'qd_dl.get_vkey'
    l = ml.mylogger(logfile,logfilelevel,funcname) 
    url = 'http://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg'
    para = {'loginUin':'0',
            'hostUin':'0',
            'format':'json',
            'inCharset':'utf8',
            'outCharset':'utf-8',
            'notice':'0',
            'platform':'yqq',
            'needNewCode':'0',
            'cid':'205361747', #important 205361747
            'uin':'0',
            'songmid':str(songmid),
            'filename':'C400'+str(songmid)+'.m4a',
            'guid':'6179861260' #504753841
            }
    #guid 6179861260
    req = oprqs(url,para)
    j = req.json()
    vkey = j['data']['items'][0]['vkey']
    l.debug(vkey)
    return vkey

def dl_song(vkey,songmid,q='C400',t='.m4a',tag='66'):
    funcname = 'qd_dl.dl'
    l = ml.mylogger(logfile,logfilelevel,funcname) 
    url = 'http://dl.stream.qqmusic.qq.com/'+q+songmid+t
    l.debug(url)
    para = {'guid':'6179861260',
            'vkey':vkey,
            'fromtag':tag
            }
    l.debug(para)
    mp3 = path+q+songmid+t
    l.debug(mp3)
    content = oprqs(url,para).content
    with open(mp3,'wb') as f:
        f.write(content)
        f.close()


def dl_album(web):
    funcname = 'qd_dl.dl_album'
    l = ml.mylogger(logfile,logfilelevel,funcname)  

    aDict = qd_album(page)
    albumdir = create_folder(workfolder,aDict)
    os.chdir(albumdir)
    for s in range(1,aDict['TrackNum']+1):
            songmid = aDict[s]
            l.debug('Download track number '+str(s)+' id '+aDict[s]) 
            vkey = get_vkey(songmid)
            dl_song(vkey,songmid,quantity['1'][0],quantity['1'][1],quantity['1'][2])


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
            #         wget.download(SongDic['location'],out=mp3) 
            #         print('\n')                         
            #     fname = albumfulldir+'\\'+mp3
            #     m_song = SongDic['song']
            #     m_singer = SongDic['singer']
            #     m_album = aDict['album']
            #     m_artist = aDict['artist']
            #     m_year = aDict['year']
            #     m_trackid = str(s)
            #     addtag(fname,m_song,m_album,m_artist,m_singer,m_cover,\
            #             m_year,m_trackid)   


if __name__=='__main__':
    # songmid = '003B7qBz1OKVw4'
    # vkey = get_vkey(songmid)
    # # vkey = 'segesf'

    # dl(vkey,songmid,quantity['3'][0],quantity['3'][1],quantity['3'][2])
    # # print(quantity['1'][0])


    page = 'file:///E://1.html'
    dl_album(page)
    