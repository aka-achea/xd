#!/usr/bin/python
#coding:utf-8
# Python3

from urllib.request import unquote

def decry(code): # decrypt download url
    url = code[1:]
    urllen = len(url)
    rows = int(code[0])
    cols_base = urllen // rows  #;print(cols_base) # basic column count
    rows_ex = urllen % rows #;print(rows_ex)   # count of rows that have 1 more column
    matrix = []
    for r in range(rows):
        length = cols_base + 1 if r < rows_ex else cols_base
        matrix.append(url[:length])
        url = url[length:]
    #for i in matrix : print(i)
    url = ''
    for i in range(urllen):
        url += matrix[i % rows][i // rows]
    #print(url)
    return unquote(url).replace('^', '0')


if __name__=='__main__':
    code = '5h3%2ae6FE54242258158.3h%4%E%565811f9tA28mt42%E6134FE1518mF_345%5E6Ecf228t%F.i%6151%%%11714%3pakD2E5E-3c628fp2mx.2%%E325558583553ue13%E-3f7f6ba%F1inF25%6FEE%%6_5E4%ty585-%8%166ff'
    url = decry(code)
    print(url)


# http://m32.xiami.net/646/2100013646/2104302415/1807568118_1543551088354.m4a?auth_key=1544238000-0-0-53d6341fadbb1f808f3fea098bd8dea9
# http://m64.xiami.net/646/2100013646/2104302415/1807568118_1543551088354.m4a?auth_key=1544238000-0-0-53d6341fadbb1f808f3fea098bd8dea9
# http://m320.xiami.net/646/2100013646/2104302415/1807568118_1543551088354.mp3?auth_key=1544238000-0-0-38663f0c718c6f61f266128bff2faf98
# http://m128.xiami.net/646/2100013646/2104302415/1807568118_1543551088354.mp3?auth_key=1544238000-0-0-38663f0c718c6f61f266128bff2faf98