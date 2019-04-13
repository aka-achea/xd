module list:
sharemod.py - shared function and varies
archive.py - archive mp3 
mtag.py - handle tag for mp3
xd.py - consolidation for xiami job
xd_ana.py - analyze xiami album , single song page
xd_xml.py - get xiami song location from id
xd_dl.py - create folder, download song
qd.py - consolidation for QQ music job
qd_ana.py - analyze QQ music album, single song page
qd_dl.py - download QQ music
ed.py - consolidation for QQ music job
ed_dl.py - download EasyNet music
ed_ana.py - anaylze EasyNet music

Bug list:
#bug: RecursionError: maximum recursion depth exceeded


QQ Music:
https://www.jianshu.com/p/b26c0c9c6149
https://www.cnblogs.com/daxiangxm/p/qq_music_api.html

Xiami Music:
https://kanoha.org/2011/08/30/xiami-absolute-address/

NetEasy Music:
https://mp.weixin.qq.com/s/c9CNf-iHPHf0tOtel0euPA



Change log:
2019.4.13 rebuild xiami download with old json api v6.8
2019.3.24 fix QQ duplicate name issue v6.7
2019.3.23 apply PEP8 v6.6
2019.3.9 add album inventory function v6.5
2019.3.6 fix some bugs, add QQ song function v6.4
2019.3.5 fix bug for QQ music download v6.3
2019.1.22 optimize argparse v6.2
2019.1.10 switch to myget, newlog v6.1
2019.1.7 fix name bug v6.0
2019.1.6 bug fix v5.9
2019.1.1 add inventory function, optimize unittest v5.8
2018.12.30 add archive cd cover function v5.7
2018.12.25 add unittest for arch.py v5.6
2018.12.24 optimize multiple cd download v5.5
2018.12.10 fix xm mass track issue v5.4
2018.12.8 add unittest for xd_xml v5.3
2018.12.5 rewrite arch.py with argparse,configparser v5.2
2018.12.4 rewrite xd with argparse v5.1
2018.12.2 rewrite xd_ana,xd_dl, since page change v5.0
2018.10.22 add read mp3 tag and rename mp3 function v4.9
2018.10.18 build archive function v4.8
2018.8.23 build basic download function for QQ music v4.7
2018.8.18 fix unpublished track issue v4.6
2018.8.17 fix multi disc issue v4.5
2018.8.16 rebuild xml analysis v4.4
2018.8.15 rebuild album analysis v4.3
2018.8.4 optimize mylog v4.2
2018.4.11 optimize log module, split modstr,decry module v4.1
2018.4.9 split log module v4.0
2018.1.20 fix 404 error v3.9
2018.1.19 add cookie, favorite download v3.8
2018.1.2 fix log handler, songName issue v3.7
2017.12.31 remove empty album, add EP album v3.6
2017.12.30 add decorator v3.5
2017.12.29 change logger, color theme v3.4
2017.12.28 upgrade header v3.3
2017.8.13 add __init__ v3.2
2017.7.31 fix file name length issue v3.1
2017.7.17 workaround JSON index issue v3.0
2017.7.16 fix pagelist bug v2.9
2017.7.15 fix trackid, no publish issue v2.8
2017.7.13 fix character "', add debug mode v2.7
2017.7.12 fix pagelist 0 issue v2.6
2017.7.9 add verbose log mode v2.5
2017.7.8 add color theme v2.4
2017.7.2 change input method v2.3
2017.6.28 get_allalbum function v2.2
2017.6.26 upgrade to Python3 v2.1
2017.4.9 fix small cover download issue v2.0
2017.4.8 fix multi disc, character ・ issue v1.9
http://www.crifan.com/unicodeencodeerror_gbk_codec_can_not_encode_character_in_position_illegal_multibyte_sequence/
2017.4.6 fix character ?/: in name v1.8
2017.3.20 embed cover, disc number to tag v1.7
2017.3.19 JSON link dead, change download approach v1.6
2017.3.4 workaround special character failure issue in songname v1.5
2017.2.26 fix cover_b_url corruption,windows tag compatibility and track number issue v1.4
2017.2.25 extract trackid, add tagging function v1.3
2017.2.19 extract CD_id, artist_name, CD_id, year v1.2
2017.2.18 auto select download quality HIGH v1.1
2017.2.14 build basic download function v1.0
