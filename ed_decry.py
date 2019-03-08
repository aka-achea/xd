#!/usr/bin/python3
#coding:utf-8
# tested in win

from Crypto.Cipher import AES
import base64


def aes_encrypt(text, key):
    iv = "0102030405060708"
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    result = encryptor.encrypt(text)
    result_str = base64.b64encode(encrypt_text)
    return result_str