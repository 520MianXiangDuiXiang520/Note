<!--961032830987546d0e6d54829fc886f6-->

目录(Catalo)

* [UDP编程](#UDP%E7%BC%96%E7%A8%8B)
  * [UDP常用的scoket模块](#UDP%E5%B8%B8%E7%94%A8%E7%9A%84scoket%E6%A8%A1%E5%9D%97)

<!--a46263f7a69f33f39fc26f907cdb773a-->
# UDP编程

UDP特定：面向无连接，速度快，质量不如TCP

## UDP常用的scoket模块

1. socket([family[,type[,proto]]])
   * family:socket,AF_INET表示IPv4，AF_INET6表示IPv6
   * SCOK_STREAM:TCP，SOCK_DGRAM:UDP

2. sendto(string,address):把string发送给address，address是一个元组(IP地址，端口号)
3. recvfrom(bufsize[,flags]) :接收数据

```python
# 接收端

import socket

# IPv4,UDP
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

# 绑定端口和端口号
s.bind(('',5000))

while True:
    data,addr=s.recvfrom(1024)
    print('接收到消息{0},发送端：{1}发送端口：{2}'.format(data.decode(),addr[0],addr[1]))
    if data.decode().lower()=='bye':
        print("接收到中断消息，已停止运行程序")
        break
```

```python
# 发送端
import socket
import sys

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# argv是获取命令行参数的，使用命令行运行脚本时，后面的参数会被作为列表的值传入列表，比如argv[0]就是脚本名
s.sendto(sys.argv[1].encode(),('192.168.47.1',5000))
s.close()
```

接收端效果

```doc
E:\PYthon\pythonday\python-note\again_study_python\测试代码>python recv.py
接收到消息helloworld,发送端：192.168.47.1发送端口：53126
接收到消息bye,发送端：192.168.47.1发送端口：51881
接收到中断消息，已停止运行程序
```

发送端效果

```doc
E:\PYthon\pythonday\python-note\again_study_python\测试代码>python send.py helloworld

E:\PYthon\pythonday\python-note\again_study_python\测试代码>python send.py bye
```