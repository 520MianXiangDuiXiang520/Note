import socket
import threading


def Send(udp_socket, receive_addr):
    while True:
        info = str(input('请输入：')).encode()
        udp_socket.sendto(info, receive_addr)

def Receive(udp_socket):
    """
    接受端函数
    :return:
    """
    while True:
        data, addr = udp_socket.recvfrom(1024)
        print(f'接收到来自 {addr[0]}({addr[1]}) 的消息： {data.decode()}')



def main():
    # 建立套接字
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('', 5000))
    # 接收端套接字
    receive_addr = ('192.168.1.6', 1231)
    t1 = threading.Thread(target=Send, args=(udp_socket, receive_addr))
    t2 = threading.Thread(target=Receive,args=(udp_socket, ))
    t1.start()
    t2.start()

if __name__ == '__main__':
    main()
