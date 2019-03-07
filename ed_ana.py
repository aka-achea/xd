#!/usr/bin/python
#coding:utf-8
# Python3

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
    # html = op_simple(weblink)[0]
    html = op_requests(url,verify=False) 
    bsObj = BeautifulSoup(html,"html.parser")
    # l.debug(bsObj)

    song_name = bsObj.find('em',{'class':'f-ff2'})
    song_name = modstr(song_name.text)
    l.info(song_name)

    artist_name = bsObj.find('a',{'class':'s-fc7'})
    artist_name = modstr(artist_name.text.strip())
    l.info(artist_name)

def ana_cd(weblink):
    l = mylogger(logfile,logfilelevel,get_funcname()) 
    html = op_simple(weblink)[0]
    bsObj = BeautifulSoup(html,"html.parser") #;print(bsObj)


if __name__ == "__main__":
    url = 'https://music.163.com/#/song?id=1346093140'    
    ana_song(url)