import requests
from lxml import etree
import threading
from time import sleep

class Proxy:
    """
    爬取主流的几个代理网站，找到可用的代理
    """

    def __init__(self):
        self._proxy = []
        self.POOL = []


    @staticmethod
    def _is_usable(url: str) -> bool:
        """
        判断代理是否可用
        """
        protocol = url.split(":")[0]
        soure_ip = url.split("//")[1].split(":")[0]
        proxy = {protocol: url}
        url = 'http://ip.chinaz.com/'
        try:
            request = etree.HTML(requests.get(url, proxies=proxy,timeout=3).text)
            my_ip = request.xpath('//dd[@class = "fz24"]/text()')
            print(my_ip)
            return my_ip[0] == soure_ip
        except:
            print("代理连接失败")
        
        

    def _get_proxy0(self):
        """
        免费代理IP库第一页代理，后面的基本不能用
        该站十秒刷新一次
        """
        link = 'http://ip.jiangxianli.com/'
        while True:
            request = etree.HTML(requests.get(link).text)
            proxy = request.xpath(
                '//tbody/tr/td/button[@class = "btn btn-sm btn-copy"]/@data-url')
            self._proxy.extend(proxy)
            sleep(10)


    def _add(self):
        while True:
            if self._proxy:
                for i in self._proxy:
                    if self._is_usable(i):
                        self.POOL.append(i)
                    print(self.POOL)


    def run(self):
        t1 = threading.Thread(target=self._get_proxy0)
        t2 = threading.Thread(target=self._add)
        t1.start()
        t2.start()
        self._get_proxy0()
        # self._is_usable('http://115.206.104.143:8060')

if __name__ == '__main__':
    p = Proxy()
    p.run()
