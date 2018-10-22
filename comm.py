#!/usr/bin/python
#coding:utf-8
# Python3

import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3NoHeaderError, error # really need error?
from mutagen.id3 import ID3,TIT2,TALB,TPE1,TPE2,COMM,USLT,TCOM,TCON,TPOS,TDRC,TRCK,APIC



import mylog as ml
logfilelevel = 10 # Debug
logfile = 'E:\\app.log'

def modstr(text):
    funcname = 'comm.modstr'    
    l = ml.mylogger(logfile,logfilelevel,funcname)     
    #file_name = re.sub(r'\s*:\s*', u' - ', file_name)    # for FAT file system
    text = str(text)    
    before = text
    text = text.replace('?', u'？')      # for FAT file system
    text = text.replace('/', u'／')
    text = text.replace('|', '')
    text = text.replace(':', u'∶')    # for FAT file system
    text = text.replace('*', u'×')
    text = text.replace('&amp;', u'&')
    text = text.replace('&#039;', u'\'')
    #text = text.replace('\'', u'＇')
    text = text.replace('\\', u'＼')
    text = text.replace('"', u'＂')
    #text = text.replace('\'', u'＇')
    text = text.strip()
    #file_name = file_name.replace('$', '\\$')    # for command, see issue #7
    after = text
    if before != after :
        l.debug("Before modify: "+before)
        l.debug("After modify: "+after)
    return text

def create_folder(workfolder,aDict):
    funcname = 'comm.create_folder'
    l = ml.mylogger(logfile,logfilelevel,funcname)
    album = aDict['album']
    artist = aDict['artist']
    year = aDict['year']
    albumdir = artist+' - '+year+' - '+album
    l.info('Create folder: '+albumdir)
    os.chdir(workfolder)
    albumfulldir = workfolder +"\\"+albumdir
    if not os.path.exists(albumfulldir):
        os.makedirs(albumfulldir)
        os.chdir(albumfulldir)
    else:
        l.error('---- Album folder already exists !')
        os.chdir(albumfulldir)
    return albumdir

#addtag(mp3,m_artist,m_cover,m_year,m_trackid)
def addtag(fname,m_artist,m_cover,m_year='',m_trackid='',m_album='',\
           m_song='',m_singer='', m_cd=''):
    l = ml.mylogger(logfile,logfilelevel,'comm.addtag') 
    try:
        tags = ID3(fname)
    except ID3NoHeaderError:
        l.debug("Adding ID3 header on " + m_trackid)
        tags = ID3()
    
    if not m_song == '': 
        l.debug('add song name '+str(m_song))
        tags["TIT2"] = TIT2(encoding=3, text=m_song) 
    if not m_album == '': 
        l.debug('add album name '+m_album)
        tags["TALB"] = TALB(encoding=3, text=m_album) 
    if not m_artist == '': 
        l.debug('add artist name '+m_artist)
        tags["TPE2"] = TPE2(encoding=3, text=m_artist) #album artist
    #tags["COMM"] = COMM(encoding=3, lang=u'eng', desc='desc', text=u'mutagen comment')
    if not m_singer == '' : 
        l.debug('add singer name '+m_singer)
        tags["TPE1"] = TPE1(encoding=3, text=m_singer) # singer
    #tags["TCOM"] = TCOM(encoding=3, text=u'mutagen Composer')
    #tags["TCON"] = TCON(encoding=3, text=u'mutagen Genre')
    if not m_year == '': 
        l.debug('add year '+m_year)
        tags["TDRC"] = TDRC(encoding=3, text=m_year)
    if not m_trackid == '': 
        l.debug('add trackid '+str(m_trackid))
        tags["TRCK"] = TRCK(encoding=3, text=str(m_trackid))
    if not m_cd == '': 
        l.debug('add cd number '+str(m_cd))
        tags["TPOS"] = TPOS(encoding=3, text=str(m_cd))
    with open(m_cover,'rb') as c:
            cover = c.read()  #prepare for tag
    tags["APIC"] = APIC(encoding=3, mime=u'image/png',type=3,desc=u'Cover',data=cover)
    tags.save(fname,v2_version=3)

def readtag(fname):
    l = ml.mylogger(logfile,logfilelevel,'comm.readtag')
    tags = ID3(fname)
    title = tags["TIT2"]
    singer = tags['TPE1']
    l.debug(singer)
    l.debug(title)
    return singer,title


if __name__=='__main__':
    # text1 = 'ル・デ'
    # modstr(text1)
    # print(text1)
    fname = 'F:\\Music\\02 No Love for Hard Times.mp3'
    a = readtag(fname)
    print(type(a))
    singer = str(a[0])
    title = str(a[1])
    songname = singer+' - '+title
    print(songname)
#    print(a('TIT2'))
#    print(str(a['TDRC']).strip())
    
