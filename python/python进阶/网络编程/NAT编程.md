<!--961032830987546d0e6d54829fc886f6-->

目录(Catalo)

* [代理服务器端口映射](#代理服务器端口映射)
  * [服务端代码](#服务端代码)

<!--a46263f7a69f33f39fc26f907cdb773a-->
# 代理服务器端口映射

原理是在两个端口之间转发数据

## 服务端代码

```python
import socket
import threading


def replyMessage(conn):
    while True:
        # 接受代理发过来的消息原样返回
        data = conn.recv(1024)
        conn.send(data)
        print('接收到数据 %s' % data.decode())
        if data.decode().lower() == 'bye':
            print('断开连接')
            break
    conn.close()


def accept_middle(sockScr):
    while True:
        conn, addr = sockScr.accept()
        print('服务器已启动')
        print("与 %s 建立连接" % addr[0])
        replyMessage(conn)


def main():
    # TCP
    sockScr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockScr.bind(('', 1234))
    sockScr.listen(20)
    t1 = threading.Thread(target=accept_middle, args=(sockScr,))
    t2 = threading.Thread(target=accept_middle, args=(sockScr,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()


if __name__ == '__main__':
    main()
```

代理端代码

```python
import socket
import threading

def middle(conn,addr):
    # 发起与服务器的连接
    sockDst=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sockDst.connect(('192.168.47.130',1234))
    while True:
        data=conn.recv(1024).decode()
        print('收到客户端数据:'+data)
        sockDst.send(data.encode())
        print('转发给服务器')
        data_fromServer=sockDst.recv(1024).decode()
        print('接收到服务器的反馈:'+data_fromServer)
        conn.send(b'Server reply:'+data_fromServer.encode())
        print('转发给客户端')
    conn.close()
    sockDst.close()

def accept_client(sockScr):
    while True:
        try:
            # 响应客户端连接请求
            conn,addr=sockScr.accept()
            middle(conn,addr)
            print('新客户:'+str(addr))
        except:
            pass

def main():
    sockScr=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sockScr.bind(('',12345))
    sockScr.listen(20)
    print('代理已启动')
    t1=threading.Thread(target=accept_client,args=(sockScr,))
    t2 = threading.Thread(target=accept_client, args=(sockScr,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

if __name__ == '__main__':
    try:
        main()
    except:
        pass
```

客户端代码

```python
# 客户端
import socket
import sys

# 代理服务器地址与端口号
HOST='127.0.0.1'
PORT=12345
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    # 尝试连接代理服务器
    s.connect((HOST,PORT))
except Exception as e:
    print("代理服务端未开启")
    sys.exit()
while True:
    c=input("what you want to say:")
    # 向代理服务端发送请求消息
    s.sendall(c.encode())
    # 接受代理服务端反馈消息
    data=s.recv(1024)
    data=data.decode()
    print(data)
    if c.lower()=='bye':
        break
s.close()


```