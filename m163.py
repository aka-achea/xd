from Crypto.Cipher import AES
import base64
import random
import codecs
import requests
# from fake_useragent import UserAgent
import time
from multiprocessing import Process
from openlink import op_simple , op_requests,ran_header

class DownLoadWYY:
    # ua = UserAgent()

    def __init__(self):
        self.arg2 = "010001"
        self.arg3 = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
        self.arg4 = "0CoJUm6Qyw8W8jud"
        self.session = requests.Session()
        self.session.headers = ran_header(ref="https://music.163.com/")
        self.__get_random_str()
        # self.__init_session()

    def __init_session(self):
        '''拿到后面需要的cookies'''
        resopnse = self.session.get("https://music.163.com/#/discover/playlist", headers=self.session.headers)
        print(resopnse.headers)

    def __AES_encrypt(self, text, key):
        '''
        获取到加密后的数据
        :param text: 首先CBC加密方法，text必须位16位数据
        :param key: 加密的key
        :return: 加密后的字符串
        '''
        iv = "0102030405060708"
        pad = 16 - len(text) % 16
        if isinstance(text, str):
            text = text + pad * chr(pad)
        else:
            text = text.deocde("utf-8") + pad * chr(pad)
        aes = AES.new(key=bytes(key, encoding="utf-8"), mode=2, iv=bytes(iv, encoding="utf-8"))
        res = aes.encrypt(bytes(text, encoding="utf-8"))
        res = base64.b64encode(res).decode("utf-8")
        return res

    def __get_encText(self):

        encText = self.__AES_encrypt(self.arg1, self.arg4)
        encText = self.__AES_encrypt(encText, self.random_16_str)
        return encText

    def __get_encSecKey(self):
        '''通过查看js代码，获取encSecKey'''
        text = self.random_16_str[::-1]
        rs = int(codecs.encode(text.encode('utf-8'), 'hex_codec'), 16) ** int(self.arg2, 16) % int(self.arg3, 16)
        return format(rs, 'x').zfill(256)

    def __get_random_str(self):
        '''这是16位的随机字符串'''
        str_set = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        random_str = ""
        for i in range(16):
            index = random.randint(0, len(str_set) - 1)
            random_str += str_set[index]
        self.random_16_str = random_str

    def __getFormData(self):
        '''获取到提交的数据'''
        data = {"params": self.__get_encText(), "encSecKey": self.__get_encSecKey()}
        return data

    def downloadSong(self, songId):
        '''获取到歌曲的下载的地址就好了。如果想要下载可以单独再写一个方法去下载音乐'''
        print("开始爬取歌曲mp3地址....")
        self.arg1 = '{"ids":"[%s]","level":"standard","encodeType":"aac","csrf_token":""}' % songId
        api = "https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token="
        headers = self.session.headers.copy()
        formdata = self.__getFormData()
        response = self.session.post(url=api, data=formdata, headers=headers)
        print("歌曲的下载地址为>>:", response.json()["data"][0]["url"])

    def song_comment(self, songId):
        '''获取到歌曲评论信息，我只是将结果print出来，如果保存的话，可以单独写一个保存的方法'''
        print("开始爬取歌曲评论信息....")
        # self.arg1的格式为："{"rid":"R_SO_4_歌曲id","offset":"0","total":"true","limit":"20","csrf_token":""}"
        # 第一页为0，第二页为20，第三页为40  第四页为60  第五页为80
        offset = 0
        n = 1
        api = "https://music.163.com/weapi/v1/resource/comments/R_SO_4_{}?csrf_token=".format(songId)
        headers = self.session.headers.copy()
        while True:
            self.arg1 = '{"rid":"R_SO_4_%s","offset":"%s","total":"true","limit":"20","csrf_token":""}' % (
                songId, offset)
            formdata = self.__getFormData()
            response = self.session.post(url=api, headers=headers, data=formdata)
            # print("*"*100)
            # print("第{}页评论".format(n))
            comment_list = response.json().get("comments")
            for dic in comment_list:
                try:
                    print("用户: {}".format(dic["user"]["nickname"]))
                    print("评论内容： {} ".format(dic.get("content")))
                    print()
                except UnicodeEncodeError:
                    pass
            offset += 20
            n += 1
            time.sleep(1)


if __name__ == '__main__':
    song = DownLoadWYY()
    comment = DownLoadWYY()
    p1 = Process(target=song.downloadSong, args=(1418069679,))
    # p2 = Process(target=comment.song_comment, args=(1361348080,))

    p1.start()
    # p2.start()

    p1.join()
    # p2.join()

    print("爬取完毕...")