#!/usr/bin/python3
#coding:utf-8
# tested in win

from bs4 import BeautifulSoup
from urllib.request import urlopen,Request,HTTPError,unquote
from html.parser import HTMLParser
import re

# customized module
from mylog import get_funcname,mylogger
from sharemod import modstr,logfile,logfilelevel
from openlink import op_simple

# logfilelevel = 10 # Debug
# logfile = 'E:\\app.log'

def qd_album(weblink): 
    l = mylogger(logfile,logfilelevel,get_funcname()) 
    html = op_simple(weblink)[0]
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
    l.debug('Cover link: '+cover)
    aDict = {'album':album_name,'artist':artist_name,'year':year,'cover':cover }

    song = bsObj.findAll('div',{'class':'songlist__number'})
    n = 0
    for i in song:
        n += 1
        tracknumber = i.text
        l.debug('Find track '+str(tracknumber))
        si = i.next_sibling.next_sibling
        si = si.find('span',{'class':'songlist__songname_txt'}).a
        songmid = si.attrs['href'].split('/')[-1][:-5]
        songname = si.text
        si = [songmid, songname]
        aDict[int(tracknumber)] = si
    aDict['TrackNum'] = n
    l.debug(aDict)
    return aDict  # Album dictionary

def qd_song(weblink): # return song dictionary
    l = mylogger(logfile,logfilelevel,get_funcname()) 
    songmid = weblink.split('/')[-1]
    songmid = songmid.split('.')[0]
    l.debug(songmid)
    html = op_simple(weblink)[0]
    bsObj = BeautifulSoup(html,"html.parser")

    artist_name = bsObj.find('div',{'class':'data__singer'})
    artist_name = artist_name.attrs['title']
    l.debug(artist_name)

    song_name = bsObj.find('h1',{'class':'data__name_txt'})
    song_name = modstr(song_name.text.strip())
    l.debug(song_name)

    cover = bsObj.find('img',{'class':'data__photo'})
    cover = 'http:'+cover.attrs['src']
    l.debug('Cover link: '+cover)
    sDict = {'artist':artist_name,'song_name':song_name,'songmid':songmid,'cover':cover }
    l.debug(sDict)
    return sDict


if __name__=='__main__':
    # page = 'file:///E://1.html'
    # qd_album(page)
    weblink = 'https://y.qq.com/n/yqq/song/003lVR2n4O9XtI.html'
    print(qd_song(weblink))