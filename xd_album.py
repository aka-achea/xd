#!/usr/bin/python
#coding:utf-8
# Python3


from bs4 import BeautifulSoup
from urllib.request import urlopen,Request,HTTPError,unquote
from html.parser import HTMLParser
from modstr import modificate

web = 'file:///E://22.html'

html = urlopen(web)
bsObj = BeautifulSoup(html,"html.parser") #;print(bsObj)


album_name = modificate(bsObj.find('h1').text)
print(album_name)

info = bsObj.find(text = '艺人：').parent.next_sibling.next_sibling
print(info)

artist_name = modificate(info.text)
print(artist_name)

year = info.next_sibling.next_sibling.next_sibling
print(year)

# track = bsObj.find_all('input',{'type':'checkbox'})
# for i in track:
#     #print(i)
#     trackid = i.attrs['value']
#     print(trackid)
#     tracknumber = i.parent.next_sibling.next_sibling.text
#     print(tracknumber)
#     song

# type="checkbox"
# checked="checked"










