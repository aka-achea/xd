#!/usr/bin/python3
#coding:utf-8
# tested in win

import requests

download_url = "http://music.163.com/song/media/outer/url?id=%s" % '1346093140'
try:
    with open(i[1]+'.mp3', 'wb') as f:
        f.write(requests.get(download_url, headers=headers).content)
except:
    pass