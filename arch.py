#!/usr/bin/python
#coding:utf-8
# Python3


import os,re




def path_art(artist):
    topdir = 'C:\\D'
    for dirpath, dirnames, files in os.walk(topdir):
        for name in dirnames:
            if name == artist:
                path = os.path.join(dirpath, name)

    return path #return last result


def archive_al():
    topdir = 'C:\\D'
    for dirname in os.listdir(topdir):        
        if os.path.isdir(os.path.join(topdir, dirname)) == True:
            # print(dirname)
            m = re.split('\s\-\s\d{4}\s\-\s',str(dirname))
            if len(m) == 2:
                print(m[0])
            # album = str(dirname).split(" - ")
            # if len(album) == 3:
            #     print(album)
            # p_art = path_art(dirname)
            # if p_art  




if __name__=='__main__':
    # path = path_art("SCCM")
    # print(path)
    archive_al()

