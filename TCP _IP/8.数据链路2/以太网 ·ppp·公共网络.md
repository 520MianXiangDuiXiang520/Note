嗨，我想听一个 TCP 的笑话。
你好，你想听 TCP 的笑话么？
嗯，我想听一个 TCP 的笑话。
好的，我会给你讲一个TCP 的笑话。
好的，我会听一个TCP 的笑话。
你准备好听一个TCP 的笑话么？
嗯，我准备好听一个TCP 的笑话
Ok，那我要发 TCP 笑话了。大概有 10 秒，20 个字。
嗯，我准备收你那个 10 秒时长，20 个字的笑话了。
抱歉，你的连接超时了... 你好，你想听 TCP 的笑话么？
<!--more-->
# 1.以太网
以太网（英语：Ethernet）是一种计算机局域网技术。IEEE组织的IEEE 802.3标准制定了以太网的技术标准，它规定了包括物理层的连线、电子信号和介质访问层协议的内容。以太网是当前应用最普遍的局域网技术，取代了其他局域网标准如令牌环、FDDI和ARCNET
## 1.1以太网连接形式
* 最初：使用一根同轴电缆的共享介质型连接方式
* 后来：使用终端与交换机之间独占电缆的方式

## 1.2 以太网的分类
以太网类型由电缆类型与通信速度有关，如 10Base－T 10Broad－36 10GBASE—T 等  
*  Base 代表 “基带” Broad 表示“带宽”  
* Base和Broad之前的数字表示通信速度，单位是Mbps，如10G表示10GMbps  
* Base和Broad之后的数字或字母表示所用电缆类型

## 1.3 以太网帧
在以太网链路上的数据包称为**以太网帧**  
### 1.3.1 以太网帧的结构

|前导码|帧开始符（SFD）|帧本体|
|-----|--------|------|
|占7个字节|占1个字节||

#### 前导码与帧开始符
>来源：维基百科
>
>一个帧以7个字节的前导码和1个字节的帧开始符作为帧的开始。快速以太网之前，在线路上帧的这部分的位模式是10101010 10101010 10101010 10101010 10101010 10101010 10101010 10101011。由于在传输一个字节时最低位最先传输(LSB)，因此其相应的16进制表示为0x55 0x55 0x55 0x55 0x55 0x55 0x55 0xD5。
10/100M 网卡(MII PHY)一次传输4位(一个半字)。因此前导符会成为7组0x5+0x5,而帧开始符成为0x5+0xD。1000M网卡(GMII)一次传输8位，而10Gbit/s(XGMII) PHY芯片一次传输32位。 注意当以octet描述时，先传输7个01010101然后传输11010101。由于8位数据的低4位先发送，所以先发送帧开始符的0101，之后发送1101。

#### 帧本体
一般的以太网帧本体结构  

|目标MAC地址|源MAC地址|类型|数据|FCS|
|------------|-------|-----|---|---|
|6字节|6字节|2字节|46·1500字节|4字节|
|存放目标工作站物理地址|存放构造以太网帧的发送端物理地址|明确以太网上一层网络协议类型| |用来检查帧是否损坏|

IEEE802.3以太网帧体结构

|目标MAC地址|源MAC地址|帧长度|LLC|SNAP|数据|FCS|
|-----------|--------|-----|----|----|-----|---|
|6字节|6字节|2字节|3字节|5字节|38~1492字节|4字节|

* LLC
>来源：[维基百科](https://zh.wikipedia.org/wiki/%E4%BB%A5%E5%A4%AA%E7%BD%91%E5%B8%A7%E6%A0%BC%E5%BC%8F)
>一些协议，尤其是为OSI模型设计的，会直接在802.2 LLC层上操作。802.2 LLC层同时提供数据报和面向连接的网络服务。
>
>802.2以太网变种没有在常规网络中普遍使用。只有一些大公司的没有与IP网络融合的Netware设备。以前，很多公司Netware网络支持802.2以太网，以便支持从以太网到IEEE 802.5令牌环网或FDDI网络的透明桥接。当今最流行的数据包是以太网版本二，由基于IP协议的网络使用，将其以太类型设置为0x0800用于封装IPv4或者0x86DD来支持IPv6。
>
>还有一个英特网标准来使用LLC/SNAP报头将IPv4封装在IEEE 802.2帧中。[3] 这几乎从未在以太网中实现过。(但在FDDI以及令牌环网，IEEE 802.11和其他IEEE 802网络中使用)。如果不使用SNAP,IP传输无法封装在IEEE 802.2 LLC帧中。这是因为LLC协议中虽然有一种IP协议类型，却没有ARP。IPv6同样可使用LLC/SNAP在IEEE 802.2以太网上传播，但，如同IPv4，它也绝少被这样使用。(尽管LLC/SNAP的IPv6数据包在IEEE 802网络中被使用)。
* SNAP : 明确以太网上一层网络协议类型

# 2.无线通信
无线通讯（英语：Wireless communication）是指多个节点间不经由导体或缆线传播进行的远距离传输通讯， 利用收音机、无线电等都可以进行无线通讯。

大部分无线通讯技术会用到无线电，包括距离只到数米的Wi-fi，也包括和航海家1号通讯、距离超过数百万公里的深空网络。但有些无线通讯的技术不使用无线电，而是使用其他的电磁波无线技术，例如光、磁场、电场等。
## 2.1 无线通信种类
分类标准：传输距离

|分类|通信距离|相关技术|
|----|-------|--------|
|短距离无线|数米|RF-ID|
|无线PAN|10米左右|蓝牙|
|无线LAN（局域网）|100米左右|Wi-Fi|
|无线MAN|数千米~100km|WiMAX|
|无线RAN|200km~700km|——|
|无线WAN（广域网）|——|3G，LTE，4G等|

* Wi-Fi ： 高质量无线LAN，与Hi-Fi类似（高保真音质）
# 3.公共网络

## 3.1 模拟电话线路
详情点击[百度百科](https://baike.baidu.com/item/%E6%A8%A1%E6%8B%9F%E7%94%B5%E8%AF%9D)
## 3.2 FTTH
Fiber To The Home,光纤到户，是一种光纤通信的传输方法。是直接把光纤接到用户的家中
[详情](https://baike.baidu.com/item/FTTH/922996?fr=aladdin)查看百度百科

## 3.3 VPN
虚拟专用网络，实质是利用加密技术在公用网络链路上开辟一条专用通道，
[详情](https://baike.baidu.com/item/%E8%99%9A%E6%8B%9F%E4%B8%93%E7%94%A8%E7%BD%91%E7%BB%9C?fromtitle=VPN&fromid=382304)百度百科
# 4.ppp
## 4.1 PPP的定义
点对点协议（英语：Point-to-Point Protocol，PPP）工作在数据链路层（以OSI参考模型的观点）。它通常用在两节点间创建直接的连接，并可以提供连接认证、传输加密（使用ECP，RFC 1968）以及压缩。

PPP仅仅作用于OSI参考模型的第二层——数据链路层，仅有PPP是无法完成通信的，需要与物理层结合。

## 4.2 LCP与NCP
在开始进行数据传输之前，要建立PPP级的连接，之后可以进行身份验证，压缩，加密

PPP的主要功能中包括两个协议，LCP（不依赖上层）和NCP（依赖上层，如果上层是IP，也叫IPCP）

* LCP：负责建立和断开连接，设置最大连接单元（MRU），设置验证协议（PAP和CHAP）以及设置是否进行通信质量监控等
  * PAP：通过两次握手进行用户名和密码的验证，密码以明文传输，安全性不高
  * CHAP：使用一次性密码OTP，可以有效防止窃听，还可以定期交换密码，用来检测对端是否中途被替换
* IPCP：负责IP地址设置以及是否进行TCP/IP首部压缩

## 4.3 PPP帧

|名称|标志|地址|控制|类型|数据|FCS|标志|
|----|----|---|---|---|----|----|----|
|字节数|1|1|1|2|0~1500|4|1|
|描述|区分帧|广播地址|控制字|数据报文中所使用的协议|数据报文|错误校验|区分帧|
