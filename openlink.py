#!/usr/bin/python
#coding:utf-8
# Python3
# Version: 2018.10.22

import random,time,requests
from urllib.request import urlopen,Request,HTTPError
from urllib.error import URLError

def oplink(URL):
    headers = {
        "Accept":"text/html,application/xhtml+xml,application/xml; " \
            "q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding":"text/html",
        "Accept-Language":"en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2",
        "Content-Type":"application/x-www-form-urlencoded",
        # "User-Agent":"Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 "\
        #     "(KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        #"Referer":"www.xiami.com"
        }
    req = Request(URL,headers=headers)
    try:
        html = urlopen(req)
        time.sleep(random.uniform(2,3))
        #l.verbose(html.info())
        #l.debug(html.getcode())
        status = html.getcode()
    except HTTPError as e:
        status = e #5xx,4xx
        html = 0
    except URLError as e:
        print('Host no response, try again')
        time.sleep(30)
        try:
            html = urlopen(req)
        except:
            status = e 
            html = 0
    return html,status #return array object

def opsel(URL):    
    pass

def oprqs(URL,para=''):
    headers = {
        "Accept":"text/html,application/xhtml+xml,application/xml; " \
            "q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding":"text/html",
        "Accept-Language":"en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2",
        "Content-Type":"application/x-www-form-urlencoded",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        }
    html = requests.get(url=URL,params=para,headers=headers)
    return html

if __name__=='__main__':

    url = 'http://www.xiami.com/widget/xml-single/sid/1769402049'
    html = oplink(url)
    print(html[1])
    print(html[0])
