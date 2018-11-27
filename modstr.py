#!/usr/bin/python
#coding:utf-8
# Python3
# version: 20181127

import mylog as ml
logfilelevel = 10 # Debug
logfile = 'E:\\app.log'

def modificate(text):
    funcname = 'modstr.modificate'    
    l = ml.mylogger(logfile,logfilelevel,funcname)     
    #file_name = re.sub(r'\s*:\s*', u' - ', file_name)    # for FAT file system
    text = str(text)    
    before = text
    text = text.replace('?', u'？')      # for FAT file system
    text = text.replace('/', u'／')
    text = text.replace('|', '')
    text = text.replace(':', u'∶')    # for FAT file system
    text = text.replace('*', u'×')
    text = text.replace('&amp;', u'&')
    text = text.replace('&#039;', u'\'')
    #text = text.replace('\'', u'＇')
    text = text.replace('\\', u'＼')
    text = text.replace('"', u'＂')
    #text = text.replace('\'', u'＇')
    text = text.strip()
    #file_name = file_name.replace('$', '\\$')    # for command, see issue #7
    after = text
    if before != after :
        l.debug("Before modify: "+before)
        l.debug("After modify: "+after)
    return text

if __name__=='__main__':
    text1 = 'ル・デ'
    modificate(text1)
    print(text1)
   
   