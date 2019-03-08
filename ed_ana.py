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
from openlink import op_simple , op_requests

def ana_song(weblink):

    l = mylogger(logfile,logfilelevel,get_funcname()) 
    html = op_simple(weblink)[0]
    # html = op_requests(url,verify=False) 
    bsObj = BeautifulSoup(html,"html.parser")
    # l.debug(bsObj)
    # title = bsObj.find('title')
    # print(title)

    song_name = bsObj.find('em',{'class':'f-ff2'})
    songname = modstr(song_name.text.strip())
    l.info(songname)
    aa = bsObj.findAll('p',{'class':'des s-fc4'})
    artistname = modstr(aa[0].span.a.text)
    albumname = modstr(aa[1].a.text)
    l.info(artistname)
    l.info(albumname)

def ana_cd(weblink):
    l = mylogger(logfile,logfilelevel,get_funcname()) 
    html = op_simple(weblink)[0]
    bsObj = BeautifulSoup(html,"html.parser") #;print(bsObj)


if __name__ == "__main__":
    url = 'https://music.163.com/song?id=1346093140'    
    ana_song(url)