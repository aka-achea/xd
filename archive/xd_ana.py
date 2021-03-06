#!/usr/bin/python
#coding:utf-8
# Python3


from bs4 import BeautifulSoup
from urllib.request import urlopen,Request,HTTPError,unquote
from html.parser import HTMLParser

# customized module
from mylog import get_funcname,mylogger
from sharemod import modstr,logfile,logfilelevel,albumlist,find_album

#aDict {'album','artist','year','bcover','scover','Discs','DiskNum','(DiscNum,TrackNum)'}

#not convenient to get song name , move to xml
def ana_song(weburl):
    l = mylogger(logfile,logfilelevel,get_funcname()) 
    songid = weburl.split('/')[-1]
    songid = songid.split('?')[0]
    l.debug(songid)
    return songid

def ana_cd(page):  # download web first, return album dictionary
    # print(logfile)
    l = mylogger(logfile,logfilelevel,get_funcname()) 
    html = urlopen(page)
    bsObj = BeautifulSoup(html,"html.parser") 
    #print(bsObj)
    album_name = bsObj.find('div',{'class':'album-name'})
    album_name = modstr(album_name.text)
    l.debug(album_name)
    artist = bsObj.find('div',{'class':'singers'})
    artist_name = modstr(artist.text)
    l.debug(artist_name)
    year = artist.next_sibling.text[:4]
    l.debug(year)
    cover = bsObj.find('div',{'class':'cover'})
    cover = cover.attrs['style'].split('(')
    scover = 'http://'+cover[1][2:-1]
    l.debug(scover)
    bcover = scover.split('?')[0]
    l.debug(bcover)    
    fullname = artist_name+' - '+year+' - '+album_name
    if find_album(album_name,albumlist):
        l.warning(fullname+' already downloaded')
        return False
    else:
        aDict = {'album':album_name,'artist':artist_name,'year':year,'fullname':fullname,
                'bcover':bcover,'scover':scover }
        l.debug(aDict)
        discs = bsObj.find_all('div',{'class':'disc'})
        disc_n = len(discs)
        aDict['Discs'] = disc_n
        for d in discs:
            DiscNum = modstr(d.h3.text[4:])
            l.debug('DiscNum '+DiscNum)
            Tracks = d.find_all('span',{'class':'em index'})
            aDict[DiscNum] = len(Tracks)
            for t in Tracks:
                tracknum = t.text
                l.debug(tracknum)
                songid = t.parent.parent.next_sibling.div.div.a["href"]
                songid = songid.split('/')[2]
                l.debug(songid)
                aDict[DiscNum,tracknum] = songid
        l.debug(aDict)
    return aDict



if __name__=='__main__':
    logfilelevel = 10 # Debug
    logfile = 'E:\\app.log'
    #test xd_album
    web = 'file:///E://1.html'
    page = 'file:\\\E:\\UT\\xd_ana.ana_cd.html'

    D = ana_cd(page)
    print(D)

    # test xd_song
    # weburl = 'https://www.xiami.com/song/1798102569?spm=a2oj1.12028094.0.0.ba054ca2H9ui3w'
    # # web = 'file:///E://song.html'
    # song_id = ana_song(weburl)
    # # l.debug(song_id)
    # print(song_id)
