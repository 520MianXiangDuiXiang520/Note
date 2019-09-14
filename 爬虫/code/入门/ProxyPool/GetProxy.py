import requests
from lxml import etree
from time import sleep

class GetProxy:
    def __init__(self):
        pass

    def get_proxy0(self):
        """
        免费代理IP库
        该站十秒刷新一次
        """
        link = 'http://ip.jiangxianli.com/?page='
        for i in range(1, 4):
            request = etree.HTML(requests.get(link + str(i)).text)
            proxy = request.xpath(
                '//tbody/tr/td/button[@class = "btn btn-sm btn-copy"]/@data-url')
            print(proxy)
            return proxy

if __name__ == '__main__':
    s = GetProxy()
    s.get_proxy0()