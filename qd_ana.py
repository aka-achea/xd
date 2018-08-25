#!/usr/bin/python
#coding:utf-8
# Python3

from bs4 import BeautifulSoup
from urllib.request import urlopen,Request,HTTPError,unquote
from html.parser import HTMLParser
from modstr import modificate
import re,wget

import mylog as ml
logfilelevel = 10 # Debug
logfile = 'E:\\app.log'

def qd_album(page):
    funcname = 'qd_ana.qd_album'
    l = ml.mylogger(logfile,logfilelevel,funcname)   
    html = urlopen(page)

    bsObj = BeautifulSoup(html,"html.parser") #;print(bsObj)
    album_name = bsObj.find('h1',{'class':'data__name_txt'})
    album_name = modificate(album_name.text)
    l.debug(album_name)

    artist_name = bsObj.find('a',{'class':'js_singer data__singer_txt'})
    artist_name = modificate(artist_name.text)
    l.debug(artist_name)

    year = bsObj.find(text = re.compile('^发行时间'))[5:9]
    l.debug(year)

    cover = bsObj.find('img',{'id':'albumImg'})
    cover = 'http:'+cover.attrs['src']
    l.info(cover)
    wget.download(str(cover),'a.jpg')

    aDict = {'album':album_name,'artist':artist_name,'year':year }

    song = bsObj.findAll('div',{'class':'songlist__number'})
    n = 0
    for i in song:
        n = n+1
        # l.info(i)
        tracknumber = i.text
        l.debug(tracknumber)
        midid = i.next_sibling.next_sibling
        midid = midid.find('span',{'class':'songlist__songname_txt'}).a.attrs['href']
        midid = midid.split('/')[-1][:-5]
        l.debug(midid)
        aDict[int(tracknumber)] = midid

    aDict['TrackNum'] = n
    l.debug(aDict)

    return aDict

def qd_song(page):
    pass


if __name__=='__main__':
    page = 'file:///E://1.html'
    qd_album(page)
