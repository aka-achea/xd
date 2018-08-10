#!/usr/bin/python
#coding:utf-8
# Python3

from decry import decry
from modstr import modificate
from bs4 import BeautifulSoup
# from html.parser import HTMLParser
from openlink import oplink

# c = url.split('/')[3]
#     if c == 'song':
#     elif c == 'album':
#         print('album')

def get_songid(song_url):
    bsObj = BeautifulSoup(oplink(song_url)[0],"html.parser")
    print(bsObj)
    song_id = bsObj.find('meta',{'name':'mobile-agent'})
    print(song_id)
    song_id = song_id.get('content').split('/')[-1]
    print(song_id)
    # albumname = bsObj.find('meta',{'property':'og:music:album'})
    # albumname = albumname.get('content')
    # print(albumname)
    return song_id

# def get_songlist(html):
#     bsObj = BeautifulSoup(html,"html.parser")
#     album_id = bsObj.find('meta',{'name':'mobile-agent'})
#     print(album_id)
#     #album_id = album_id.get('content')#.split('/')[-1]
#     # albumname = bsObj.find('meta',{'property':'og:title'})
#     # albumname = albumname.get('content')
#     return album_id#,albumname

def get_location(song_id):
    url = 'http://www.xiami.com/widget/xml-single/sid/%s'
    url = url.replace('%s', song_id)
    #location = re.search('<location*</location>',(oplink(url)[0]))
    bsObj = BeautifulSoup(oplink(url)[0],"html.parser") #;print(bsObj)
    location = bsObj.find("location")
    location = str(location)[19:-14]
    artist_name = bsObj.find("artist_name")
    artist_name = modificate(str(artist_name)[22:-17])  
    song_name = bsObj.find("song_name")
    song_name = modificate(str(song_name)[20:-15])
    album_name = bsObj.find("album_name")
    album_name = modificate(str(album_name)[21:-17])
    return location , artist_name,song_name,album_name

if __name__=='__main__':
    import mylog as ml
    import wget #, requests
    funcname = '__name__'
    logfilelevel = 10 # Debug
    logfile = 'E:\\app.log'
    l = ml.mylogger(logfile,logfilelevel,funcname)  

    # Test get_location()
    # song_id = '1796424128'
    # arrlocation = get_location(song_id)
    # location = arrlocation[0]
    # artist_name = arrlocation[1]
    # song_name = arrlocation[2]
    # album_name = arrlocation[3]
    # l.info(location)
    # l.info(artist_name)
    # l.info(song_name)
    # l.info(album_name)
    # mp3 = decry(location)
    # l.info(mp3)
    # wget.download(mp3)

    # Test get_songid()
    song_url = 'https://www.xiami.com/song/1796424128'
    r = get_songid(song_url)
    l.info(r)
   

    # headers = {
    #     "Accept":"text/html,application/xhtml+xml,application/xml; " \
    #         "q=0.9,image/webp,*/*;q=0.8",
    #     "Accept-Encoding":"text/html",
    #     "Accept-Language":"en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2",
    #     "Content-Type":"application/x-www-form-urlencoded",
    #     "User-Agent":"Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 "\
    #         "(KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36",
    #     "Referer":"www.xiami.com"}

    # url = 'http://www.xiami.com/album/nnejaZ95f64?spm=a1z1s.3061781.6856533.8.Pthiuw'
    # cookies = dict(member_auth="gWmcS45LuWkxi6PDSt8ydSIY4uLVGzmAlNtTjOMqvwQlddwMN4Ctx6uTQQxB3iGq0glcS%2BM")
    # html = requests.get(url,cookies=cookies,headers=headers)




    # r = get_songlist(html)
    # print(r)