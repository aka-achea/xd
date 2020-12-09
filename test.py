
import requests
from pprint import pprint
from fake_useragent import UserAgent
from hashlib import md5
from bs4 import BeautifulSoup

from mystr import fnamechecker as modstr
import myget


tk = "fd2b79b5d409ca9e0fb2d843331813b0"


def _get_params__s() -> str:
    '''
    :param api: URL的地址
    :param _q:  需要加密的参数
    :return: 加密字符串
    '''
    _q = "{\"albumId\":\"jXUpa9298\"}"
    xm_sg_tk = "fd2b79b5d409ca9e0fb2d843331813b0"
    print(xm_sg_tk)
    data = xm_sg_tk + "_xmMain_" + "/api/album/initialize" + "_" + _q
    return md5(bytes(data, encoding="utf-8")).hexdigest()

print(_get_params__s())


