#!/usr/bin/python3
#coding:utf-8
# tested in win


import shutil
import os
import random


# customized module
from config import logfile, dldir
from mp3archive import create_folder,find_album
import myget
from myfs import clean_f
from myimg import squaresize
from mtag import addtag
from mylog import get_funcname,mylogger
from mytool import mywait
from mystr import fnamechecker as modstr
from ed_ana import ana_cd
from ed_decry import get_dlurl


def dl(albumlink,force=False):
    '''main function to download album'''
    ml = mylogger(logfile,get_funcname()) 

    adict = ana_cd(albumlink)
    coverlink = adict['cover']
    artist = adict['artist']
    year = adict['year']
    albumname = adict['albumname']

    albumdir = f'{artist} - {year} - {albumname}'
    if find_album(albumdir) and force == False:
        ml.warning(f'Album alread archived')
    else:
        albumfulldir = create_folder(dldir,albumdir)
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

        for tracknum in range(1,adict['number']+1):
            songid = adict[tracknum]['id']
            singer = modstr(adict[tracknum]['singer'])
            songname = modstr(adict[tracknum]['songname']) 
            songfullname = f'{singer} - {songname}.mp3'
            mp3 = os.path.join(albumfulldir,songfullname)
            ml.info(f'{tracknum} {singer} - {songname}')
            if os.path.isfile(mp3):
                ml.warning('---- Track download already !') 
            else:
                try:
                    dlurl = get_dlurl(songid)   
                    myget.dl(dlurl,out=mp3) 
                except TypeError:
                    ml.error('Not published Track')
                    continue
                except Exception as e :
                    ml.error(e)
                    ml.error("Content incomplete -> retry")
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


def main():
    # workfolder = r'L:\Music\_DL'
    while True:
        url = input('Link>>')
        try:
            dl(url)
        except KeyboardInterrupt:
            print('ctrl + c')  
            break  


if __name__ == "__main__":
    main()
        