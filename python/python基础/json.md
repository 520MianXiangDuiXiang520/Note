<!--961032830987546d0e6d54829fc886f6-->

目录(Catalo)

* [python-JSON](#python-JSON)

<!--a46263f7a69f33f39fc26f907cdb773a-->
# python JSON

json（JavaScript对象表示法）最初由JavaScript引入，JSON有数据，数组，对象三个概念

* 数据：键值配对形式，多个数据由“,”隔开，数据可以包括数字，字符，布尔类型，数组，对象，NULL
* 对象：用`{}`保存，对象可以包含多个数据
* 数组：用`[]`保存，数组可以保存多个对象

```json
{
    "ststic":[
        {"name":"home","url":"127.0.0.1:8000/home"},
        {"name":"about","url":"127.0.01:8000/about"},
    ]
}
```

----

在python中的json模块提供了七种方法实现python对象与json的编码转换：dumps、dump、loads、load,后三个不用管

```python
__all__ = [
    'dump', 'dumps', 'load', 'loads',
    'JSONDecoder', 'JSONDecodeError', 'JSONEncoder',
]
```

* dumps:将 Python 对象编码成 JSON 数据
* dump:将 JSON 数据通过特殊的形式转换为只有 Python 认识的字符串并写入文件
* loads:将已编码的 JSON 数据解码为 Python 对象
* load:将一个包含 JSON 格式数据的可读文件解码为一个 Python 对象并写入文件
* JSONDecoder:反序列化，json->python
* JSONDecodeError：数据转换异常
* JSONEncoder：序列化,python->json

```python
import json
list=[1,2,3,4,5,{"name":"home"}]
file_name='E:/桌面文件/test.json'
s=json.dumps(list)
print(type(s))
try:
    with open(file_name) as fileobject:
        r_js = json.load(fileobject)
        print(type(r_js))
        print(r_js)
except:
    with open(file_name, 'w') as fileobject:
        json.dump(list, fileobject)
```