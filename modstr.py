#!/usr/bin/python
#coding:utf-8
# Python3


def modificate(text):
    #file_name = re.sub(r'\s*:\s*', u' - ', file_name)    # for FAT file system
    text = str(text)    
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
    

    return text

if __name__=='__main__':
    import mylog as ml
    funcname = 'modstr'
    logfilelevel = 10 # Debug
    logfile = 'E:\\app.log'
    l = ml.mylogger(logfile,logfilelevel,funcname)  
    text1 = 'abc/eee'
    before = text1
    after = modificate(text1)
    if before != after :
        l.debug("Before modify: "+before)
        l.debug("After modify: "+after)