#!/usr/bin/python3
#coding:utf-8
# test in Win

__version__ = 20201213

import requests,json,os,re,shutil,random
from pprint import pprint
from fake_useragent import UserAgent
from hashlib import md5
from bs4 import BeautifulSoup
from pathlib import PurePath
import pyautogui as auto

# customized module
from config import logfile,dldir
# from openlink import op_simple,ran_header
from mtag import addtag
from mylog import get_funcname,mylogger
from mp3archive import find_album,create_folder
from mytool import mywait,get_text_clipboard,clickbutton,capture
from myfs import clean_f
from myimg import squaresize
from mystr import fnamechecker as modstr
import myget

class XiaMi:
    ua = UserAgent().random
    main = "https://www.xiami.com"
    # 歌曲详情信息
    APISongDetails = "/api/song/getPlayInfo"
    APIAlbumDetails = "/api/album/getAlbumDetailNormal"
    APIAlbumNologin = "/api/album/initialize"

    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            "user-agent": self.ua
        }
        self.session.headers.update(self.headers)
        self.session.get(self.main)

    def _get_api_url(self, api):
        return self.main + api

    # 获取加密字符串_s
    def _get_params__s(self, api: str, _q: str = "") -> str:
        '''
        :param api: URL的地址
        :param _q:  需要加密的参数
        :return: 加密字符串
        '''
        xm_sg_tk = self._get_xm_sg_tk()
        # print(xm_sg_tk)
        data = xm_sg_tk + "_xmMain_" + api + "_" + _q
        _s = md5(bytes(data, encoding="utf-8")).hexdigest()
        # print(_s)
        return _s

    # 获取xm_sg_tk的值，用于对数据加密的参数
    def _get_xm_sg_tk(self) -> str:
        xm_sg_tk = self.session.cookies.get("xm_sg_tk", None)
        assert xm_sg_tk is not None, "xm_sg_tk missing"
        return xm_sg_tk.split("_")[0]

    # 获取歌曲详情信息
    def get_song_details(self, songid_list) -> dict:
        '''
        :param song_ids: 歌曲的id，可以为多个
        :return: 歌曲的详情信息
        '''
        assert len(songid_list) != 0, "song_ids cannot be Null"

        for song_id in songid_list:
            if not isinstance(song_id, int):
                raise Exception("song_id not Int")

        url = self._get_api_url(self.APISongDetails)
        _q = "{\"songIds\":%s}" % songid_list
        params = {
            "_q": _q,
            "_s": self._get_params__s(self.APISongDetails, _q)
        }
        result = self.session.get(url=url, params=params).json()
        # pprint(result)
        return result

    # 获取歌曲的下载地址
    def get_song_download_url(self, songid_list):
        download_url_dict = {}
        song_details = self.get_song_details(songid_list)
        songPlayInfos = song_details["result"]["data"]["songPlayInfos"]
        # pprint(songPlayInfos)
        for songPlayInfo in songPlayInfos:
            song_download_url = songPlayInfo["playInfos"][0]["listenFile"] or songPlayInfo["playInfos"][1]["listenFile"]
            song_id = songPlayInfo["songId"]
            download_url_dict[song_id] = song_download_url

        # print("歌曲下载地址为:", download_url_dict)
        return download_url_dict

    def download_album(self,workfolder,album_detail):
        ml = mylogger(logfile,get_funcname()) 

        artist_name = album_detail['artist_name']
        album_name = album_detail['album_name']
        year = album_detail['year']
        albumdir = f'{artist_name} - {year} - {album_name}'

        albumfulldir = create_folder(workfolder,albumdir)
        try:
            coverlink = album_detail['coverlink']
            cover = os.path.join(albumfulldir,albumdir+'.jpg')
            m_cover = os.path.join(albumfulldir,albumdir+'.png')
            if os.path.isfile(cover):
                ml.warn('---- Big Cover download already !') 
            else:
                ml.info('Download big cover')
                myget.dl(coverlink,out=cover)
            if os.path.isfile(m_cover):
                ml.warn('---- Small cover ready !') 
            else:
                shutil.copy(cover,m_cover)
                squaresize(m_cover)
            songid_list = album_detail['songid_list']
            download_url_dict = self.get_song_download_url(songid_list)
            ml.dbg(download_url_dict)
            for s in songid_list:
                singers = modstr(album_detail['song_detail_list'][s]['singers'])
                songname = modstr(album_detail['song_detail_list'][s]['songname'])
                songfullname = f'{singers} - {songname}.mp3'
                mp3 = os.path.join(albumfulldir,songfullname)
                if os.path.isfile(mp3):
                    ml.warn(f'---- {songname} download already !') 
                else:
                    cdserial = str(album_detail['song_detail_list'][s]['cdserial'])
                    track = str(album_detail['song_detail_list'][s]['track'])
                    ml.info(f'{cdserial}.{track} {singers} - {songname}')
                    if dlurl := download_url_dict[s]:
                        try:
                            myget.dl(dlurl,out=mp3)
                            mywait(random.randint(1,3))
                            addtag(mp3,songname,album_name,artist_name,singers,m_cover,year,track,cdserial)                    
                        except Exception as e:
                            print(e)
                            if "HTTP Error 404: Not Found" in str(e):
                                ml.err("File Not Found")
                            else:
                                raise
            os.remove(m_cover)
            clean_f(albumfulldir,'tmp')
            ml.info('Download Complete')
        except FileNotFoundError:
            pass

    # def get_album_details(self):
    #     url = 'https://www.xiami.com/album/jXUpa9298'
    #     headers = {
    #         "referer": url
    #     }

    #     album_id = url.split("/")[-1]
    #     print(album_id)
    #     url = self._get_api_url(self.APISongDetails)

    #     _q = "{\"albumId\":\"%s\"}" % album_id
    #     print(_q)
    #     params = {
    #         "_q": _q,
    #         "_s": self._get_params__s(self.APIAlbumNologin, _q)
    #         # "_s": "af88385b7dd456a7a161c5a276d4fc17"
    #     }
    #     self.session.headers.update({"referer": url})
    #     result = self.session.get(url=url, params=params).json()
    #     pprint(result)
    #     # bsObj = BeautifulSoup(result,"html.parser") 
    #     # album_name = bsObj.find('div',{'class':'titleInfo-name'})
    #     # album_name = modstr(album_name.text)
    #     # artist_name = bsObj.find('div',{'class':'singer-name'})
    #     # artist_name = modstr(artist_name.text)

    #     # year = bsObj.find(text="发行")
    #     # year = modstr(year.text)

    #     # print(year)

    def test(self):
        # self._get_xm_sg_tk()
        # self.get_song_details(1769449479,1813243760)
        # self.get_song_download_url(1769449479,1813243760)
        self.dl_mp3(1769449479,1813243760)
        # self.get_album_details()

        pass


def xm_json(year=None,force=True):
    '''Analyze json album data'''
    ml = mylogger(logfile,get_funcname()) 

    j = json.loads(get_text_clipboard())
    # pprint(j)
    # j = f2json(get_text_clipboard())
    j = j['result']['data']['albumDetail']
    album_detail = {}
    # if year is None:
    #     year = input('Publish year>>')
    artist_name = modstr(j['artistName'])
    album_name = modstr(j['albumName'])
    coverlink = j['albumLogo']
    album_detail['year'] = year
    album_detail['artist_name'] = artist_name
    album_detail['album_name'] = album_name
    album_detail['coverlink'] = coverlink    
    albumdir = f'{artist_name} - {year} - {album_name}'
    if find_album(albumdir) and force == False:
        ml.warn(f'{albumdir} alread archived')
        return None
    else:
        coverlink = j['albumLogo']
        cdcount = j['cdCount']
        songcount = j['songCount']
        song_detail_list = {}
        songid_list = []
        for s in range(songcount):
            songid_list.append(j['songs'][s]['songId'])
            song_detail_list[j['songs'][s]['songId']] = {
                "singers":modstr(j['songs'][s]['singers']),
                "songname":modstr(j['songs'][s]['songName']),
                "cdserial":j['songs'][s]['cdSerial'],
                "track":j['songs'][s]['track']
            }            

        # pprint(song_detail_list)
        # pprint(songid_list)
        album_detail['song_detail_list'] = song_detail_list
        album_detail['songid_list'] = songid_list
    ml.dbg(album_detail)
    return album_detail

def chromef12(year=None,autoclose=False):
    """
    Chrome F12 find xhr and close page
    ensure filter XHR
    """
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
        album_detail = xm_json(year=year)
    else:
        raise
    if autoclose:
        auto.hotkey('ctrl','w')
    return album_detail


def main():
    year = input('Publish year>>')
    if album_detail := chromef12(year):
        xm = XiaMi()
        xm.download_album(dldir, album_detail)

if __name__ == "__main__":
    main()