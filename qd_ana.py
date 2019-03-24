#!/usr/bin/python3
#coding:utf-8
# tested in win

from bs4 import BeautifulSoup
from urllib.request import urlopen,Request,HTTPError,unquote
from html.parser import HTMLParser
import re

# customized module
from mylog import get_funcname,mylogger
from sharemod import modstr,logfile
from openlink import op_simple


def ana_album(weblink): 
    ml = mylogger(logfile,get_funcname()) 
    html = op_simple(weblink)[0]
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

    song = bsObj.findAll('div',{'class':'songlist__number'})
    n = 0
    songtmp = [] # name duplicate check
    for i in song:
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
            s = list(map(lambda x: x.text, singers ))
            singer = ','.join(s) 
        else:
            singer = singers[0].text
        ml.debug(singer)
        si = [songmid, songname,singer]
        aDict[int(tracknumber)] = si
    aDict['TrackNum'] = n
    ml.debug(aDict)
    return aDict  # Album dictionary

def ana_song(weblink): # return song dictionary
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


if __name__=='__main__':
    import os
    if os.path.exists(logfile):
        os.remove(logfile)
    # test ana_album
    page = 'file:///E://1.html'
    # page = 'https://y.qq.com/n/yqq/album/004PDvDb4ZxKrR.html'
    ana_album(page)

    # test ana_song
    # weblink = 'https://y.qq.com/n/yqq/song/003lVR2n4O9XtI.html'
    # print(ana_song(weblink))