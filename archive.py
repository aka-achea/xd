#!/usr/bin/python
#coding:utf-8
# Python3


import os,re,shutil,argparse,configparser

# customized module
from comm import readtag , f_move
# import mylog as ml
import myfs
from mylognew import get_funcname, mylogger

confile = 'L:\\MUSIC\\xd.ini'
config = configparser.ConfigParser()
config.read(confile)
topdir = config['arch']['topdir']
archdir = config['arch']['archdir']
evadir = config['arch']['evadir']
coverdir = config['arch']['coverdir']
musicure = config['arch']['musicure']
inventory =  config['arch']['inventory']
logfile = config['log']['logfile']
logfilelevel = int(config['log']['logfilelevel'])

# def find_art(topdir,artist):
#     funcname = 'arch.find_art'
#     l = mylogger(logfile,logfilelevel,funcname) 
#     p_art = ''
#     for dirpath, dirnames, files in os.walk(topdir):
#         for name in dirnames:
#             l.debug(name)
#             if name == artist:
#                 p_art = os.path.join(dirpath, name)
#     return p_art #return last result

def find_art(artist,inventory):
    p_art = ''
    if artist[-1] == '.':  # windows folder name cannot end with .
        artist = artist[:-2] 
    with open(inventory,'r') as f:        
        a = f.readlines()
        for i in a:
            if artist == i.strip().split('\\')[-1]:
                p_art = i.strip()
                break
    return p_art

def build_inv(archdir):        
    with open(inventory,'w') as f:
        for pdir in os.listdir(archdir):
            pdir = os.path.join(archdir,pdir)
            for adir in os.listdir(pdir):
                if adir !=  '_VA':               
                    f.write(os.path.join(pdir,adir)+'\n')

def rename_mp3(topdir):
    funcname = 'arch.rename_mp3'
    l = mylogger(logfile,logfilelevel,funcname) 
    for mp3 in os.listdir(topdir):        
        p_mp3 = os.path.join(topdir,mp3)
        if p_mp3[-3:] == 'mp3':
            # print(mp3[:-3])
            d = readtag(p_mp3)
            singer = str(d[0])
            title = str(d[1])
            songname = singer+' - '+title+'.mp3'
            if mp3 != songname:
                l.info('Change '+mp3+'  --->  '+songname)
                src = p_mp3
                dst = os.path.join(topdir,songname)
                l.debug(src)
                l.debug(dst)
                os.rename(src,dst)

def archive_cd(evadir,archdir):
    funcname = 'arch.archive_cd'
    l = mylogger(logfile,logfilelevel,funcname)     
    for dirname in os.listdir(evadir):  
        al_src = os.path.join(evadir, dirname)             
        if os.path.isdir(al_src) == True:
            l.debug(al_src)
            m = re.split('\s\-\s\d{4}\s\-\s',str(dirname))
            if len(m) == 2: #find album
                pic_src = os.path.join(evadir,dirname,dirname+'.jpg')
                l.debug('Cover from '+pic_src)
                pic_dst = os.path.join(evadir,dirname+'.jpg')
                l.debug('Cover to '+pic_dst)
                if os.path.exists(pic_dst) == False: 
                    shutil.copyfile(pic_src,pic_dst) 
                l.info('Searching Artist: '+m[0])
                p_art = find_art(m[0],inventory)
                l.debug(p_art)
                if os.path.isdir(p_art) == True :
                    # l.info(p_art)
                    l.info('Archive '+dirname)
                    al_dst = p_art
                    l.debug(al_dst)                                
                elif os.path.isdir(os.path.join(evadir, m[0])) == True:
                    l.warning('Already prearchive -> move album '+dirname)
                    al_dst = os.path.join(evadir,m[0])
                else:
                    l.warning('Prearchive '+m[0]+' -> move album '+dirname)
                    os.mkdir(os.path.join(evadir, m[0]))
                    al_dst = os.path.join(evadir, m[0])
                myfs.d_move(al_src,al_dst)
                if os.path.isdir(os.path.join(al_dst,m[0])) == True: 
                    l.info("Archive complete") 

def move_mp3(topdir,musicure):
    funcname = 'arch.move_mp3'
    l = mylogger(logfile,logfilelevel,funcname)    
    for mp3 in os.listdir(topdir):
        if mp3[-3:] == 'mp3':
            l.info('Move --> '+mp3)
            src = os.path.join(topdir,mp3)
            dst = os.path.join(musicure,mp3)
            l.debug(src)
            l.debug(dst)
            shutil.move(src,dst)

def move_cover(evadir,coverdir):
    funcname = 'arch.move_cover'
    l = mylogger(logfile,logfilelevel,funcname)        
    for jpg in os.listdir(evadir):
        if jpg[-3:] == 'jpg':
            l.info('Move --> '+jpg)
            src = os.path.join(evadir,jpg)
            dst = os.path.join(coverdir,jpg)
            l.info(src)
            l.info(dst)
            shutil.move(src,dst)

#move a-z, manuel check others
def arch_cover(coverdir):
    funcname = 'arch.arch_cover'
    l = mylogger(logfile,logfilelevel,funcname)
    for c in os.listdir(coverdir):
        src = os.path.join(coverdir,c)
        if os.path.isdir(src) == False:
            l.debug(src)    
            dd = os.path.join(coverdir,c[0])     
            if os.path.isdir(dd) == True:
                dst = os.path.join(dd,c)
                l.debug(dst)
                f_move(src,dst)          

def evaluate_art(evadir,musicure):
    funcname = 'arch.evaluate_art'
    l = mylogger(logfile,logfilelevel,funcname)
    for art in os.listdir(evadir):
        if os.path.isdir(os.path.join(evadir,art)) == True:
            l.info('='*20)
            l.info('Evaluate '+art)
            n = 0
            for dirpath, dirnames, files in os.walk(musicure):
                for name in files:
                    #bug name contain -
                    if str(name).split('-')[0].strip() == art:
                        l.info(name)
                        n += 1
            if n == 0:    
                l.warning('Zero !!! Track ---> Move to misc')
            else:
                an = len(os.listdir(os.path.join(evadir,art)))
                rate = str(n/an)[:4]                
                if float(rate) < 0.5:
                    l.warning('Rate '+rate+' from '+str(an)+' Album --> One more CD to evaluate ')
                else:           
                    l.info('Rate '+rate+' from '+str(an)+' Album --> Total '+str(n)+' Tracks') 

def main():
    funcname = 'arch.main'
    l = mylogger(logfile,logfilelevel,funcname) 
    parser = argparse.ArgumentParser(description = 'Archive music tool')
    parser.add_argument('-a',action="store_true", help='Archive CD')
    parser.add_argument('-e',action="store_true", help='Evaluate artist')
    parser.add_argument('-r',action="store_true", help='Rename MP3')
    parser.add_argument('-m',action="store_true", help='Move MP3')
    parser.add_argument('-f',action="store_true", help='Find Artist')
    parser.add_argument('-c',action="store_true", help='Archive CD Cover')
    parser.add_argument('-i',action="store_true", help='Build Inventory')
    args = parser.parse_args()

    if args.a :
        print('Archive CD')
        archive_cd(evadir,archdir)
        move_cover(evadir,coverdir)

    elif args.e:
        print('Evaluate artist')
        evaluate_art(evadir,musicure)

    elif args.r:
        print('Rename MP3')
        rename_mp3(topdir)

    elif args.m:
        print('Move MP3')
        move_mp3(topdir,musicure)

    elif args.f:
        artist = input("Find Artist:  ")
        path = find_art(topdir,artist)
        l.info(path)

    elif args.i:
        print('Build Inventory')
        build_inv(archdir)

    elif args.c: 
        arch_cover(coverdir)

    else:
        parser.print_help()



if __name__ == "__main__":
    main()
    # p =    find_art('Elyonbeats',r'L:\Music\MI.txt')
    # print(p)