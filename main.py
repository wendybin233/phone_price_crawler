# coding=utf-8
import sys
import requests
import urllib
from pyquery import PyQuery as pq
from lxml import etree

searchUrl =  "http://ks.pconline.com.cn/product.shtml?"

def crawl():
    param = {'q' : u'nexus 5'.encode('gb2312')}
    r = requests.get(searchUrl + urllib.urlencode(param) )
    d = pq(r.text)

    print  d('div.dRise i.big').text()




if  __name__ == '__main__':
    crawl()



