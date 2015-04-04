# coding=utf-8
import requests
import urllib
from pyquery import PyQuery as pq
from lxml import etree

searchUrl = "http://ks.pconline.com.cn/product.shtml?"
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
    (mode, price, screen, cpu, memory) = crawlerImp(phoneId)
    if mode == 'n':
        (mode, price, screen, cpu, memory) = crawlerImp(phoneBrand + ' ' + phoneId)
        if mode == 'n':
            ## not phone
            (mode, price, screen, cpu, memory)  = ('n', 'n', 'n', 'n', 'n')

    prefix = id + '\t' + phoneBrand + '\t' + phoneId
    print prefix + '\t' + mode + '\t' + price + '\t' + screen + '\t' + cpu + '\t' + memory


def crawlerImp(query):
    price = 'n'
    cpu = 'n'
    screen = 'n'
    mode = 'n'
    memory = 'n'
    try:
        query_encode = query.decode('utf-8').encode('gb2312')
    except:
        query_encode = query
    param = {'q': query_encode}
    r = requests.get(searchUrl + urllib.urlencode(param))
    d = pq(r.text)
    
    if d('div.dRise i.big').eq(0):
        price = d('div.dRise i.big').eq(0).text().encode('utf-8')
    find_more = d('dl.dlInfor').eq(0)
    if not find_more:
        return (price, cpu, screen, mode, memory)
    more_link = find_more('span a').eq(0)
    if more_link and more_link.text().encode('utf-8') == '更多参数>>':
        more_link = more_link.attr('href')
        k = more_link.rfind('/')
        more_3g_link = 'http://product.3g.pconline.com.cn/mobile/motorola/' + \
            more_link[k+1:]

        more_r = requests.get(more_3g_link.encode('utf-8'))
        more_d = pq(more_r.text)

        size = len(more_d('p'))

        for i in range(size):
            detail = more_d('p').eq(i).text().encode('utf-8')
            # print detail
            if not detail:
                continue
            if detail.find('CPU：') == 0:
                cpu = detail[detail.find('CPU：') + len('CPU：'):]
            elif detail.find('主屏尺寸：') == 0:
                screen = detail[detail.find('主屏尺寸：') + len('主屏尺寸：'):]
            elif detail.find('运行内存：') == 0:
                memory = detail[detail.find('运行内存：') + len('运行内存：'):]
            elif detail.find('4G网络') == 0:
                mode = '4G'
            elif detail.find('2G/3G网络：') == 0:
                if detail.find('CDMA') > 0:
                    mode = '3G'
                else:
                    mode = '2G'

    return (mode, price, screen, cpu, memory)

        # find cpu
        #more_d = more_d('table.paramTable')
        # print more_d.text().encode('utf-8')


if __name__ == '__main__':
    #crawler('1', '米錡    M228', '3200')
    readFile()
