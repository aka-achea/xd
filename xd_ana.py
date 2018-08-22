#!/usr/bin/python
#coding:utf-8
# Python3


from bs4 import BeautifulSoup
from urllib.request import urlopen,Request,HTTPError,unquote
from html.parser import HTMLParser
from modstr import modificate

import mylog as ml
logfilelevel = 10 # Debug
logfile = 'E:\\app.log'

#not convenient to get song name , move to xml
def xd_album(page):
    funcname = 'xd_ana.xd_album'
    l = ml.mylogger(logfile,logfilelevel,funcname)   
    html = urlopen(page)
    bsObj = BeautifulSoup(html,"html.parser") #;print(bsObj)
    album_name = bsObj.find('meta',{'property':'og:title'})
    album_name = modificate(album_name.attrs['content'])
    l.debug(album_name)

    info = bsObj.find(text = '艺人：').parent.next_sibling.next_sibling
    l.debug(info)
    artist_name = modificate(info.text)
    l.debug(artist_name)
    info = bsObj.find(text = '发行时间：').parent.next_sibling.next_sibling
    l.debug(info)
    year = modificate(info.text[:4])
    l.debug(year)

    info = bsObj.find('div',{'id':'album_cover'}).a
    bcover = 'http:'+info.attrs['href']
    scover = 'http:'+info.img.attrs['src']
    l.debug(scover)
    l.debug(bcover)

    aDict = {'album':album_name,'artist':artist_name,'year':year,
            'bcover':bcover,'scover':scover }
    l.debug(aDict)

    disc = bsObj.find_all('strong',{'class':'trackname'})
    l.debug(disc)

    if len(disc) < 2:
        track = bsObj.find_all('input',{'type':'checkbox'})
        n = 0
        for i in track:
            l.debug(i)
            n = n + 1
            trackid = i.attrs['value']
            l.debug(trackid)
            i = i.parent.next_sibling.next_sibling
            tracknumber = int(i.text)
            l.debug(tracknumber)
            # i = i.next_sibling.next_sibling
            # song_name = modificate(i.text)
            # print(song_name)
            aDict[tracknumber] = trackid
        l.debug(n)
        aDict['TrackNum'] = n
    else:
        l.info('There are '+str(len(disc))+' Disc')
        track = bsObj.find_all('input',{'type':'checkbox'})
        n = 0 ; m = 0
        for i in track:
            l.debug(i)
            n = n + 1
            trackid = i.attrs['value']
            l.debug(trackid)
            i = i.parent.next_sibling.next_sibling
            tracknumber = int(i.text)
            l.debug('Track number : '+str(tracknumber))
            if tracknumber == 1: m = m+1                
            aDict[m,tracknumber] = trackid
        l.debug(n)
        aDict['TrackNum'] = n
        aDict['Disc'] = m
    l.debug(aDict)
    return aDict

def xd_song(page):
    funcname = 'xd_ana.xd_album'
    l = ml.mylogger(logfile,logfilelevel,funcname) 
    html = urlopen(page)
    bsObj = BeautifulSoup(html,"html.parser") #;print(bsObj)
    song_id = bsObj.find('meta',{'name':'mobile-agent'})
    l.debug(song_id)
    song_id = song_id.get('content').split('/')[-1]
    l.debug(song_id)
    return song_id

if __name__=='__main__':
    

    #test xd_album
    web = 'file:///E://1.html'
    D = xd_album(web)
    # print(D['1'],D)
    # print(D['Disc'])

    # test xd_song
    # web = 'file:///E://song.html'
    # song_id = xd_song(web)
    # l.debug(song_id)
    # print(song_id)
