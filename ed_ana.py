#!/usr/bin/python3
#coding:utf-8
# tested in win

from bs4 import BeautifulSoup
from urllib.request import urlopen,Request,HTTPError,unquote
from html.parser import HTMLParser
import re
# from urllib.parse import urlparse


# customized module
from mylog import get_funcname,mylogger
from sharemod import modstr,logfile
from openlink import op_simple , op_requests

def ana_song(weblink):
    ml = mylogger(logfile,get_funcname()) 
    html = op_simple(weblink)[0]
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


def ana_cd(weblink):
    ml = mylogger(logfile,get_funcname()) 
    html = op_simple(weblink)[0]
    bsObj = BeautifulSoup(html,"html.parser") #;print(bsObj)

    albumname = bsObj.findAll('h2',{'class':'f-ff2'}).text
    ml.info(albumname)

    cover = bsObj.find('div',{'class':'cover u-cover u-cover-alb'})
    cover = cover.img.attrs['href']
    ml.info(cover)
     
    artistname = bsObj.find(text='歌手：')
    artistname = artistname.next_siblings.a.text
    ml.info(artistname)

    year = bsObj.find(text='发行时间：').text
    ml.info(year)




if __name__ == "__main__":
    url = 'https://music.163.com/#/song?id=1330348068'    
    sDict = ana_song(url)
    
    # url = 'file:///E://1.html'
    # ana_cd(url)
