# 代理服务器端口映射

原理是在两个端口之间转发数据

## 服务端代码

```python
import socket
import threading

def replyMessage(conn):
    while True:
        # 接受代理发过来的消息原样返回
        data=conn.recv(1024)
        conn.send(data)
        print('接收到数据 %s'% data.decode())
        if data.decode().lower()=='bye':
            print('断开连接')
            break
    conn.close()

def main():
    # TCP
    sockScr=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sockScr.bind(('',12345))
    sockScr.listen(20)
    while True:
        conn,addr=sockScr.accept()
        print("与 %s 建立连接" % addr[0])
        t=threading.Thread(target=replyMessage,args=(conn,))
        t.start()
        t.join()

if __name__ == '__main__':
    main()
```