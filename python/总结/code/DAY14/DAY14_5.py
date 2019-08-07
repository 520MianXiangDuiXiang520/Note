import socket
import threading

lock = threading.Lock()

# 建立套接字
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 接收端套接字
# 192.168.1.7
# 192.168.1.6
receive_socket = ('192.168.1.7', 12315)

# 发送端套接字
send_socket = ('', 12315)

def Send():
    while True:
        lock.acquire()
        message = str(input("请输入发送内容："))
        s.sendto(message.encode('utf-8'), receive_socket)
        lock.release()

def Receive():
    """
    接受端函数
    :return:
    """
    while True:
        lock.acquire()
        data, addr = s.recvfrom(1024)
        print(f'接收到来自 {addr[0]}({addr[1]}) 的消息： {data.decode()}')
        lock.release()


def main():
    t1 = threading.Thread(target=Send)
    t2 = threading.Thread(target=Receive)
    t1.start()
    t2.start()

if __name__ == '__main__':
    main()