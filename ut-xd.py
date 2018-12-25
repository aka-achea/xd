#!/usr/bin/python
#coding:utf-8

import unittest,configparser,os,shutil

conf = 'E:\\xd.ini'
config = configparser.ConfigParser()
config.read(conf)
# code = config['ut']['xd_xml_decry']

import xd_xml
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

import xd_ana
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

import xd_dl
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

import arch
class Test_arch(unittest.TestCase):


    @classmethod
    def setUpClass(self):
        print('UnitTest xd_dl')
        self.root = 'E:\\UT\\xd'
        self.ttopdir = 'E:\\UT\\xd\\ttop'
        os.mkdir(self.ttopdir)
        self.tmusicure = 'E:\\UT\\xd\\tmusicure'
        os.mkdir(self.tmusicure)
        self.tevadir = 'E:\\UT\\xd\\tevadir'
        os.mkdir(self.tevadir)
        self.tcoverdir = 'E:\\UT\\xd\\tcoverdir'
        os.mkdir(self.tcoverdir)
        self.tarchdir = 'E:\\UT\\xd\\tarchdir'
        os.mkdir(self.tarchdir)
        self.tdir = 'E:\\UT\\xd\\tevadir\\t-t - 2011 - e-t'
        os.mkdir(self.tdir)
        shutil.copy(os.path.join(self.root,'t.mp3'),\
                    os.path.join(self.ttopdir,'t.mp3'))
        shutil.copy(os.path.join(self.root,'t.jpg'),\
                    os.path.join(self.ttopdir,'t.jpg'))
        shutil.copy(os.path.join(self.root,'t.jpg'),\
                    os.path.join(self.tdir,'t-t - 2011 - e-t.jpg'))



    @classmethod
    def tearDownClass(self):        
        print('Test complete')

    def test_find_art(self):
        print('find_art')
        artist = "Booker T. & the MG's"
        topdir = 'L:\\Music'
        p_art = arch.find_art(topdir,artist)
        self.assertEqual(p_art,"L:\Music\_Archived\Funk\Booker T. & the MG's")
        # print(p_art)

    
    def test_move_mp3(self):
        print('move_mp3')   
        arch.move_mp3(self.ttopdir,self.tmusicure)
        mp3 = os.path.exists(os.path.join(self.tmusicure,'t.mp3'))
        self.assertTrue(mp3)

    def test_rename_mp3(self):
        print('rename_mp3')
        arch.rename_mp3(self.tmusicure)
        mp3 = os.path.exists(os.path.join(self.tmusicure,''))
        self.assertTrue(mp3)        

    def test_archive_cd(self):
        arch.archive_cd(self.tevadir,self.tarchdir)
        t = os.path.exists('E:\\UT\\xd\\tevadir\\t-t\\t-t - 2011 - e-t')
        self.assertTrue(t)
        shutil.move('E:\\UT\\xd\\tevadir\\t-t','E:\\UT\\xd\\tarchdir\\t-t')
        t2 = 'E:\\UT\\xd\\tevadir\\t-t - 2055 - e-t'
        os.mkdir(t2)
        shutil.copy(os.path.join(self.root,'t.jpg'),\
                    os.path.join(t2,'t-t - 2055 - e-t.jpg'))
        arch.archive_cd(self.tevadir,self.tarchdir)
        t2 = os.path.exists('E:\\UT\\xd\\tarchdir\\t-t\\t-t - 2055 - e-t')
        self.assertTrue(t2)

    def test_move_cover(self):
        print('move_cover')
        arch.move_cover(self.ttopdir,self.tcoverdir)
        jpg = os.path.exists(os.path.join(self.tcoverdir,'t.jpg'))        
        self.assertTrue(jpg)

    def test_evaluate_art(self):
        pass

def run_Testarch():
    Testarch = unittest.TestSuite()
    # Testarch.addTest(Test_arch('test_find_art'))
    Testarch.addTest(Test_arch('test_move_mp3'))
    Testarch.addTest(Test_arch('test_move_cover'))
    Testarch.addTest(Test_arch('test_rename_mp3'))
    Testarch.addTest(Test_arch('test_archive_cd'))

    unittest.TextTestRunner().run(Testarch)

if __name__ == '__main__':
	# unittest.main()

    # run_Testxdxml()
    # run_Testxdana()
    # run_Testxddl()
    run_Testarch()

