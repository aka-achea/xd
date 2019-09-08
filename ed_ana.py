#!/usr/bin/python3
#coding:utf-8
# tested in win
#version:20190828


from bs4 import BeautifulSoup
from urllib.request import urlopen,Request,HTTPError,unquote
# from html.parser import HTMLParser
import re,json
from pprint import pprint
# from urllib.parse import urlparse
from selenium import webdriver  
# from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options  


# customized module
from mylog import get_funcname,mylogger
from config import logfile
from openlink import op_simple , op_requests,ran_header
from mystr import fnamechecker as modstr
from mystr import splitall

# header = {
#     'Cookie': 'appver=1.5.0.75771;',
#     'Referer': 'http://music.163.com/',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
# }


url = 'http://music.163.com/api/album/%d/'

agentref = 'http://music.163.com/'

def ana_song(weblink):
    ml = mylogger(logfile,get_funcname()) 
    html = op_simple(weblink,header)[0]
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


def ana_cd(albumlink):
    '''Get album JSON data'''
    # ml = mylogger(logfile,get_funcname()) 
    # html = op_simple(albumlink,ran_header(ref=agentref))[0]
    year = op_sel(albumlink)
    # print(year)
    albumid = albumlink.split('=')[-1]
    # print(albumid)
    url = f'http://music.163.com/api/album/{albumid}/'
    html = op_simple(url,ran_header(ref=agentref))[0]
    bsObj = BeautifulSoup(html,"html.parser")
    jdata = bsObj.prettify()
    adict = ana_json(jdata)
    adict['year'] = year
    # print(jdata)
    return adict


def ana_json(data):
    '''Analyze Json get album song details'''
    j=json.loads(data)
    # pprint(j)
    adict = {}
    adict['cover'] = j['album']['picUrl']
    adict['number'] = j['album']['size']
    adict['albumname'] = j['album']['name']
    adict['artist'] = j['album']['artist']['name']
    for s in j['album']['songs']:
        sdict = {}
        sdict['id'] = s['id']
        sdict['songname'] = s['name']
        artists = []         
        for x in s['artists']:
            artists.append(x['name'])
        sdict['singer'] = ','.join(artists)
        adict[s['no']] = sdict
    # pprint(adict)
    return adict


def op_sel(web):
    '''Use selenium + chromedriver to scrap web
    Put chromedriver into Python folder
    Need to explicit driver.quit() after invocation
    '''
    chrome_options = Options()  
    chrome_options.add_argument("headless") 
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # chrome_options.add_argument("no-sandbox") 
    # chrome_options.add_argument('user-data-dir="E:\\xm"')   
    # cpath = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
    # chrome_options.binary_location = cpath    
    # if log != '':
    cd_arg = [f"--log-path=j:\c.log","--verbose"]
    # chrome_options.add_argument('log-path=j:\\c.log')
    # chrome_options.add_argument('verbose')
    driver = webdriver.Chrome(
            # executable_path="J:\\DOC\\GH\\test\\chromedriver.exe",
            # service_args=cd_arg,  # this work
            options=chrome_options)  
    driver.get(web)  
    driver.switch_to.frame('contentFrame')
    year = driver.find_elements_by_css_selector('p.intr')
    year = year[1].text
    year = splitall(['：','-'],year)[1]
    driver.quit()
    return year


if __name__ == "__main__":
    # url = 'https://music.163.com/#/song?id=1330348068'    
    # sDict = ana_song(url)
    
    # url = 'file:///E://1.html'
    url = 'https://www.xiami.com/album/yhWS4Ie1702'
    adict = ana_cd(url)
    pprint(adict)
   