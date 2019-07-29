#!/usr/bin/python3
#coding:utf-8
# tested in win

# import requests

# download_url = "http://music.163.com/song/media/outer/url?id=%s" % '1346093140'
# try:
#     with open(i[1]+'.mp3', 'wb') as f:
#         f.write(requests.get(download_url, headers=headers).content)
# except:
#     pass


from ed_ana import ana_cd,ana_json


def dl(albumlink):
    jdata = ana_cd(albumlink)
    adict = ana_json(jdata)
    cover = adict['cover']
    artist = adict['artist']
    for s in range(1,adict['number']+1):
        print(adict[s]['id'])
        singer = adict[s]['singer']
        songname = adict[s]['songname'] 
        adict[s][''] 
        adict[s]['']        


if __name__ == "__main__":
    url = 'https://music.163.com/#/album?id=79753582'
    dl(url)
        