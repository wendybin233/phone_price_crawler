# coding=utf-8
import requests
import urllib
from pyquery import PyQuery as pq
from lxml import etree

searchUrl = "http://detail.zol.com.cn/index.php?"
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
        (mode, price, screen, cpu, memory) = crawlerImp(
            phoneBrand + ' ' + phoneId)
        if mode == 'n':
            ## not phone
            (mode, price, screen, cpu, memory) = ('n', 'n', 'n', 'n', 'n')

    prefix = id + '\t' + phoneBrand + '\t' + phoneId
    print prefix + '\t' + mode + '\t' + price + '\t' + screen + '\t' + cpu + '\t' + memory


def crawlerImp(query):

    try:
        query_encode = query.decode('utf-8').encode('gb2312')
    except:
        query_encode = query

    param = {'keyword': query_encode, 'c': 'SearchList'}
    r = requests.get(searchUrl + urllib.urlencode(param))
    d = pq(r.text)
    price = 'n'
    cpu = 'n'
    screen = 'n'
    mode = 'n'
    memory = 'n'
    if d('div.price-box').eq(0):
        price = d('div.price-box').eq(0)('b.price-type').text().encode('utf-8')
    find_more = d('ul.param').eq(0)('li a')

    if not find_more:
        return (price, cpu, screen, mode, memory)
    size = len(find_more)
    more_link = ''
    for i in range(size):
        link = find_more.eq(i)
        if link and link.text().encode('utf-8') == '更多参数>>':
            more_link = link.attr('href')

    if not more_link:
        return (price, cpu, screen, mode, memory)
    more_r = requests.get('http://detail.zol.com.cn' + more_link)
    more_d = pq(more_r.text)
    paras = more_d('ul.category_param_list li')
    size = len(paras)

    for j in range(size):
        detail = paras.eq(j)
        if not detail:
            continue

        if detail('span.param-name').text().encode('utf-8') == 'CPU型号':
            cpu = detail(
                'span.param-name').siblings('span').eq(0).text().encode('utf-8')

        elif detail('span.param-name').text().encode('utf-8') == '主屏尺寸':
            screen = detail(
                'span.param-name').siblings('span').eq(0).text().encode('utf-8')

        elif detail('span.param-name').text().encode('utf-8') == 'RAM容量':
            memory = detail(
                'span.param-name').siblings('span').eq(0).text().encode('utf-8')

        elif detail('span.param-name').text().encode('utf-8') == '4G网络':
            mode = '4G'

        elif detail('span.param-name').text().encode('utf-8') == '3G网络':
            if detail('span.param-name').siblings('span').eq(0).text().encode('utf-8').find('CDMA') > 0:
                mode = '3G'
            else:
                mode = '2G'

    return (mode, price, screen, cpu, memory)

        # find cpu
        #more_d = more_d('table.paramTable')
        # print more_d.text().encode('utf-8')


if __name__ == '__main__':
    #crawler('1', 'apple', 'iphone')
    readFile()
