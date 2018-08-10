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
    code = '7h%1m28%E15_753hDE556d3a8t22iF522%417E%_12EE4cfa1tF8.6%F6264723k5%%-cdf8cp%.n9527F1997Fe255%955cf%2xe%E1615%7.ay4EE5259a3Fit26%77458mu%%4-E2215Ama%F95697E%pt35%%-d7b9'
    url = decry(code)
    print(url)


