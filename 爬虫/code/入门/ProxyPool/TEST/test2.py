import requests
import threading
from lxml import etree


POOL = []
LOCK = threading.Lock()


def get_proxy0():
    link = 'http://ip.jiangxianli.com/?page='
    for i in range(1, 4):
        request = etree.HTML(requests.get(link + str(i)).text)
        proxy = request.xpath(
            '//tbody/tr/td/button[@class = "btn btn-sm btn-copy"]/@data-url')
        POOL.extend(proxy)


def is_usable():
    while True:
        if len(POOL) > 0:
            with LOCK:
                url = POOL.pop()
                protocol = url.split(":")[0]
                # soure_ip = url.split("//")[1].split(":")[0]
                proxy = {protocol: url}
            # try:
            #     html = requests.get('http://ip.chinaz.com/', proxies=proxy, timeout=15).html
            # except:
            #     print(f"{proxy}超时")
            # else:
            #     request = etree.HTML(html)
            #     my_ip = request.xpath('//dd[@class = "fz24"]/text()')
            #     print(f'访问IP为{my_ip}')
            try:
                html = requests.get(url, proxies=proxy, timeout=15).json()
            except:
                pass
            else:
                print(html)


Thread_POOL = []
t0 = threading.Thread(target=get_proxy0)
for i in range(15):
    t = threading.Thread(target=is_usable)
    Thread_POOL.append(t)

t0.start()
for i in Thread_POOL:
    i.start()

