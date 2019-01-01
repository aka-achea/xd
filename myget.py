#!/usr/bin/python
#coding:utf-8
# Python3
# Version: 20181229

import sys , os , shutil ,datetime , math
from urllib.request import urlretrieve
from urllib.parse import urlparse



def get_console_width():
    #Code from http://bitbucket.org/techtonik/python-pager
    if os.name == 'nt':
        STD_INPUT_HANDLE  = -10
        STD_OUTPUT_HANDLE = -11
        STD_ERROR_HANDLE  = -12
        # get console handle
        from ctypes import windll, Structure, byref
        from ctypes.wintypes import SHORT, WORD, DWORD
        console_handle = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        # CONSOLE_SCREEN_BUFFER_INFO Structure
        class COORD(Structure):
            _fields_ = [("X", SHORT), ("Y", SHORT)]
        class SMALL_RECT(Structure):
            _fields_ = [("Left", SHORT), ("Top", SHORT),
                        ("Right", SHORT), ("Bottom", SHORT)]
        class CONSOLE_SCREEN_BUFFER_INFO(Structure):
            _fields_ = [("dwSize", COORD),
                        ("dwCursorPosition", COORD),
                        ("wAttributes", WORD),
                        ("srWindow", SMALL_RECT),
                        ("dwMaximumWindowSize", DWORD)]
        sbi = CONSOLE_SCREEN_BUFFER_INFO()
        ret = windll.kernel32.GetConsoleScreenBufferInfo(
            console_handle, byref(sbi))
        if ret == 0:
            return 0
        return sbi.srWindow.Right+1
    return 80



def filename_from_url(url):
    fname = os.path.basename(urlparse(url).path)
    if len(fname.strip(" \n\t.")) == 0:
        return None
    return fname

def pbar(blocks, block_size, total_size):
    if not total_size or total_size < 0:
        sys.stdout.write(str(block_size*blocks)+'\r')
        sys.stdout.flush()
    else:
        dlsize = block_size*blocks
        if dlsize > total_size: dlsize = total_size
        rate = dlsize/total_size
        # print(str(rate))
        percentrate = str(math.floor(100*rate))+'%'  
        # print(percentrate)
        # width = get_console_width()-8
        width = 40
        # dots = int(math.floor(rate*width))
        dots = int(math.floor(rate*width))

        # print(dots)
        bar = '▇'*dots+'--'*(width-dots)
        # sys.stdout.write("|"+bar+'| '+percentrate+' '+str(dlsize)+'/'+str(total_size)+'\r')
        if rate == 1:
            sys.stdout.write(bar+' '+percentrate+' '+str(dlsize)+'/'+str(total_size)+'\n')
        else:
            sys.stdout.write(bar+' '+percentrate+' '+str(dlsize)+'/'+str(total_size)+'\r')

        sys.stdout.flush()



def dl(url,out=None,pbar=pbar):     

    # detect of out is a directory
    outdir = None
    if out and os.path.isdir(out):
        outdir = out
        out = None

    if out:
        prefix = out        
    else:
        prefix = filename_from_url(url)
    # print(prefix)
    now = str(datetime.datetime.utcnow()).replace(':','')
    tmpname = prefix+now+'.tmp'
    # print(tmpname)

    local_filename, headers = urlretrieve(url,tmpname,pbar )
    # print(headers)
   
    # size = int(headers['Content-Length'])
    # # # size = size/(1024*1024)
    # print(size)    
    ftype = '.'+str(headers['Content-Type']).split('/')[1]
    # print(ftype)
    if out:
        shutil.move(tmpname,out)
    else:
        shutil.move(tmpname,prefix+now+ftype)


if __name__ == "__main__":
    # url = 'http://python.org/'
    # url = 'https://github.com/hfaran/progressive/blob/master/example.gif'
    url = 'http://m128.xiami.net/761/96761/2102654949/1795287087_1479699396518.mp3?auth_key=1546570800-0-0-c5bc8bc5db6fb85dde5e6171bd821a81'
    # url = 'https://epass.icbc.com.cn/ICBCChromeExtension.msi'

    out = 'tesget.mp3'
    # out = None
    dl(url,out)
    # print(get_console_width())
