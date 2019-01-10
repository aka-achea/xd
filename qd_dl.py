#!/usr/bin/python
#coding:utf-8
# Python3

import os,wget,shutil

# customized module
from openlink import op_requests
from qd_ana import qd_album
from sharemod import create_folder,logfile,logfilelevel
from mtag import addtag
from mylog import get_funcname,mylogger


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


workfolder = 'F:\\XM'
# path = 'e:\\'

def get_vkey(songmid):
    l = mylogger(logfile,logfilelevel,get_funcname()) 
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
    req = op_requests(url,para)
    j = req.json()
    vkey = j['data']['items'][0]['vkey']
    l.debug(vkey)
    return vkey

def dl_song(vkey,songmid,mp3,m='4'):
    l = mylogger(logfile,logfilelevel,get_funcname()) 

    q = quantity[m][0]
    t = quantity[m][1]
    tag = quantity[m][2]

    url = 'http://dl.stream.qqmusic.qq.com/'+ q + songmid + t
    l.debug(url)
    para = {'guid':'6179861260',
            'vkey':vkey,
            'fromtag':tag
            }
    l.debug(para)
    content = op_requests(url,para).content
    with open(mp3,'wb') as f:
        f.write(content)
        f.close()


def dl_album(web,m='4'):
    l = mylogger(logfile,logfilelevel,get_funcname()) 
    aDict = qd_album(page)
    albumdir = create_folder(workfolder,aDict)
    albumfulldir = workfolder +"\\"+albumdir
    os.chdir(albumfulldir)
    cover = albumdir+'.jpg'
    m_cover = albumdir+'.png'
    if os.path.isfile(cover):
        l.error('---- Cover download already !') 
    else:
        wget.download(aDict['cover'],out=cover)
        print('\n')  
        shutil.copyfile(cover,m_cover)

    m_artist = aDict['artist']
    m_year = aDict['year']
    m_album = aDict['album']
    

    for s in range(1,aDict['TrackNum']+1):
        mp3 = m_artist+' - '+aDict[s][1]+quantity[m][1]
        m_trackid = s
        
        if os.path.isfile(mp3):
            l.error('---- Track download already !') 
        else:
            songmid = aDict[s][0]
            vkey = get_vkey(songmid)
            l.info('Download '+str(s)+'. '+aDict[s][1]) 
            dl_song(vkey,songmid,mp3,m)
        addtag(mp3,m_artist,m_cover,m_year,m_trackid)   




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
        


if __name__=='__main__':
    # songmid = '003B7qBz1OKVw4'
    # vkey = get_vkey(songmid)
    # # vkey = 'segesf'

    # dl(vkey,songmid,quantity['3'][0],quantity['3'][1],quantity['3'][2])
    # # print(quantity['1'][0])


    page = 'file:///E://1.html'
    dl_album(page,'1')
    