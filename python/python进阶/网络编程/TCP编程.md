<!--961032830987546d0e6d54829fc886f6-->

目录(Catalo)

* [TCP编程](#TCP编程)
  * [常用方法](#常用方法)

<!--a46263f7a69f33f39fc26f907cdb773a-->
# TCP编程

TCP用于可靠数据传输，面向有连接

## 常用方法

1. connect(address)：连接远程计算机
2. send(bytes[,flags]):发送数据
3. recv(bufsize[,flags]):接收数据
4. bind(address)：绑定地址
5. listen(backlog):开始监听，等待客户端连接
6. accept():响应客户端请求，接受一个连接

```python
# 客户端
import socket
import sys

# 服务器地址与端口号
HOST='127.0.0.1'
PORT=57890
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    # 尝试连接远程服务器
    s.connect((HOST,PORT))
except Exception as e:
    print("服务端未开启")
    sys.exit()
while True:
    c=input("what you want to say:")
    # 向服务端发送请求消息
    s.sendall(c.encode())
    # 接受服务端反馈消息
    data=s.recv(1024)
    data=data.decode()
    print(data)
    if c.lower()=='bye':
        break
s.close()

```

```python
# 服务端

import socket

words={'how are you':'gun'}

# 服务端IP地址，为空时表示可以使用本机任何可用IP
HOST=''
# 服务器端口号，占用该端口与客户端通信
PORT=57890
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# 绑定地址和端口号
s.bind((HOST,PORT))
# 开始监听
s.listen(1)
print("正在监听端口 %d" % PORT)
# 监听发现有客户端请求建立连接，响应客户端请求，返回一个元组，包含一个socket对象和一个客户端信息，也是一个元组(hostaddr, port)
conn,addr=s.accept()
print(" 与 %s 建立了连接"% repr(addr[0]))
while True:
    # 接受客户端请求消息
    data=conn.recv(1024)
    data=data.decode()
    if not data:
        break
    print('Received message:',data)
    # 向客户端发送对应相应消息
    conn.sendall(words.get(data,'Nothing').encode())
# 关闭与客户端的连接
conn.close()
# 关闭服务器连接
s.close()
```

运行效果：

服务端

```shell
E:\PYthon\pythonday\python-note\again_study_python\测试代码\TCP>python server.py
正在监听端口 57890
 与 ('127.0.0.1', 60527) 建立了连接
Received message: how are you
Received message: hello
Received message: how are you
Received message: Bye
```

客户端

```shell
what you want to say:how are you
gun
what you want to say:hello
Nothing
what you want to say:how are you
gun
what you want to say:Bye
Nothing
```