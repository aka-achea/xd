#!/usr/bin/python
#coding:utf-8
# Python3

import sys,os
from mylog import mylogger as ml
from xd_dl import dl_album,dl_one

logfilelevel = 10 # Debug
logfile = 'E:\\app.log'
l = ml(logfile,logfilelevel,__name__) 

   




def xd():
    Usage = "Usage:\n\
xd a <Artist Link> [vv]\n\
xd s <Album Link> [vv]\n\
xd 1 <Single Song Link> [vv]\n\
xd f <Favorite Page Number>\n\
"
    # print(sys.argv)
    # print(len(sys.argv))
    if len(sys.argv) < 2:
        l.info(Usage)
        sys.exit()

    # if sys.argv[-1] == 'v':
    #     l.debug("Enable verbose log")
    # elif sys.argv[-1] == 'vv':
    #     l.debug("Enable debug log")

    if sys.argv[1] == 'a':
        if sys.argv[2]:
            link = sys.argv[2]
            l.info("Begin to download all artist album")
            #l.info("Link>> " + link))
            CD_list = get_all_CD(link)
            for i in CD_list:
                tracknum = int(0)
                l.debug("Album link: "+i)
                time.sleep(5)
                html = open_link(i)
                if html == 0: continue
                single_CD_download(html)
            l.info("Artist all album downloaded !!!!!!!")
            if Emptylist:
                l.error('Empty Album list:')
                for i in Emptylist: l.error(i)
            if Faillist:
                l.error("Fail list:")
                for i in Faillist : l.error(i)
        else:
            l.error("all album link missing")



    # elif sys.argv[1] == 'f':
    #     if sys.argv[2].isdigit() :
    #         l.info("Begin Download album in update favorite list")
    #         for i in range(1,int(sys.argv[2])):
    #             nlink = url_notice+str(i)
    #             l.debug(nlink)
    #             cdlink = favorite_CD(nlink,cookies)
    #             for i in cdlink :
    #                 l.debug("Download album from page:")
    #                 l.debug(i)
    #                 html = open_link(i)
    #                 if html == 0: continue
    #                 single_CD_download(html)
    #     else:
    #         l.info(Usage)

    # elif sys.argv[1] == 't':
    #     l.info("TEST MODE")
    #     l.info('Start reading database')
    #     l.debug('Updating records ...')
    #     l.error('Finish updating records')
    #     l.debug('Records: ')

    elif sys.argv[1] == 's':
        try:
            link = sys.argv[2]
            l.info("Begin to download single album")
            #l.info("Link>> " + sys.argv[2]))
            l.debug("Download album from page:")
            l.debug(sys.argv[2])
            html = open_link(sys.argv[2])
            html = web # for test
            if html == 0: sys.exit()
            dl_album(html)
            if Emptylist:
                l.error('Empty Album list:')
                for i in Emptylist: l.error(i)
            if Faillist:
                l.erroror("Fail list:")
                for i in Faillist : l.error(i)
        except:
            l.error("Album link missing")

    elif sys.argv[1] == '1':
        try:
            link = sys.argv[2]
            link = web # for test
            print(link)
            l.info("Begin Download one song")
            dl_one(link)            
        except:
            l.erroror("Song link missing")
    else:
        l.info(Usage)



if __name__=='__main__':
    
    web = 'file:///E://1.html'
    xd()













