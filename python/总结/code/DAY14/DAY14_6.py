import socket
import sys

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# argv是获取命令行参数的，使用命令行运行脚本时，后面的参数会被作为列表的值传入列表，比如argv[0]就是脚本名
info = str(input('请输入：')).encode()
s.sendto(info, ('192.168.1.8', 5000))
s.close()