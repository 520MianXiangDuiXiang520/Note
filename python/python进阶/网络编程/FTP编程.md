# FTP编程

我个人觉得其实就是TCP加OS处理命令行参数和二进制文件操作的合集...

客户端

```python
import socket
import sys
import struct
import getpass

def main(serverIP):
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((serverIP,10600))
    userId=input('输入用户名：')
    userPwd=getpass.getpass('请输入密码：')
    message=userId+',' + userPwd
    sock.send(message.encode())
    login=sock.recv(100)
    if login==b'error':
        print('用户名或密码错误！')
        return
    intSize=struct.calcsize('I')
    while True:
        command=input('##>').lower().strip()
        if not command:
            continue
        command=''.join(command.split())
        sock.send(command.encode())
        if command in('q','quit'):
            break
        elif command in('list','dir','ls'):
            loc_size=struct.unpack('I',sock.recv(intSize))[0]
            files=eval(sock.recv(loc_size).decode())
            for item in files:
                print(item)
        elif command in('cd','cwd'):
            print(sock.recv(1024).decode())
        elif command.startswith('cd'):
            print('打开目录')
            print(sock.recv(100).decode())
        elif ''.join(command.split())=='cd..':
            print('返回上一级')
            print(sock.recv(100).decode())
        elif command.startswith('get'):
            isFileExist=sock.recv(20)
            if isFileExist != b'ok':
                print('error')
            else:
                print('downloading.',end='')
                # print(command.split())
                fp=open(command.split('get')[1],'wb')
                while True:
                    print('.',end='')
                    data=sock.recv(4096)
                    if data ==b'overxxxxx':
                        break
                    fp.write(data)
                    sock.send(b'ok')
                fp.close()
                print('ok')
        else:
            print("无效")
    sock.close()

if __name__ == '__main__':
    serverIp=sys.argv[1]
    main(serverIp)

```

服务端

```python
import socket
import threading
import os
import struct

users={
    'zhangsan':{'pwd':'zs12345','home':r'E:\PYthon\pythonday\python-note\again_study_python'},
    'lisi':{'pwd':'ls12345','home':r'E:\PYthon\pythonday\python-note\again_study_python'}
}
def server(conn,addr,home):
    print('新客户端：'+str(addr))
    os.chdir(home)
    while True:
        data=conn.recv(100).decode().lower()
        print(data)
        if data in('quit','q'):
            break
        elif data in ('list','dir','ls'):
            files=str(os.listdir(os.getcwd()))
            files=files.encode()
            conn.send(struct.pack('I',len(files)))
            conn.send(files)
        elif ''.join(data.split())=='cd..':
            cwd=os.getcwd()
            newCwd=cwd[:cwd.rindex('\\')]
            if newCwd[-1]==':':
                newCwd+='\\'
            if newCwd.lower().startswith(home):
                os.chdir(newCwd)
                conn.send(b'ok')
            else:
                conn.send(b'error')
        elif data in ('cwd','cd'):
            conn.send(str(os.getcwd()).encode())
        elif data.startswith('cd'):
            data=data.split('cd')
            if len(data)==2 and os.path.isdir(data[1]):
                os.chdir(data[1])
            else:
                conn.send(b'error')
        elif data.startswith('get'):
            # data=data.split(maxsplit=1)
            data = data.split('get')
            print(data)
            if len(data)==2 and os.path.isfile(data[1]):
                conn.send(b'ok')
                fp=open(data[1],'rb')
                while True:
                    content=fp.read(4096)
                    if not content:
                        conn.send(b'overxxxxx')
                        break
                    conn.send(content)
                    if conn.recv(10)==b'ok':
                        continue
                fp.close()
            else:
                conn.send(b'no')
        else:
            pass

    conn.close()
    print(str(addr)+'关闭连接')


if __name__ == '__main__':
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.bind(('',10600))
    sock.listen(5)
    while True:
        conn,addr=sock.accept()
        print('与 %s 建立连接' %addr[0])
        userId,userPwd=conn.recv(1024).decode().split(',')
        if userId in users and users[userId]['pwd']==userPwd:
            conn.send(b'ok')
            home=users[userId]['home']
            t=threading.Thread(target=server,args=(conn,addr,home))
            t.daemon=True
            t.start()
        else:
            conn.send(b'error')
```