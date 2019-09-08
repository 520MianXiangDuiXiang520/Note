from urllib import request
from urllib import parse

# url = 'https://www.baidu.com'

# resp = request.urlopen(url)
# request.urlretrieve(url, 'baidu.html')
# print(resp.read().decode('utf-8'))

# s = {'key':"哈哈哈"}
# urls = parse.urlencode(s)
# print(urls)
# print(parse.parse_qsl(urls))
# print(parse.parse_qs(urls))
# key = %E5 % 93 % 88 % E5 % 93 % 88 % E5 % 93 % 88
# [('key', '哈哈哈')]
# {'key': ['哈哈哈']}

proxy = {'http': '171.13.200.149:9999'}
url = 'https://httpbin.org/ip'
hander = request.ProxyHandler(proxy)
opener = request.build_opener(hander)
resp = opener.open(url)
print(resp.read().decode('utf-8'))
