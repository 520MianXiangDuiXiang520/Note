<!--961032830987546d0e6d54829fc886f6-->

目录(Catalo)

* [尚方宝剑-requests库](#%E5%B0%9A%E6%96%B9%E5%AE%9D%E5%89%91-requests%E5%BA%93)

<!--a46263f7a69f33f39fc26f907cdb773a-->
# 尚方宝剑-requests库

get请求

```python
import requests

url=""
headers={}
request=requests.get(url,headers=headers)

```

post请求

```python
import requests

data={'key1':value,'key2'；value2}
url=""
request=requests.post(url,data=data)

```

get和post一般都要带上headers信息，headers复制太麻烦？可以试试用字典生成式->

```python
# 直接从浏览器复制下来headers，保存为多行字符串
header='''accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9
cache-control: max-age=0
cookie: _ga=GA1.2.1934859142.1553158342; __gads=ID=bb2c52e7f95e20ea:T=1553158342:S=ALNI_MbCqantLKdwLUa38oG6ZMcHeLfCjA; sc_is_visitor_unique=rx9614694.1553935711.DBD9700252C94FAFBCEA644716871ED5.1.1.1.1.1.1.1.1.1; UM_distinctid=169d2216183388-07ae2582475b69-7a1437-144000-169d2216184432; CNZZDATA1260206164=1990517475-1554008597-https%253A%252F%252Fwww.baidu.com%252F%7C1554008597; _gid=GA1.2.1584687891.1556348763; __utmz=226521935.1556352396.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utma=226521935.1934859142.1553158342.1556352396.1556352395.1
if-modified-since: Sat, 27 Apr 2019 13:11:17 GMT
referer: https://www.google.com/
upgrade-insecure-requests: 1
user-agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Mobile Safari/537.36'''
# 使用字典生成式
header={i.split(":")[0]:i.split(":")[1] for i in header.split('\n')}
print(header)

# 结果

# s={'accept': ' text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
#    'accept-encoding': ' gzip, deflate, br',
#    'accept-language': ' zh-CN,zh;q=0.9',
#    'cache-control': ' max-age=0',
#    'cookie': ' _ga=GA1.2.1934859142.1553158342; __gads=ID=bb2c52e7f95e20ea',
#    'if-modified-since': ' Sat, 27 Apr 2019 13',
#    'referer': ' https',
#    'upgrade-insecure-requests': ' 1',
#    'user-agent': ' Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Mobile Safari/537.36'
#    }

```

设置编码

```python
import requests

url=""
request=requests.get(url)
request.encoding="utf-8"

```

获得cookie

现在大多数网站都需要人机验证，用爬虫登录有点难了，可以直接复制cookie

```python
import requests

url=""
data={'user':"","password":""}
session=requests.session()
# 使用session提交登录表单，成功后，cookie会保存在session中
session.post(url,data=data)
request=session.get(url)
text=request.text

```

超时处理，使用timeout设置网页请求最大时长，超时会抛出异常，用retry修饰后被修饰的对象会被重复执行stop_max_attempt_number次，最后还没成功才会抛出异常

```python
import requests
from retrying import retry

@retry(stop_max_attempt_number=5)
def test():
    try:
        request=requests(url,timeout=3)
    except:
        pass
```