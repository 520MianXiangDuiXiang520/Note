# 关机重启
shutdown 选项 时间
* 选项：
  * 不填写默认关机，服务器一般不要关机
  * -r ：重启
  * -c ：取消命令
* 时间：
  * 立刻执行：now
  * 不填写：一分钟后执行
  * 20：25  ：晚上八点二十五关机
  * +10 ：十分钟后关机

# 查看或配置网卡信息
* 网卡：负责网络通信的硬件设备
* IP地址：设置在网卡上的地址信息


* ifconfig: 查看/配置网卡配置信息
```
junbao111@ubuntu:~$ ifconfig|grep inet
        inet 192.168.119.130  netmask 255.255.255.0  broadcast 192.168.119.255
        inet6 fe80::fcc3:a36d:1b06:30c4  prefixlen 64  scopeid 0x20<link>
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
junbao111@ubuntu:~$ 

```
* inet是ipv4的IP地址，inet6是Ipv6的IP地址
* 127.0.0.1：本地回环地址

* ping ip地址 ：检测到目标ip地址连接是否正常，ctrl+C退出

```
junbao111@ubuntu:~$ ping 127.0.0.1
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.036 ms
64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.025 ms
64 bytes from 127.0.0.1: icmp_seq=3 ttl=64 time=0.025 ms
64 bytes from 127.0.0.1: icmp_seq=4 ttl=64 time=0.055 ms
64 bytes from 127.0.0.1: icmp_seq=5 ttl=64 time=0.025 ms
·
·
·
^C
--- 127.0.0.1 ping statistics ---
102 packets transmitted, 102 received, 0% packet loss, time 103408ms
rtt min/avg/max/mdev = 0.020/0.030/0.110/0.015 ms

```

原理：
乌班图给目标主机发送一个56字节的包，目标主机接收到数据包后给发送端一个64字节的回值，乌班图检测来回的时间，时间越小，网速越大。

# 远程登录和复制文件
## SSH
可靠，安全,对传输的数据进行压缩，速率高...

windows使用ssh需要安装，乌班图默认安装好了

### 域名
IP的别名，方便记忆
### 端口号
通过端口号找到计算机上允许的应用程序
* 常见的端口号

|端口号|服务|
|------|---|
|22|SSH服务器|
|80|Web服务器|
|443|HTTPs|
|21|FTP服务器|

### SSH命令
格式：
`ssh [-p port] user@remote`
* user:用户名，不指定为当前默认用户
* post： 端口号，默认为22
* remote：地址
* exit：退出当前用户登录