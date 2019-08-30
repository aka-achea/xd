#!/usr/bin/python3
#coding:utf-8
# tested in win


from urllib.request import unquote
import json,os,re,shutil,random

# customized module
from sharemod import create_folder,logfile,clean_f,modstr,imgresize
import myget
from mtag import addtag
from mylog import get_funcname,mylogger
from mp3archive import find_album
from mytool import mywait,get_text_clipboard


#https://emumo.xiami.com/play?ids=/song/playlist/id/
#emumo.xiami.com


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


def f2json(text):  
    ml = mylogger(logfile,get_funcname()) 
    try:   
        data = re.split('jsonp\d*',text)
        j = json.loads(data[1][1:-1])
    except TypeError as e:
        ml.error(e)
        return None
    return j


def xm_json(workfolder,force=False):
    ml = mylogger(logfile,get_funcname()) 

    j = f2json(get_text_clipboard())
    n = 0
  
    artist_name = modstr(j['data']['trackList'][n]['artist_name'])
    album_name = modstr(j['data']['trackList'][n]['album_name'])
    if album_name == '':
        album_name = 'unkown' 

    year = input('Publish year>>')
    if year == '': year = '2019'
    albumdir = f'{artist_name} - {year} - {album_name}'

    if find_album(albumdir) and force == False:
        ml.warning(f'Album alread archived')
    else:
        albumfulldir = create_folder(workfolder,albumdir)
        try:
            album_pic = 'http:'+j['data']['trackList'][n]['album_pic']        
            cover = os.path.join(albumfulldir,albumdir+'.jpg')
            m_cover = os.path.join(albumfulldir,albumdir+'.png')

            if os.path.isfile(cover):
                ml.warning('---- Big Cover download already !') 
            else:
                ml.info('Download big cover')
                myget.dl(album_pic,out=cover)

            if os.path.isfile(m_cover):
                ml.warning('---- Small cover ready !') 
            else:
                shutil.copy(cover,m_cover)
                imgresize(m_cover)
        except:
            m_cover = ''

        while True:
            try:
                # songId = j['data']['trackList'][n]['songId']
                singers = modstr(j["data"]["trackList"][n]["singers"])
                # singers = modificate(singers)
                songName = modstr(j["data"]["trackList"][n]["songName"])
                track = str(j["data"]["trackList"][n]["track"])
                cdSerial = str(j["data"]["trackList"][n]["cdSerial"])
                location = j["data"]["trackList"][n]["location"]
                dlurl = 'http:'+decry(location)
                songfullname = f'{singers} - {songName}.mp3'
                mp3 = os.path.join(albumfulldir,songfullname)
                ml.info(f'{cdSerial}.{track} {singers} - {songName}')
                if os.path.isfile(mp3):
                    ml.warning('---- Track download already !') 
                else:
                    try:
                        myget.dl(dlurl,out=mp3) 
                    except Exception as e :
                        ml.error(e)
                        ml.error("Content incomplete -> retry")
                        myget.dl(dlurl,out=mp3) 
                addtag(mp3,songName,album_name,artist_name,singers,m_cover,\
                        year,track,cdSerial) 
                n += 1
                mywait(random.randint(1,3))
            except IndexError:
                break

        try:
            os.remove(m_cover)
            clean_f(albumfulldir)
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
        xm_json(workfolder,force)
    except KeyboardInterrupt:
        print('ctrl + c')
