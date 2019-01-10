#!/usr/bin/python
#coding:utf-8
# Python3

# from decry import decry
from urllib.request import unquote
from modstr import modificate
from bs4 import BeautifulSoup
from openlink import op_simple

from mylognew import get_funcname,mylogger
# import mylog as ml
logfilelevel = 10 # Debug
logfile = 'E:\\app.log'

def get_loc_one(song_id):
    l = mylogger(logfile,logfilelevel,get_funcname()) 
    url = 'http://www.xiami.com/widget/xml-single/sid/%s'
    url = url.replace('%s', song_id)
    # url = 'file:///E://xml.xml'
    page = op_simple(url)
    l.debug(page[1])
    bsObj = BeautifulSoup(page[0],"html.parser") #;print(bsObj)
    location = bsObj.find("location")
    location = str(location)[19:-14]
    if location == '':
        l.debug('Track not published')
        SongDic = {}
    else:           
        l.debug('Raw Location: '+location)
        location = decry(location)
        song = bsObj.find("song_name")
        song = modificate(str(song)[20:-15])
        singer = bsObj.find("artist_name")
        singer = modificate(str(singer)[22:-17])     
        album = bsObj.find("album_name")
        album = modificate(str(album)[21:-16])
        cover = bsObj.find('album_cover')
        cover = 'http:'+str(cover)[22:-17]
        SongDic = {'location':location,'song':song,'cover':cover,\
                    'artist':singer,'singer':singer,'album':album}
        l.debug(SongDic)
    return SongDic


def get_loc_cd(song_id):
    l = mylogger(logfile,logfilelevel,get_funcname()) 
    url = 'http://www.xiami.com/widget/xml-single/sid/%s' % song_id
    # url = url.replace('%s', song_id)
    # url = 'file:///E://xml.xml'
    page = op_simple(url)
    l.debug(page[1])
    bsObj = BeautifulSoup(page[0],"html.parser") #;print(bsObj)
    location = bsObj.find("location")
    location = str(location)[19:-14] 
    if location == '':
        l.debug('Track not published')
        SongDic = {}
    else:           
        l.debug('Raw Location: '+location)
        location = decry(location)
        # location = location.replace('/m128','/m320')
        song = bsObj.find("song_name")
        song = modificate(str(song)[20:-15])
        singer = bsObj.find("artist_name")
        singer = modificate(str(singer)[22:-17])     
        SongDic = {'location':location,'song':song,'singer':singer}
        l.debug(SongDic)
    return SongDic


def decry(code): # decrypt download url
    url = code[1:]
    urllen = len(url)
    rows = int(code[0])
    cols_base = urllen // rows  #;print(cols_base) # basic column count
    rows_ex = urllen % rows #;print(rows_ex)   # count of rows that have 1 more column
    matrix = []
    for r in range(rows):
        length = cols_base + 1 if r < rows_ex else cols_base
        matrix.append(url[:length])
        url = url[length:]
    #for i in matrix : print(i)
    url = ''
    for i in range(urllen):
        url += matrix[i % rows][i // rows]
    #print(url)
    return unquote(url).replace('^', '0')


if __name__=='__main__':
     
    song_id = str(1795287087)
    # d = get_loc_one(song_id)   
    # print(d) 
    d = get_loc_cd(song_id)
    print(d)

    # Test decry()
    # code = '7h%1m28%E15_753hDE556d3a8t22iF522%417E%_12EE4cfa1tF8.6%F6264723k5%%-cdf8cp%.n9527F1997Fe255%955cf%2xe%E1615%7.ay4EE5259a3Fit26%77458mu%%4-E2215Ama%F95697E%pt35%%-d7b9'
    # url = decry(code)
    # print(url)
