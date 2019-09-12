import requests
from lxml import etree
import threading
from time import sleep


class Proxy:
    """
    爬取主流的几个代理网站，找到可用的代理
    """

    def __init__(self):
        self.POOL = set([])

    @staticmethod
    def _is_usable(url: str) -> bool:
        """
        判断代理是否可用
        http://60.217.140.101:8060
        """
        headers = {
            'User - Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 75.0.3770.100Safari / 537.36'
        }
        protocol = url.split(":")[0]
        soure_ip = url.split("//")[1].split(":")[0]
        proxy = {protocol: url}
        url = 'http://ip.chinaz.com/'
        # , proxies = proxy
        html = requests.get(url, headers=headers, proxies = proxy, timeout=5).text
        print(html)
        request = etree.HTML(html)
        my_ip = request.xpath('//dd[@class = "fz24"]/text()')
        print(f'访问IP为{my_ip}')
        return my_ip[0] == soure_ip
        # try:
        #     request = etree.HTML(requests.get(url, headers=header, proxies=proxy, timeout=5).text)
        #     my_ip = request.xpath('//dd[@class = "fz24"]/text()')
        #     print(f'访问IP为{my_ip}')
        #     return my_ip[0] == soure_ip
        # except:
        #     print("代理连接失败")

    def _get_proxy0(self):
        """
        免费代理IP库
        该站十秒刷新一次
        """
        link = 'http://ip.jiangxianli.com/?page='
        while True:
            for i in range(1, 4):
                request = etree.HTML(requests.get(link + str(i)).text)
                proxy = request.xpath(
                    '//tbody/tr/td/button[@class = "btn btn-sm btn-copy"]/@data-url')
                self._add(proxy)
                sleep(10)

    def _get_proxy1(self):
        """
        爬取快代理 
        国内高匿：https://www.kuaidaili.com/free/inha/1/
        国内普通：https://www.kuaidaili.com/free/intr/1/
        """
        link = 'https://www.kuaidaili.com/free/'
        ip_xpath = '//tbody/tr/td[@data-title="IP"]/text()'
        post_xpath = '//tbody/tr/td[@data-title="PORT"]/text()'
        type_xpath = '//tbody/tr/td[@data-title="类型"]/text()'

        while True:
            for j in ['intr', 'inha']:
                for i in range(1, 4):
                    request = etree.HTML(requests.get(link + j + "/" + str(i) + "/").text)
                    proxy_ip = request.xpath(ip_xpath)
                    proxy_post = request.xpath(post_xpath)
                    proxy_type = request.xpath(type_xpath)
                    proxy = [pt + "://" + pi + ":" + pp for pt, pi, pp in zip(proxy_type, proxy_ip, proxy_post)]
                    self._add(proxy)
                sleep(3 * 60)

    def _get_proxy2(self):
        """
        爬取 66免费代理  http://www.66ip.cn/1.html
        该站更新时间极其缓慢，代理质量不高
        """
        link = 'https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-'
        ip_xpath = '//table[@class="bg"]/tr/td[2]/text()'
        post_xpath = '//table[@class="bg"]/tr/td[3]/text()'
        type_xpath = '//table[@class="bg"]/tr/td[7]/text()'
        while True:
            for i in range(1, 4):
                request = etree.HTML(requests.get(link + str(i)).text)
                proxy_ip = request.xpath(ip_xpath)
                proxy_post = request.xpath(post_xpath)
                proxy_type = ['http' if i == 'no' else 'https' for i in request.xpath(type_xpath)]
                proxy = [pt + "://" + pi + ":" + pp for pt, pi, pp in zip(proxy_type, proxy_ip, proxy_post)]
                self._add(proxy)
                sleep(3 * 60)

    def _add(self, proxy: list):
        for i in proxy:
            if self._is_usable(i):
                self.POOL.add(i)
            print(self.POOL)

    def run(self):
        # t1 = threading.Thread(target=self._get_proxy0)
        # t2 = threading.Thread(target=self._get_proxy1)
        # t3 = threading.Thread(target=self._get_proxy2)
        # t1.start()
        # t2.start()
        # t3.start()
        print(self._is_usable('http://60.217.140.101:8060'))


if __name__ == '__main__':
    p = Proxy()
    p.run()
