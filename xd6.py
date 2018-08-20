#!/usr/bin/python
#coding:utf-8
# Python3

import sys,os
from mylog import mylogger as ml

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
    #     l.verbose("Enable verbose log")
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
                l.verbose("Album link: "+i)
                time.sleep(5)
                html = open_link(i)
                if html == 0: continue
                single_CD_download(html)
            l.info("Artist all album downloaded !!!!!!!")
            if Emptylist:
                l.err('Empty Album list:')
                for i in Emptylist: l.err(i)
            if Faillist:
                l.err("Fail list:")
                for i in Faillist : l.err(i)
        else:
            l.err("all album link missing")

    elif sys.argv[1] == 's':
        if sys.argv[2]:
            link = sys.argv[2]
            l.info("Begin to download single album")
            #l.info("Link>> " + sys.argv[2]))
            l.verbose("Download album from page:")
            l.verbose(sys.argv[2])
            html = open_link(sys.argv[2])
            if html == 0: sys.exit()
            single_CD_download(html)
            if Emptylist:
                l.err('Empty Album list:')
                for i in Emptylist: l.err(i)
            if Faillist:
                l.err("Fail list:")
                for i in Faillist : l.err(i)
        else:
            l.err("Single album link missing")

    elif sys.argv[1] == 'f':
        if sys.argv[2].isdigit() :
            l.info("Begin Download album in update favorite list")
            for i in range(1,int(sys.argv[2])):
                nlink = url_notice+str(i)
                l.verbose(nlink)
                cdlink = favorite_CD(nlink,cookies)
                for i in cdlink :
                    l.verbose("Download album from page:")
                    l.verbose(i)
                    html = open_link(i)
                    if html == 0: continue
                    single_CD_download(html)
        else:
            l.info(Usage)

    elif sys.argv[1] == 't':
        l.info("TEST MODE")
        l.info('Start reading database')
        l.verbose('Updating records ...')
        l.err('Finish updating records')
        l.debug('Records: ')

    elif sys.argv[1] == '1':
        try:
            link = sys.argv[2]
            print(link)
            l.info("Begin Download one song")
            pass
        except:
            l.error("Song link missing")
    else:
        l.info(Usage)



if __name__=='__main__':
    
    xd()













