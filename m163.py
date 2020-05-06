#!/usr/bin/python3
#coding:utf-8
# tested in win

__version__ = 20200506


import base64
import requests
import sys
import codecs
import shutil
import os
import random
import re
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from bs4 import BeautifulSoup
from urllib.request import urlopen,Request,HTTPError,unquote
from pprint import pprint
from selenium import webdriver  
# from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
# from invoke import task

# customized module
import myget
from myfs import clean_f
from myimg import squaresize
from mtag import addtag
from mylog import mylogger,get_funcname
from mytool import mywait
from mystr import fnamechecker as modstr
from mystr import splitall
from openlink import op_simple , op_requests,ran_header
from config import logfile, dldir
from mp3archive import create_folder,find_album



# para1 = "{\"ids\":\"[%d]\",\"br\":128000,\"csrf_token\":\"\"}"
para2 = "010001"
para3 = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
para4 = "0CoJUm6Qyw8W8jud"
rankey = 16 * 'F'
encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
url = 'http://music.163.com/api/album/%d/'
agentref = 'https://music.163.com/'
host = 'music.163.com'
org = 'https://music.163.com'
######### decode begin ##########
def RSA_en(value,text,modulus): # not in use
    text = text[::-1]
    rs = int(codecs.encode(text.encode('utf8'),'hex_codec'),16) ** int(value,16) % int(modulus,16)
    return format(rs,'x').zfill(256)

def get_params(para1):
    '''twice AES encrypt against songid'''
    iv = "0102030405060708"
    first_key = para4
    second_key = 16 * 'F'  # as random str
    h_encText = AES_encrypt(para1, first_key, iv)
    h_encText = AES_encrypt(h_encText, second_key, iv)
    return h_encText

def AES_encrypt(text, key, iv): 
    '''Return encoded bytes'''
    pad = 16 - len(text) % 16
    if isinstance(text, str):
        # print('Is string')
        text = text + pad * chr(pad)
    else:
        # print('Not string')
        text = text.decode('utf-8') + pad * chr(pad)
    encryptor = AES.new(key.encode("utf8"), AES.MODE_CBC, iv.encode("utf8"))
    encrypt_text = encryptor.encrypt(text.encode("utf8"))
    encrypt_text = base64.b64encode(encrypt_text)
    return encrypt_text
######### decode end ##########

def get_json(url, params, encSecKey):
    '''Get response of song download url'''
    ml = mylogger(logfile,get_funcname())
    data = {
        "params": params,
        "encSecKey": encSecKey
    }
    response = requests.post(url,headers=ran_header(agentref,host,org),data=data)
    ml.debug(response.json())
    return response.json()['data']

def get_dlurl(songid):
    '''Input song id , Return song download link'''
    # para1 = "{\"ids\":\"[%d]\",\"br\":128000,\"csrf_token\":\"\"}" % int(songid)
    para1 = '{"ids":"[%s]","level":"standard","encodeType":"mp3","csrf_token":""}' % songid
    # url = 'https://music.163.com/weapi/song/enhance/player/url?csrf_token='
    api = 'https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token='
    params = get_params(para1)   
    # encSecKey = RSA_en(para2,rankey,para3)  # not in use
    rsp = get_json(api, params, encSecKey)
    music_url = rsp[0].get('url')
    return music_url

def op_sel(web):
    '''
    Use selenium + chromedriver to scrap web
    Put chromedriver into Python folder
    Need to explicit driver.quit() after invocation
    '''
    ml = mylogger(logfile,get_funcname()) 
    chrome_options = Options()  
    chrome_options.add_argument("headless") 
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=chrome_options)  
    driver.get(web)
    try:
        element = WebDriverWait(driver,10).until(
            EC.frame_to_be_available_and_switch_to_it(('contentFrame'))
        )
        year = driver.find_elements_by_css_selector('p.intr')
        ml.debug(year)
        year = year[1].text
        year = splitall(['：','-'],year)[1]
    finally:
        driver.quit()  
    return year

def ana_song(weblink):
    ml = mylogger(logfile,get_funcname()) 
    html = op_simple(weblink,ran_header(agentref,host,org))[0]
    # html = op_requests(url,verify=False).content 
    bsObj = BeautifulSoup(html,"html.parser")
    # ml.debug(bsObj)
    # title = bsObj.find('title')
    # print(title)
    song_name = bsObj.find('em',{'class':'f-ff2'})
    songname = modstr(song_name.text.strip())
    ml.debug(songname)
    aa = bsObj.findAll('p',{'class':'des s-fc4'})
    artistname = modstr(aa[0].span.a.text)
    albumname = modstr(aa[1].a.text)
    ml.debug(artistname)
    ml.debug(albumname)
    cover = bsObj.find('div',{'class':'u-cover u-cover-6 f-fl'})
    cover = cover.img.attrs['href']
    ml.debug(cover)
    songmid = weblink.split('=')[-1]
    sDict = {'artist':artistname,'song_name':songname,'songmid':songmid,'cover':cover }
    ml.debug(sDict)
    return sDict

def ana_cd(albumlink):
    '''Get album JSON data'''
    ml = mylogger(logfile,get_funcname()) 
    year = op_sel(albumlink)
    albumid = albumlink.split('=')[-1]
    ml.debug(albumid)
    url = f'http://music.163.com/api/album/{albumid}/'
    html = op_simple(url,ran_header(agentref,host,org))[0]
    # print(html)
    jdata = BeautifulSoup(html,"html.parser").prettify()
    ml.debug(jdata)
    adict = ana_json(jdata)
    adict['year'] = year
    ml.debug(adict)
    return adict

def ana_json(jdata):
    '''Analyze Json get album song details'''
    ml = mylogger(logfile,get_funcname()) 
    j=json.loads(jdata)
    adict = {}
    adict['cover'] = j['album']['picUrl']
    adict['number'] = j['album']['size']
    adict['albumname'] = j['album']['name']
    adict['artist'] = j['album']['artist']['name']
    count = 1
    for s in j['album']['songs']:
        sdict = {}
        sdict['id'] = s['id']
        sdict['songname'] = s['name']
        sdict['tracknum'] = str(s['disc'])+'.'+str(s['no'])
        artists = []         
        for x in s['artists']:
            artists.append(x['name'])
        sdict['singer'] = ','.join(artists)
        adict[count] = sdict
        count += 1
    ml.debug(adict)
    return adict

def albumdl(albumlink,force=False):
    '''main function to download album'''
    ml = mylogger(logfile,get_funcname()) 
    adict = ana_cd(albumlink)
    coverlink = adict['cover']
    artist = adict['artist']
    year = adict['year']
    albumname = adict['albumname']
    albumdir = f'{artist} - {year} - {albumname}'
    if find_album(albumdir) and force == False:
        ml.warn(f'Album alread archived')
    else:
        albumfulldir = create_folder(dldir,albumdir)
        cover = os.path.join(albumfulldir,albumdir+'.jpg')
        m_cover = os.path.join(albumfulldir,albumdir+'.png')
        # if os.path.isfile(cover):
        #     ml.debug('Big Cover download already !') 
        if not os.path.isfile(cover):
            ml.info('Download big cover')
            myget.dl(coverlink,out=cover)
        # if os.path.isfile(m_cover):
        #     ml.debug('Small cover already generated !') 
        if not os.path.isfile(m_cover):
            shutil.copy(cover,m_cover)
            squaresize(m_cover)
        for n in range(1,adict['number']+1):
            songid = adict[n]['id']
            singer = modstr(adict[n]['singer'])
            songname = modstr(adict[n]['songname']) 
            tracknum = adict[n]['tracknum']
            songfullname = f'{singer} - {songname}.mp3'
            mp3 = os.path.join(albumfulldir,songfullname)
            ml.info(f'{tracknum} {singer} - {songname}')
            # if os.path.isfile(mp3):
            #     ml.warn('>>>> Track download already !') 
            # else:
            if not os.path.isfile(mp3):
                try:
                    dlurl = get_dlurl(songid)   
                    myget.dl(dlurl,out=mp3) 
                except TypeError:
                    ml.err('Not published Track')
                    continue
                except Exception as e :
                    ml.err(e)
                    ml.err("Content incomplete -> retry")
                    myget.dl(dlurl,out=mp3) 
                else:
                    addtag(mp3,songname,albumname,artist,singer,
                            m_cover,year,tracknum) 
                    mywait(random.randint(1,3))
        try:
            os.remove(m_cover)
            clean_f(albumfulldir,'tmp')
            ml.info(f'Complete download {albumdir}')
        except FileNotFoundError:
            pass

def songdl(weblink):
    ''''''
    ml = mylogger(logfile,get_funcname()) 
    sDict = ana_song(weblink)
    mp3 = sDict['artist']+' - '+sDict['songname']+'.mp3'
    if not os.path.isfile(mp3):
        try:
            coverlink = sDict['cover']
            m_cover = mp3+'.png'
            myget.dl(coverlink,out=m_cover)   
            myget.dl(dlurl,out=mp3) 
        except TypeError:
            ml.err('Not published Track')
        except Exception as e :
            ml.err(e)
            ml.err("Content incomplete -> retry")
            myget.dl(dlurl,out=mp3) 
        else:
            songname = sDict['songname']
            artist = sDict['artist']
            singer = sDict['artist']
            addtag(mp3,songname,albumname,artist,singer,m_cover) 


def m163():
    while True:
        url = input('Link >>')
        try:
            albumdl(url)
        except KeyboardInterrupt:
            print('ctrl + c')  
            sys.exit()  


if __name__ == "__main__":
    m163()

    # id = '1418069679'
    # music_url = get_dlurl(id)
    # print(music_url)

    # import myget
    # myget.dl(music_url)
