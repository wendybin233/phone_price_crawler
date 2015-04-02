# coding=utf-8
import sys
import requests
import urllib
from pyquery import PyQuery as pq
from lxml import etree

searchUrl =  "http://ks.pconline.com.cn/product.shtml?"
phone_id_name = "phone.txt"


def readFile():

    fin = open(phone_id_name, 'r')
    for line in fin:
        if not line:
            continue
        keys = line.strip().split('\t')
        if not keys:
            continue
        crawler(keys[0], keys[1], keys[2])



def crawler(id, phoneBrand, phoneId):
    query = phoneBrand + phoneId
    param = {'q' : query.decode('utf-8').encode('gb2312')}
    r = requests.get(searchUrl + urllib.urlencode(param) )
    d = pq(r.text)

    result = d('div.dRise i.big').eq(0)

    prefix = id + '\t' + phoneBrand + '\t' + phoneId
    if result:
        print prefix + '\t' + result.text().encode('utf-8')
    else:
        print prefix + '\t' + '无'





if  __name__ == '__main__':
    readFile()



