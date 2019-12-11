#!/usr/bin/python3
#coding:utf-8
# tested in win
__version__ = 20191126


from urllib.request import unquote
import json,os,re,shutil,random
from pathlib import PurePath
from pprint import pprint
from bs4 import BeautifulSoup
import pyautogui as auto

# customized module
from config import logfile,dldir
from openlink import op_simple,ran_header
from mtag import addtag
from mylog import get_funcname,mylogger
from mp3archive import find_album,create_folder
from mytool import mywait,get_text_clipboard,clickbutton,capture
from myfs import clean_f
from myimg import squaresize
from mystr import fnamechecker as modstr
import myget


headers = ran_header()


def decry(code): 
    '''decrypt download url'''
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


def get_songlocation(songid):
    '''Get undecryted location from xml'''
    url = f'https://emumo.xiami.com/widget/xml-single/sid/{songid}'
    html = op_simple(url,headers)[0]
    bsObj = BeautifulSoup(html,"html.parser")
    location = bsObj.find('location').text
    return location

#not use any more
def f2json(text):  
    ml = mylogger(logfile,get_funcname()) 
    try:   
        data = re.split('jsonp\d*',text)
        j = json.loads(data[1][1:-1])
    except TypeError as e:
        ml.error(e)
        return None
    return j


def xm_json(workfolder,year=None,force=False):
    '''Analyze json album data'''
    ml = mylogger(logfile,get_funcname()) 

    j = json.loads(get_text_clipboard())
    # j = f2json(get_text_clipboard())
    j = j['result']['data']['albumDetail']

    if year is None:
        year = input('Publish year>>')
    artist_name = modstr(j['artistName'])
    album_name = modstr(j['albumName'])
    albumdir = f'{artist_name} - {year} - {album_name}'
    if find_album(albumdir) and force == False:
        ml.warning(f'{albumdir} alread archived')
    else:
        albumfulldir = create_folder(workfolder,albumdir)
        try:
            coverlink = j['albumLogo']
            cover = os.path.join(albumfulldir,albumdir+'.jpg')
            m_cover = os.path.join(albumfulldir,albumdir+'.png')
            if os.path.isfile(cover):
                ml.warning('---- Big Cover download already !') 
            else:
                ml.info('Download big cover')
                myget.dl(coverlink,out=cover)
            if os.path.isfile(m_cover):
                ml.warning('---- Small cover ready !') 
            else:
                shutil.copy(cover,m_cover)
                squaresize(m_cover)
            cdcount = j['cdCount']
            songcount = j['songCount']
            for s in range(songcount):
                singers = modstr(j['songs'][s]['singers'])
                songname = modstr(j['songs'][s]['songName'])
                songfullname = f'{singers} - {songname}.mp3'
                mp3 = os.path.join(albumfulldir,songfullname)
                cdserial = str(j['songs'][s]['cdSerial'])
                track = str(j['songs'][s]['track'])
                if os.path.isfile(mp3):
                    ml.warning(f'---- {songname} download already !') 
                else:
                    try:       

                        ml.info(f'{cdserial}.{track} {singers} - {songname}')
                        songid = j['songs'][s]['songId']
                        location = get_songlocation(songid) 
                        dlurl = decry(location)
                        # dlurl = 'http:'+decry(location)
                        myget.dl(dlurl,out=mp3) 

                    except Exception as e :
                        ml.error(e)
                        ml.error("Content incomplete -> retry")
                        myget.dl(dlurl,out=mp3) 
                        mywait(random.randint(1,3))
                addtag(mp3,songname,album_name,artist_name,singers,
                        m_cover,year,track,cdserial) 
            os.remove(m_cover)
            clean_f(albumfulldir,'tmp')
            ml.info('Download Complete')
        except FileNotFoundError:
            pass


def chromef12(year,autoclose=False):
    """Chrome F12 find xhr and close page"""
    imgpath = os.path.join(PurePath(__file__).parent,'img')
    if clickbutton( os.path.join(imgpath,'xm.png')):
        auto.press('f12')
    else:
        raise
    mywait(1)
    auto.press('f5')
    mywait(2)
    if clickbutton( os.path.join(imgpath,'getalbumdetail.png')):
        auto.click(button='right')
        mywait(1)
    else:
        raise
    if clickbutton( os.path.join(imgpath,'copy.png')):
        mywait(1)
    else:
        raise    
    if clickbutton( os.path.join(imgpath,'copyresponse.png')):
        xm_json(dldir,year=year)
    else:
        raise
    if autoclose:
        auto.hotkey('ctrl','w')


if __name__ == "__main__":
    import sys
    try:
        if sys.argv[1] == 'f':
            force = True    
    except IndexError:
        force = False
    if os.path.exists(logfile):
        os.remove(logfile)
    try:
        xm_json(dldir,force=force)
    except KeyboardInterrupt:
        print('ctrl + c')

