#!/usr/bin/python3
#coding:utf-8
#version:20190729
# tested in win

# from Crypto.Cipher import AES
# from Crypto.Util.Padding import pad

from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
import base64 , requests, sys
import codecs

from openlink import ran_header

# headers = {
#     'Cookie': 'appver=1.5.0.75771;',
#     # 'Referer': 'http://music.163.com/',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
# }

first_param = "{\"ids\":\"[%d]\",\"br\":128000,\"csrf_token\":\"\"}"
second_param = "010001"
third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
forth_param = "0CoJUm6Qyw8W8jud"
rankey = 16 * 'F'
encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"


def RSA_en(value,text,modulus): # not in use
    text = text[::-1]
    rs = int(codecs.encode(text.encode('utf8'),'hex_codec'),16) ** int(value,16) % int(modulus,16)
    return format(rs,'x').zfill(256)


def get_params(first_param):
    '''twice AES encrypt against songid'''
    iv = "0102030405060708"
    first_key = forth_param
    second_key = 16 * 'F'  # as random str
    h_encText = AES_encrypt(first_param, first_key, iv)
    h_encText = AES_encrypt(h_encText, second_key, iv)
    return h_encText


def AES_encrypt(text, key, iv): 
    '''Return encoded bytes'''
    pad = 16 - len(text) % 16
    if isinstance(text, str):
        # print('Is string')
        text = text + pad * chr(pad)
    else:
        # print('Not string')
        text = text.decode('utf-8') + pad * chr(pad)
    encryptor = AES.new(key.encode("utf8"), AES.MODE_CBC, iv.encode("utf8"))
    encrypt_text = encryptor.encrypt(text.encode("utf8"))
    encrypt_text = base64.b64encode(encrypt_text)
    return encrypt_text


def get_json(url, params, encSecKey):
    '''Get response of song download url'''
    data = {
        "params": params,
        "encSecKey": encSecKey
    }
    response = requests.post(url,headers=ran_header(),data=data).json()
    return response['data']


def get_dlurl(id):
    '''Input song id , Return song download link'''
    first_param = "{\"ids\":\"[%d]\",\"br\":128000,\"csrf_token\":\"\"}" % int(id)
    url = 'https://music.163.com/weapi/song/enhance/player/url?csrf_token='
    params = get_params(first_param)   
    # encSecKey = RSA_en(second_param,rankey,third_param)  # not in use
    rsp = get_json(url, params, encSecKey)
    music_url = rsp[0].get('url')
    return music_url




if __name__ == "__main__":
    id = '1352163999'
    music_url = get_dlurl(id)
    print(music_url)

    # import myget
    # myget.dl(music_url)
