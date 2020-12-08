#!/usr/bin/python3
#coding:utf-8
# test in Win

__version__ = 20201207

import requests
import pprint
from fake_useragent import UserAgent
from hashlib import md5


ua = UserAgent()
refer = "https://www.xiami.com"

APISongDetails = "/api/song/getPlayInfo"



session = requests.Session()
headers = {
    "user-agent": ua.random
}
session.get(refer)

def _get_api_url(api):
    return refer + api

def _get_params__s(api: str, tk: str, _q: str = "") -> str:
    """
    Get _s
    :param api: URL API
    :param _q:  payload
    :return: md5 digest
    """
    data = tk + "_xmMain_" + api + "_" + _q
    return md5(bytes(data, encoding="utf-8")).hexdigest()

def _get_xm_sg_tk(session) -> str:
    """
    Get xm_sg_tk from cookies
    """
    xm_sg_tk = session.cookies.get("xm_sg_tk", None)
    assert xm_sg_tk is not None, "xm_sg_tk missing"
    return xm_sg_tk.split("_")[0]

def get_song_details(*song_ids) -> dict:
    '''
    :param song_ids: can be multiple
    :return: Song details
    '''
    assert len(song_ids) != 0, "song_ids cannot be None"

    for song_id in song_ids:
        if not isinstance(song_id, int):
            raise Exception("Not Int")

    url = refer + APISongDetails
    _q = "{\"songIds\":%s}" % list(song_ids)
    params = {
        "_q": _q,
        "_s": _get_params__s(APISongDetails,tk,_q)
    }
    result = session.get(url=url, params=params).json()
    return _dispose(result)


if __name__ == "__main__":
    ss = _get_session()
    tk = _get_xm_sg_tk(ss)
    _s = 
    print(tk)