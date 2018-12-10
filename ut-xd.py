#!/usr/bin/python
#coding:utf-8

import unittest,configparser,os


# customized module
import xd_xml , xd_ana,xd_dl

conf = 'E:\\xd.ini'
config = configparser.ConfigParser()
config.read(conf)
# code = config['ut']['xd_xml_decry']

class Test_xd_xml(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        print('UnitTest xd_xml')
    @classmethod
    def tearDownClass(self):
        print('Test complete')


    def test_decry(self):
        # print('Test: decry')
        code = '7h%1m28%E15_753hDE556d3a8t22iF522%417E%_12EE4cfa1tF8.6%F6264723k5%%-cdf8cp%.n9527F1997Fe255%955cf%2xe%E1615%7.ay4EE5259a3Fit26%77458mu%%4-E2215Ama%F95697E%pt35%%-d7b9'
        url = xd_xml.decry(code)
        # print(url)
        self.assertEqual(url[:4],'http')

    def test_get_loc_one(self):
        # print('Test: loc_one')
        song_id = str(1795287087)
        d = xd_xml.get_loc_one(song_id)  
        album = d['album']
        self.assertEqual(album,'有你的快递')

    def test_get_loc_cd(self):
        # print('Test: loc_cd')
        song_id = str(1795287087)
        d = xd_xml.get_loc_cd(song_id)  
        song = d['song']
        self.assertEqual(song,'有你的快递')

def run_Testxdxml():
    Testxdxml = unittest.TestSuite()
    Testxdxml.addTest(Test_xd_xml('test_decry'))
    Testxdxml.addTest(Test_xd_xml('test_get_loc_one'))
    Testxdxml.addTest(Test_xd_xml('test_get_loc_cd'))
    unittest.TextTestRunner().run(Testxdxml)

class Test_xd_ana(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        print('UnitTest xd_ana')
    @classmethod
    def tearDownClass(self):
        print('Test complete')

    def test_ana_song(self):
        weburl = 'https://www.xiami.com/song/1798102569?spm=a2oj1.12028094.0.0.ba054ca2H9ui3w'
        songid = xd_ana.ana_song(weburl)
        self.assertEqual(songid,'1798102569')

    def test_ana_cd(self):
        page = 'file:\\\E:\\UT\\xd_ana.ana_cd.html'
        aDict = xd_ana.ana_cd(page)
        self.assertEqual(aDict['Discs'],2)
        self.assertEqual(aDict['year'],'2006')
        self.assertEqual(aDict[('2', '21')],'1769948526')

def run_Testxdana():
    Testxdana = unittest.TestSuite()
    Testxdana.addTest(Test_xd_ana('test_ana_song'))
    Testxdana.addTest(Test_xd_ana('test_ana_cd'))
    unittest.TextTestRunner().run(Testxdana)

class Test_xd_dl(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        print('UnitTest xd_dl')
    @classmethod
    def tearDownClass(self):
        
        print('Test complete')

    def test_dl_one(self):
        weburl = 'https://www.xiami.com/song/1798102569?spm=a2oj1.12028094.0.0.ba054ca2H9ui3w'
        workfolder = 'E:\\UT' 
        xd_dl.dl_one(weburl,workfolder)
        mp3 = os.path.join(workfolder,'Ray Charles - The Thing.mp3')
        # print(mp3)
        self.assertTrue(os.path.exists(mp3))
        os.remove(mp3)

    def test_dl_cd(self):
        pass

def run_Testxddl():
    Testxddl = unittest.TestSuite()
    Testxddl.addTest(Test_xd_dl('test_dl_one'))
    Testxddl.addTest(Test_xd_dl('test_dl_cd'))
    unittest.TextTestRunner().run(Testxddl)


if __name__ == '__main__':
	# unittest.main()

    # run_Testxdxml()
    # run_Testxdana()
    run_Testxddl()