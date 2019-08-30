#!/usr/bin/python3
#coding:utf-8
# tested in win


from urllib.request import unquote
import json,os,re,shutil,random
from pprint import pprint
from bs4 import BeautifulSoup

# customized module
from config import logfile
import myget
from mtag import addtag
from mylog import get_funcname,mylogger
from mp3archive import find_album,create_folder
from mytool import mywait,get_text_clipboard
from myfs import clean_f
from myimg import squaresize
from mystr import fnamechecker as modstr
from openlink import op_simple,ran_header


headers = ran_header()


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
        ml.warning(f'Album alread archived')
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
                cdserial = str(j['songs'][s]['cdSerial'])
                track = str(j['songs'][s]['track'])
                singers = modstr(j['songs'][s]['singers'])
                songname = modstr(j['songs'][s]['songName'])
                songid = j['songs'][s]['songId']
                location = get_songlocation(songid)
                dlurl = decry(location)
                # dlurl = 'http:'+decry(location)
                songfullname = f'{singers} - {songname}.mp3'
                mp3 = os.path.join(albumfulldir,songfullname)
                ml.info(f'{cdserial}.{track} {singers} - {songname}')
                if os.path.isfile(mp3):
                    ml.warning('---- Track download already !') 
                else:
                    try:
                        myget.dl(dlurl,out=mp3) 
                    except Exception as e :
                        ml.error(e)
                        ml.error("Content incomplete -> retry")
                        myget.dl(dlurl,out=mp3) 
                addtag(mp3,songname,album_name,artist_name,singers,
                        m_cover,year,track,cdserial) 
                mywait(random.randint(1,3))
            os.remove(m_cover)
            clean_f(albumfulldir,'tmp')
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    workfolder = r'L:\Music\_DL'
    import sys
    try:
        if sys.argv[1] == 'f':
            force = True    
    except IndexError:
        force = False
    if os.path.exists(logfile):
        os.remove(logfile)
    try:
        xm_json(workfolder,force=force)
    except KeyboardInterrupt:
        print('ctrl + c')

