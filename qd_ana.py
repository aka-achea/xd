#!/usr/bin/python
#coding:utf-8
# Python3

from bs4 import BeautifulSoup
from urllib.request import urlopen,Request,HTTPError,unquote
from html.parser import HTMLParser
import re

# customized module
from mylog import get_funcname,mylogger
from sharemod import modstr#,logfile,logfilelevel

logfilelevel = 10 # Debug
logfile = 'E:\\app.log'

def qd_album(page): # download web first
    l = mylogger(logfile,logfilelevel,get_funcname()) 
    html = urlopen(page)
    bsObj = BeautifulSoup(html,"html.parser") #;print(bsObj)
    album_name = bsObj.find('h1',{'class':'data__name_txt'})
    album_name = modstr(album_name.text)
    l.debug(album_name)

    artist_name = bsObj.find('a',{'class':'js_singer data__singer_txt'})
    artist_name = modstr(artist_name.text)
    l.debug(artist_name)

    year = bsObj.find(text = re.compile('^发行时间'))[5:9]
    l.debug(year)

    cover = bsObj.find('img',{'id':'albumImg'})
    cover = 'http:'+cover.attrs['src']
    l.debug(cover)
    aDict = {'album':album_name,'artist':artist_name,'year':year,'cover':cover }

    song = bsObj.findAll('div',{'class':'songlist__number'})
    n = 0
    for i in song:
        n = n+1
        tracknumber = i.text
        l.debug(tracknumber)
        si = i.next_sibling.next_sibling
        si = si.find('span',{'class':'songlist__songname_txt'}).a
        songmid = si.attrs['href'].split('/')[-1][:-5]
        songname = si.text
        si = [songmid, songname]
        aDict[int(tracknumber)] = si
    aDict['TrackNum'] = n
    l.debug(aDict)

    return aDict

def qd_song(page):
    pass


if __name__=='__main__':
    page = 'file:///E://1.html'
    qd_album(page)
