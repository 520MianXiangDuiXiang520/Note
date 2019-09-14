import requests
from lxml import etree
import threading

class IsUsable:
    """
    判断代理是否可用
    """
    def __init__(self, url: str):
        self.url = url

    def zhanzhang(self):
        url = self.url
        protocol = url.split(":")[0]
        soure_ip = url.split("//")[1].split(":")[0]
        print(soure_ip)
        proxy = {protocol: url}
        try:
            html = requests.get('http://ip.chinaz.com/', proxies=proxy, timeout=15).html
        except:
            print("代理连接超时")
        else:
            request = etree.HTML(html)
            my_ip = request.xpath('//dd[@class = "fz24"]/text()')
            print(f'访问IP为{my_ip}')

    def httpbin(self):
        url = self.url
        protocol = url.split(":")[0]
        soure_ip = url.split("//")[1].split(":")[0]
        print(soure_ip)
        proxy = {protocol: url}
        url = 'http://httpbin.org/ip'
        try:
            html = requests.get(url, proxies=proxy, timeout=15).json()
        except:
            print("代理连接超时")
        else:
            print(html)


if __name__ == '__main__':
    i = IsUsable('http://115.233.210.218:808')
    t1 = threading.Thread(target=i.httpbin)
    t2 = threading.Thread(target=i.zhanzhang)
    t1.start()
    t2.start()
