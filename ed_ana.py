#!/usr/bin/python3
#coding:utf-8
# tested in win

'''
API reference: 
https://github.com/yanunon/NeteaseCloudMusic/blob/master/NeteaseCloudMusic.py
https://github.com/darknessomi/musicbox/blob/master/NEMbox/encrypt.py
'''


from bs4 import BeautifulSoup
from urllib.request import urlopen,Request,HTTPError,unquote
from html.parser import HTMLParser
import re,pprint,json
# from urllib.parse import urlparse


# customized module
from mylog import get_funcname,mylogger
from sharemod import modstr,logfile
from openlink import op_simple , op_requests,ran_header

# header = {
#     'Cookie': 'appver=1.5.0.75771;',
#     'Referer': 'http://music.163.com/',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
# }


url = 'http://music.163.com/api/album/%d/'

agentref = 'http://music.163.com/'

def ana_song(weblink):
    ml = mylogger(logfile,get_funcname()) 
    html = op_simple(weblink,header)[0]
    # html = op_requests(url,verify=False).content 
    bsObj = BeautifulSoup(html,"html.parser")
    # ml.debug(bsObj)
    # title = bsObj.find('title')
    # print(title)

    song_name = bsObj.find('em',{'class':'f-ff2'})
    songname = modstr(song_name.text.strip())
    ml.info(songname)
    aa = bsObj.findAll('p',{'class':'des s-fc4'})
    artistname = modstr(aa[0].span.a.text)
    albumname = modstr(aa[1].a.text)
    ml.info(artistname)
    ml.info(albumname)

    cover = bsObj.find('div',{'class':'u-cover u-cover-6 f-fl'})
    cover = cover.img.attrs['href']
    ml.info(cover)
    
    songmid = weblink.split('=')[-1]

    sDict = {'artist':artistname,'song_name':songname,'songmid':songmid,'cover':cover }
    ml.debug(sDict)
    return sDict


def ana_cd(albumlink):
    '''Get album JSON data'''
    ml = mylogger(logfile,get_funcname()) 
    # html = op_simple(weblink,header)[0]
    # bsObj = BeautifulSoup(html,"html.parser") #;print(bsObj)

    # with open(r'M:\GH\xd\t.txt','w',encoding='utf-8') as f:
    #     f.writelines(html)
    # albumname = bsObj.findAll('h2',{'class':'f-ff2'})
    # print(albumname)
    # ml.info(albumname)

    # cover = bsObj.find('div',{'class':'cover u-cover u-cover-alb'})
    # cover = cover.img.attrs['href']
    # ml.info(cover)
     
    # artistname = bsObj.find(text='歌手：')
    # artistname = artistname.next_siblings.a
    # ml.info(artistname)

    # year = bsObj.find(text='发行时间：')
    # ml.info(year)

    albumid = albumlink.split('=')[-1]
    # print(albumid)
    url = f'http://music.163.com/api/album/{albumid}/'
    jdata = op_simple(url,ran_header(ref=agentref))[0]
    # pprint.pprint(j)
    # print(type(j))
    return jdata


def ana_json(data):
    '''Analyze Json get album song details'''
    j=json.load(data)
    # pprint.pprint(j)
    adict = {}
    adict['cover'] = j['album']['picUrl']
    adict['number'] = j['album']['size']
    adict['albumname'] = j['album']['name']
    adict['artist'] = j['album']['artist']['name']
    for s in j['album']['songs']:
        sdict = {}
        sdict['id'] = s['id']
        sdict['songname'] = s['name']
        artists = []         
        for x in s['artists']:
            artists.append(x['name'])
        sdict['singer'] = ','.join(artists)
        adict[s['no']] = sdict
    # pprint.pprint(adict)
    return adict




if __name__ == "__main__":
    # url = 'https://music.163.com/#/song?id=1330348068'    
    # sDict = ana_song(url)
    
    # url = 'file:///E://1.html'
    url = 'https://music.163.com/#/album?id=79753582'
    ana_cd(url)

   