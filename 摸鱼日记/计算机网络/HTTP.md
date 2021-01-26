#  HTTP

为什么会出现 HTTP 协议，从 HTTP1.0 到 HTTP3 经历了什么？HTTPS 又是怎么回事？

<!-- more -->

HTTP 是一种用于获取类似于 HTML 这样的资源的 **应用层通信协议**， 他是万维网的基础，是一种 CS 架构的协议，通常来说，HTTP 协议一般由浏览器等 “客户端” 发起，发起的这个请求被称为 Request, 服务端接受到客户端的请求后，会返回给客户端所请求的资源，这一过程被称为 Response，在大部分情况下，客户端和服务器之间还可能存在许多 [proxies](https://developer.mozilla.org/en-US/docs/Glossary/Proxy)，他们的作用可能各不相同，有些可能作为网关存在，有些可能作为缓存存在。

![](https://cdn.jsdelivr.net/gh/520MianXiangDuiXiang520/cdn@master/img/1609752900346-1609752900153.png)

HTTP 协议有三个基本的特性：

1. 简单：HTTP 的协议和报文是简单，易于理解和阅读的（HTTP/2 已经改用二进制传输数据，但 HTTP 整体还是简单的）
2. 可拓展的：请求和响应都包括 “Header” 和 “Body” 两部分，我们可以通过添加头部字段轻松的拓展 HTTP 的功能
3. 无状态的：服务端不保存客户端状态，也就是说每一次请求的服务端来说都是唯一无差别的，我们只能通过 Cookie 等技术创建有状态的会话。

## HTTP 的历史

HTTP 的历史可以追溯到万维网刚被发明的时候，1989年， Tim Berners-Lee 博士写了一份关于建立一个**通过网络传输超文本系统**的报告。该系统起初被命名为 *Mesh*，在随后的1990年项目实施期间被更名为万维网（*World Wide Web）。他以现有的 TCP IP 协议为基础建造， 由四个部分组成：

* 用来表示超文本文档的文本格式，即超文本标记语言（HTML）
* 一个用来传输超文本的简单应用层协议，即超文本传输协议（HTTP）
* 一个用来显示或编辑超文本文档的客户端，即网络浏览器，而第一个浏览器则被称为 *WorldWideWeb*
* 一个用于提供可访问文档的服务，[httpd](https://zh.wikipedia.org/wiki/Httpd) 的前身.

这四部分在 1990 年底完成，这时候的 HTTP 协议还很简单，后来为了于其他版本的协议区分，最初的 HTTP 协议被记为 HTTP/0.9，

后来，随着计算机技术的发展，HTTP 协议也随着 HTTP/1.0, HTTP/1.1, HTTP/2 等关键版本更迭变得更加高效实用。

### HTTP/0.9 on-line

最初的 0.9 版本也被称为单行协议（on-line）, 基于 TCP 协议，该版本下只有一个可用的请求方法：GET， 请求格式也相当简单：

```http
GET /index.html
```

它表示客户端请求 `index.html` 的内容，0.9 版本的 HTTP 响应也同样简单，他只允许响应 HTML 格式的字符串，如：

```html
<html>
    <h1> ..... </h1>
</html>
```

这一阶段的响应甚至没有响应头，也没有响应码或错误代码，一旦出现问题，服务端会响应一段特殊的 HTML 字符串以便客户端查看。 服务端在发送完数据后，就会立刻关闭 TCP 连接。

### HTTP/1.0

0.9 版本的 HTTP 协议太过于简单甚至是简陋，而随着浏览器和服务器的应用被扩展到越来越多的领域，0.9 版本的协议已经不能适应，直到 1996年11月，[RFC 1945](https://tools.ietf.org/html/rfc1945) 定义了 HTTP/1.0, 但他并不是官方标准，该版本的 HTTP 协议较 0.9 版本有了一下改变：

1. 版本号被添加到了请求头上，像下面这样：

   ```http
   GET /mypage.html HTTP/1.0
   ```

2. 引入了 HTTP头的概念，无论是请求还是响应，允许传输元数据，这使得协议更加灵活和具有拓展性。

3. 请求方法拓展到了 GET，HEAD，POST

4. 在新 HTTP 头（`Content-Type`）的帮助下，可以传输不止 HTML 的任意格式的数据。

5. 响应时带上了状态码，使得浏览器能够知道响应的状态并作出响应的处理。

6. ...

### HTTP/1.1

同 0.9 版本一样，1.0 版本下，TCP 连接是不能复用的，数据发送完后服务端会立刻关闭连接，但由于建立 TCP 连接的代价较大，所以 1.0 版本的 HTTP 协议并不是足够高效，加上 HTTP/1.0 多种不同的实现方式在实际运用中显得有些混乱，自1995年就开始了 HTTP 的第一个标准化版本的修订工作，到1997年初，HTTP1.1 标准发布。

1.1 版本的改进包括：

1. 支持长连接：在 HTTP1.1 中默认开启 Connection： keep-alive，允许在一个 TCP 连接上传输多个 HTTP 请求和响应，减少了建立和关闭连接造成的性能消耗。

2. 支持 `pipline`: HTTP/1.1 还支持流水线（pipline）工作，流水线是指在同一条长连接上发出连续的请求，而不用等待应答返回。这样可以避免连接延迟。

3. 支持响应分块：对于比较大的响应，HTTP/1.2 通过 `Transfer-Encoding` 首部支持将其分割成多个任意大小的分块，每个数据块在发送时都会附上块的长 度，最后用一个零长度的块作为消息结束的标志。

4. 新的缓存控制机制：HTTP/1.1定义的 [`Cache-Control`](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Headers/Cache-Control) 头用来区分对缓存机制的支持情况，同时，还提供 [`If-None-Match`](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Headers/If-None-Match), [`ETag`](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Headers/ETag) ,  [`Last-Modified`](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Headers/Last-Modified), [`If-Modified-Since`](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Headers/If-Modified-Since) 等实现缓存的验证等工作。

5. 允许不同域名配置到同一IP的服务器上：在 HTTP/1.0 时，认为每台服务器绑定一个唯一的 IP，但随着技术的进步，一台服务器的多个虚拟主机会共享一个IP，为了区分同一服务器上的不同服务，HTTP/1.1 在请求头中加入了 `HOST` 字段，它指明了请求将要发送到的服务器主机名和端口号，这是一个必须字段，请求缺少该字段服务端将会返回 400.

6. 引入内容协商机制，包括语言，编码，类型等，并允许客户端和服务器之间约定以最合适的内容进行交换。

7. 使用了 100 状态码：HTTP/1.0 中，定义：

   ```txt
   o 1xx: Informational - Not used, but reserved for future use
   ```

   在 2.0 版本时，使用了这个保留的状态码，用来表示临时响应。

### HTTPS

HTTP/1.1 之后，对 HTTP 协议的拓展变得更加简单，但 HTTP 依然存在一个天然的缺陷就是明文传输数据，直到 1994 年底，网景公司在 TCP/IP 协议栈的基础上添加了 SSL 层用来加密传输，后来，在标准化的过程中， SSL 成了  TLS （Transport Layer Security 传输层安全协议），基于 HTTPS 通信的客户端和服务器在建立完 TCP 连接之后会协商通信密钥，在之后的通信过程中， 客户端和服务器会使用该密钥对数据进行对称加密，以防数据被窃取或篡改。（密钥协商阶段会使用非对称加密）。

### HTTP/2

HTTP/1.1 虽然允许连接复用和以流水线方式运作，但在一个 TCP 连接里面，所有数据依然还是按序发送的，服务器只能处理完一个请求再去处理另一个请求，如果第一个请求非常慢，就会造成后面的请求长时间阻塞，这被称为 **队头阻塞（Head-of-line blocking）**，2009 年，谷歌公开了自行研发的 SPDY 协议，它基于 HTTPS，并采用多路复用解决了队头阻塞的问题，同时，它还使用了 Header 压缩等技术大大降低了延时并提高了带宽利用率，在之后的 2015 到 2019 年间，谷歌在自家浏览器上实践和证明了这个协议，SPDY 也成了 HTTP/2 的基石。

2015 年 5 月， HTTP/2 正式标准化，他与 1.x 版本 不同在于：

1. 1.x 版的 HTTP 协议传输的是文本信息，这对开发者很友好，但却浪费了计算机的性能，HTTP/2 改成了基于二进制而不再是基于文本的协议，
2. 这是一个复用协议。并行的请求能在同一个链接中处理，移除了HTTP/1.x中顺序和阻塞的约束。
3. 压缩了headers。因为headers在一系列请求中常常是相似的，其移除了重复和传输重复数据的成本。
4. 其允许服务器在客户端缓存中填充数据，通过一个叫服务器推送的机制来提前请求。

虽然 HTTP/2 2015 年就被标准化，在到目前为止，HTTP/1.1 任然被广泛使用，据 [MySSL](https://myssl.com/https_reports.html) 的最新统计，截至 2020 年 12 月，已有 65.84% 的站点支持了 HTTP/2.

### HTTP/3

HTTP/3 是即将到来的第三个主要版本的 HTTP 协议，在 HTTP/3 中，将弃用 TCP 协议，改为使用基于 UDP 的 [QUIC](https://zh.wikipedia.org/wiki/快速UDP网络连接) 协议实现。QUIC（快速UDP网络连接）是一种实验性的网络传输协议，由Google开发，该协议旨在使网页传输更快。

在2018年10月28日的邮件列表讨论中，[IETF(互联网工程任务组)](https://zh.wikipedia.org/wiki/IETF) HTTP和QUIC工作组主席 [Mark Nottingham](https://zh.wikipedia.org/w/index.php?title=Mark_Nottingham&action=edit&redlink=1) 提出了将 HTTP-over-QUIC 更名为 HTTP/3 的正式请求，以“明确地将其标识为HTTP语义的另一个绑定……使人们理解它与 QUIC 的不同”，并在最终确定并发布草案后，将 QUIC 工作组继承到 HTTP 工作组, 在随后的几天讨论中，Mark Nottingham 的提议得到了 IETF 成员的接受，他们在2018年11月给出了官方批准，认可 HTTP-over-QUIC 成为 HTTP/3。

2019年9月，HTTP/3支持已添加到 CloudFlare 和 Chrome 上。Firefox Nightly 也将在2019年秋季之后添加支持。

## HTTP/1.1 细节

### HTTP报文

HTTP 的报文都由消息头和消息体两部分组成，两者之间以 `CRLF(回车换行)` 分割。


#### 请求头格式

请求头第一行为**请求行**，其余为请求头字段：如下：

```http
POST /api/article/list HTTP/1.1
Host: junebao.top:8888
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0
Accept: application/json, text/plain, */*
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate, br
Content-Type: application/json;charset=utf-8
Content-Length: 32
Origin: https://junebao.top
Connection: keep-alive
Referer: https://junebao.top/
Cache-Control: max-age=0
```

请求行由三部分组成：

1. 请求方法
2. 请求资源的 url
3. 协议版本

他们以空格分隔，[RFC2068](https://tools.ietf.org/html/rfc2068#section-5.1.1) 定义了其中不同的请求方法，他们分别为  OPTIONS， GET， HEAD， POST， PUT， DELETE， TRACE,除此之外，后来还添加了一个 PATCH 方法。

| 方法    | 基本用法                                                     | 请求                                | 响应                                                    | 幂等性 | 缓存                     | 安全性 |
| ------- | ------------------------------------------------------------ | ----------------------------------- | ------------------------------------------------------- | ------ | ------------------------ | ------ |
| OPTIONS | 获取目的资源所支持的通信选项,<br />如检测服务器所支持的请求方法或CORS预检请求 | 不能携带请求体或数据                | 可以携带响应体，但一般有效数据被放在头部如 Allow 等字段 | 幂等   | 不可缓存                 | 安全   |
| GET     | 用于获取某个资源                                             | 参数一般携带在 URL 后面，没有请求体 | 有响应体                                                | 幂等   | 可缓存                   | 安全   |
| HEAD    | 用于请求资源的头部信息，如下载前获取大文件的大小             | 没有请求体                          | 没有响应体，响应头应该与使用 GET 请求时的一样           | 幂等   | 可缓存                   | 安全   |
| POST    | 将数据发送给服务器                                           | 数据放在请求体中                    | 有响应体                                                | 不幂等 | 可缓存（包含新鲜信息时） | 不安全 |
| PUT     | 使用请求中的负载创建或替换目标资源                           | 数据放在请求体中                    | 有响应体                                                | 幂等   | 不可缓存                 | 不安全 |
| DELETE  | 删除指定资源                                                 | 可以由请求体                        | 可以由响应体                                            | 幂等   | 不可缓存                 | 不安全 |
| TRACE   | 回显服务器收到的请求，主要用于测试或诊断。                   | 无请求体                            | 无响应体                                                | 幂等   | 不可缓存                 | 不安全 |
| PATCH   | 作为 PUT 的补充，用于修改已知资源的部分                      | 有请求体                            | 无响应体                                                | 非幂等 | 不可缓存                 | 不安全 |

##### 请求头字段

[RFC 2068](https://tools.ietf.org/html/rfc2068#section-5.3) 提供了 17 种请求头字段，但 HTTP 协议是易于拓展的，我们可以根据自己的需要添加自己的请求头，常见的请求头字段包括：

| 字段       | 作用                                                         | 示例                |
| ---------- | ------------------------------------------------------------ | ------------------- |
| HOST       | 指明了要发送到的服务器的主机号和端口号，这是一个必须字段，缺失服务器一般会返回 400,<br />端口号默认 80 和 443 | Host: www.baidu.com |
| ACCEPT     | 告知服务器客户端可以处理的内容类型，用[MIME类型](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Basics_of_HTTP/MIME_types)来表示。 | Accept: text/html   |
| User-Agent | 用户代理标识                                                 |                     |
| Cookies    | 用于维持会话                                                 |                     |
| ...        | ...                                                          | ...                 |

#### 响应头格式

```txt
 Response      = Status-Line
                 *( general-header
                 | response-header
                 | entity-header )
                 CRLF
                 [ message-body ]
```

类似于请求头，响应头包括状态行和响应头字段两部分组成。

状态行包括协议版本，状态码，状态描述三部分组成，类似：

```http
http/2 200 ok
```

目前 http 使用的状态码分为 5 类：

* 1xx: 信息响应类
* 2xx: 正常响应类
* 3xx: 重定向类
* 4xx: 客户端错误类
* 5xx: 服务端错误类

##### 常见状态码

| 状态码 | 描述                       | 作用                                                         |
| ------ | -------------------------- | ------------------------------------------------------------ |
| 100    | Continue                   | 迄今为止的所有内容都是可行的，客户端应该继续请求             |
| 200    | Ok                         | 请求成功                                                     |
| 201    | Created                    | 该请求已成功，并因此创建了一个新的资源。这通常是在POST请求，或是某些PUT请求之后返回的响应。 |
| 301    | Moved Permanently          | 永久重定向                                                   |
| 302    | Found                      | 临时重定向                                                   |
| 400    | Bad Request                | 请求参数错误或语义错误                                       |
| 401    | Unauthorized               | 请求未认证                                                   |
| 403    | Forbidden                  | 拒绝服务                                                     |
| 404    | Not Found                  | 资源不存在                                                   |
| 429    | Too Many Requests          | 超过请求速率限制（节流）                                     |
| 500    | Internal Server Error      | 服务端未知异常                                               |
| 501    | Not Implemented            | 此请求方法不被服务端支持                                     |
| 502    | Bad Gateway                | 网关错误                                                     |
| 503    | Service Unavailable        | 服务不可用                                                   |
| 504    | Gateway Timeout            | 网关超时                                                     |
| 505    | HTTP Version Not Supported | HTTP 版本不被支持                                            |

### 无状态的 HTTP

HTTP 是一个无状态的协议，为了维持会话，每客户端请求时，都应该携带一个 “凭证”，证明 who am i, 目前维持会话常用的技术有：cookie, session, token, 等

#### cookie

[RFC 6265](https://tools.ietf.org/html/rfc6265) 定义了 Cookie 的工作方式, Cookie 是服务器发送给客户端并存储在本地的一小段数据，在用户第一次登录时，服务器生成 Cookie 并在响应头里添加 `Set-Cookie` 字段，客户端收到响应后，将 `Set-Cookie` 字段的值（Cookie）存储在本地，以后每次请求时，客户端会自动通过 `Cookie` 字段携带 Cookie。

Cookie 以键值的形式储存，除了必须的 Name 和 Value，还可以为 Cookie 设置以下属性：

* Domain：指定了哪写主机可以接收该 Cookie，默认为 Origin， 不包含子域名。
* Path：规定了请求主机下的哪些路径时要携带该 Cookie。
* Expires/Max-Age: 规定该 Cookie 过期时间或最大生存时间，该时间只与客户端有关。
* HttpOnly: JavaScript [`Document.cookie`](https://developer.mozilla.org/zh-CN/docs/Web/API/Document/cookie) API 无法访问带有 HttpOnly 属性的cookie,用于预防 XSS 攻击；用于持久化会话的 Cookie 一般应该设置 HttpOnly 。
* Secure：标记为 Secure 的 Cookie 只能使用 HTTPS 加密传输给服务器，因此可以防止中间人攻击，但 Cookie 天生具有不安全性，任何敏感数据都不应该使用 Cookie 传输，哪怕标记了 secure.
* Priority：
* SameSite：要求该 Cookie 在跨站请求时不会被发送，用来阻止 CSRF 攻击，它有三种可选的值：
  * None：在同站请求和跨站请求时都会携带上 Cookie
  * Strict：只会在访问同站请求时带上 Cookie
  * Lex：与 Strict 类似，但用户从外部站点导航至URL时（例如通过链接）除外，新版浏览器一般以 Lex 为默认选项。

Cookie 被完全保存在客户端，对客户端用户来说是透明的，用户可以自己创建和修改 Cookie，所以将敏感信息（如用于持久化会话的用户身份信息等）存放在 Cookie 中是十分危险的，如果不得已需要使用 Cookie 来存储和传递这类信息，应该考虑使用 JWT 等类似机制。

由于 Cookie 的不安全性，绝大部分 Web 站点已经开始停止使用 Cookie 持久化会话，但 Cookie 在一些对安全性要求不高的场景下依然被广泛使用，如：

* 个性化设置
* 浏览器用户行为跟踪。

> 了解更多：
>
> [超级 Cookie 和僵尸 Cookie](https://www.sohu.com/a/259750790_185201)
>
> [决战僵尸 Cookie](https://yq.aliyun.com/articles/299884/)

#### SESSION

Cookie 不安全的根源在于它将会话信息保存在了客户端，为此，就有了使用 Session 持久化会话的方案，用户在第一次登录时，服务器会将用户会话状态信息保存在服务器内存中，同时会为这段信息生成一串唯一索引，将这个索引作为 Cookie （Name 一般为 SESSION_IDSESSION_ID）返回给客户端，客户端下一次请求时，会自动携带这个 SESSION_ID, 服务器只需要根据 SESSION_ID 的值找到对应的状态信息就可以知道这次请求是谁发起的。

SESSION 很大程度上还是依赖于 Cookie，但这时 Cookie 中保存的已经是一段对客户端来说无意义的字符串了，因此使用 Session 能安全的实现会话持久化，但 Session 信息被保存在服务器内存中，可能造成服务器压力过大，并且在分布式和前后端分离的环境下，Session 并不容易拓展。

#### TOKEN

Cookie 和 Session 都是开箱即用的 API，因此，他们不可避免地缺少灵活性，在一般开发中，往往采用更灵活地 Token，Token 与 Session 原理一致，都是将会话信息保存到服务器，然后向客户端返回一个该信息的索引（token），但 Token 完全由开发者实现，可以根据需要将会话信息存储在内存，数据库，文件等地方，而对于该信息的索引，也可以根据具体需要选择使用请求头，请求体或者 Cookie 传递，也不必拘束于只 Cookie 传递。

##### JWT

全称 json web token, 是一种客户端存储会话状态的技术，它使用数字签名技术防止了负荷信息被篡改，jwt 包含三部分信息：

- Header：包含 token 类型和算法名称
- Payload：存储的负载信息（敏感信息不应该明文存放在此）
- Signature：服务端使用私钥对 Header 和 Payload 的签名，防止信息被篡改。

这三部分原本都是 json 字符串，最终他们会经过 Base64 编码后拼接到一起，使用 `.` 分割。

#### 分布式解决方案

在分布式场景下，同一用户的不同次请求可能会被打到不同的服务器上，这时如果还像单机时那样存储，就会出问题，一般的解决方案包括：

* 粘性 session：将用户绑定到一台服务器上，如 Nginx 负载均衡策略使用 ip_hash, 但这样如果当前服务器发生故障，可能导致分配到这台服务器上的用户登录信息失效，容错度低。
* session 复制：一台服务器的 session 改变，就广播给所有服务器，但会影响服务器性能
* session 共享：把所有服务器的 session 放在一起，如使用 redis 等分布式缓存做 session 集群。
* 客户端记录状态：使用诸如 JWT 之类的方法。

### 连接管理

连接管理是一个 HTTP 的关键话题：打开和保持连接在很大程度上影响着网站和 Web 应用程序的性能。在 HTTP/1.x 里有多种模型：**短连接** ，**长连接**和**HTTP 流水线**

#### 短连接

HTTP 最早期的模型，也是 HTTP/1.x 的默认模型，是短连接。每发起一个HTTP请求都会通过三次握手建立一个TCP连接，在接受到数据之后再通过四次挥手释放连接，因为TCP连接的建立和释放都是一个耗时操作，加之现代网页可能需要多次连续请求才能渲染完成，这就显得这种简单的模型效率低下。

TCP 协议握手本身就是耗费时间的，所以 TCP 可以保持更多的热连接来适应负载。短连接破坏了 TCP 具备的能力，新的冷连接降低了其性能。

为此，HTTP/1.1 时新增加了两种连接管理模式，分别是长连接和流水线，在HTTP/2 中，又基于数据流采用了新的连接管理模式。

#### 长连接

长连接是指在客户端接受完数据后，不立刻关闭这个 TCP 连接，这个连接还可以用来发送和接收其他 HTTP 数据，这样一来可以减少部分连接建立和释放的耗时，但这个连接也并不会一直保持，服务端可以设置 `Keep-alive` 标头来指定一个最小的连接保持时间（单位秒）和最大请求数：

```http
HTTP/1.1 200 OK
Connection: Keep-Alive
Keep-Alive: timeout=5, max=1000
```

>  HTTP/1.0 里默认并不使用长连接。把 [`Connection`](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Headers/Connection) 设置成 `close` 以外的其它参数都可以让其保持长连接，通常会设置为 `retry-after。`
>
>  在 HTTP/1.1 里，默认就是长连接的，协议头都不用再去声明它(但我们还是会把它加上，万一某个时候因为某种原因要退回到 HTTP/1.0 呢)。

长连接并不总是好的，比如，他在空闲状态下仍会消耗服务器资源，而在网络重负载时，还有可能遭受 [DoS ](https://developer.mozilla.org/en-US/docs/Glossary/DoS_attack) 攻击。这种场景下，可以使用非长连接，即尽快关闭那些空闲的连接，也能对性能有所提升。

#### 流水线

默认情况下，HTTP 请求是按顺序发出的。下一个请求只有在当前请求收到应答过后才会被发出。由于会受到网络延迟和带宽的限制，在下一个请求被发送到服务器之前，可能需要等待很长时间。

流水线是在同一条长连接上发出连续的请求，而不用等待应答返回。这样可以避免连接延迟。理论上讲，性能还会因为两个 HTTP 请求有可能被打包到一个 TCP 消息包中而得到提升，就算 HTTP 请求不断的继续导致 TCP 包的尺寸增加，通过设置 TCP 的 [MSS](https://en.wikipedia.org/wiki/Maximum_segment_size)(Maximum Segment Size) 选项，流水线方式仍然足够包含一系列简单的请求。

使用流水线的另一个需要注意的问题是**错误重传**，因此，只有**幂等的方法**，如 GET，HEAD，PUT， DELETE 等方法能够安全地使用流水线。

流水线只是针对客户端来说的，服务器依然和非流水线方式那样工作，这就导致如果第一个请求非常耗时，那流水线上后面的请求就会被阻塞住，这种现象被称为**Head-of-line blocking（队头阻塞）**，除此之外，复杂的网络环境和代理服务器也可能会导致流水线不能像预期的那样高效工作，因此，现代浏览器都没有默认启用流水线，在 HTTP/2 里，有更高效的算法代替了流水线。

#### 三者比较

![](https://cdn.jsdelivr.net/gh/520MianXiangDuiXiang520/cdn@master/img/1610616066018-1610616065992.png)

### CORS

在前后端分离开发时，你也许遇到过类似这样的报错：

```txt
Access to XMLHttpRequest at '*' from origin '*' has been blocked by CORS policy: Response to preflight request doesn't pass access control check: No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

这就是 CORS 的问题了，所谓 **CORS** （Cross-Origin Resource Sharing，跨域资源共享），它首先是一个系统，由一系列 HTTP 头组成，这些 HTTP 头决定了浏览器是否阻止前端 JavaScript 代码获取跨域请求的响应。

之所以需要 CORS，是由于浏览器的同源安全策略：

#### 同源安全策略

同源安全策略用来限制一个源（origin）的文档或者它加载的脚本如何能与另一个源的资源进行交互。它能帮助阻隔恶意文档，减少可能被攻击的媒介。

只有两个 URL 的协议，主机，端口都相同时，他们才被认为是“同源的”，反之，如：`http://www.a.com` 和 `https://www.a.com` 则会被认为是不同源的（协议不同），在默认情况下，同源策略会阻止通过不同源的URL获取资源，而 CORS 就是提供了一种机制，以允许不同源的资源进行共享。

#### 原理

CORS 的原理很简单，它通过添加一组 HTTP 头，允许服务器声明哪些源站通过浏览器有权限访问哪些资源。另外，规范要求，对那些可能对服务器数据产生副作用的 HTTP 请求方法（非简单请求），浏览器必须首先使用 OPTIONS 方法发起一个预检请求，从而获知服务端是否允许该跨源请求。服务器确认允许之后，才发起实际的 HTTP 请求。在预检请求的返回中，服务器端也可以通知客户端，是否需要携带身份凭证（包括 Cookies 或 HTTP 认证相关数据）。

上面说到的 “可能对服务器数据产生副作用的 HTTP 请求” 就是**非简单请求（not-so-simple request）**，与之对应的是**简单请求（simple request）**，同时满足以下几个条件的，属于简单请求。

1. 请求方法是以下三种方法之一：

   * HEAD
   * GET
   * POST
2. 首部字段只包含被用户代理自动设置的首部字段（例如 Connection ，User-Agent）和允许人为设置的字段为 Fetch 规范定义的 [对 CORS 安全的首部字段集合](https://fetch.spec.whatwg.org/#cors-safelisted-request-header)。该集合为：

   * Accept

   * Accept-Language

   * Content-Language

   * Content-Type, 只限于三个值`application/x-www-form-urlencoded`、`multipart/form-data`、`text/plain`

   * DPR

   * Downlink

   * Save-Data

   * Width

   * Viewport-Width
3. 请求中的任意[`XMLHttpRequestUpload`](https://developer.mozilla.org/zh-CN/docs/Web/API/XMLHttpRequestUpload) 对象均没有注册任何事件监听器；[`XMLHttpRequestUpload`](https://developer.mozilla.org/zh-CN/docs/Web/API/XMLHttpRequestUpload) 对象可以使用 [`XMLHttpRequest.upload`](https://developer.mozilla.org/zh-CN/docs/Web/API/XMLHttpRequest/upload) 属性访问。
4. 请求中没有使用 [`ReadableStream`](https://developer.mozilla.org/zh-CN/docs/Web/API/ReadableStream) 对象。

只要有其一不满足，就是费简单请求，非简单请求在正式请求之前会先使用 `OPTION` 方法像服务器发起一个 **预检请求**，如下面这个请求：

```js
var invocation = new XMLHttpRequest();
var url = 'http://bar.other/resources/post-here/';
var body = '<?xml version="1.0"?><person><name>Arun</name></person>';

function callOtherDomain(){
  if(invocation)
    {
      invocation.open('POST', url, true);
      invocation.setRequestHeader('X-PINGOTHER', 'pingpong');
      invocation.setRequestHeader('Content-Type', 'application/xml');
      invocation.onreadystatechange = handler;
      invocation.send(body);
    }
}
```

当前域为 `foo.example.com`,请求 `bar.other`, 属于跨域请求，并且请求时自己添加了一个请求头 `X-PINGOTHER` ,并且 `Content-Type` 类型为 `application/xml`, 所以它属于一个非简单请求，在实际请求之前需要使用 `OPTION` 方法发一个预检请求：

```http
OPTIONS /resources/post-here/ HTTP/1.1
Host: bar.other
User-Agent: Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1b3pre) Gecko/20081130 Minefield/3.1b3pre
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-us,en;q=0.5
Accept-Encoding: gzip,deflate
Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7
Connection: keep-alive
Origin: http://foo.example
Access-Control-Request-Method: POST
Access-Control-Request-Headers: X-PINGOTHER, Content-Type


HTTP/1.1 200 OK
Date: Mon, 01 Dec 2008 01:15:39 GMT
Server: Apache/2.0.61 (Unix)
Access-Control-Allow-Origin: http://foo.example
Access-Control-Allow-Methods: POST, GET, OPTIONS
Access-Control-Allow-Headers: X-PINGOTHER, Content-Type
Access-Control-Max-Age: 86400
Vary: Accept-Encoding, Origin
Content-Encoding: gzip
Content-Length: 0
Keep-Alive: timeout=2, max=100
Connection: Keep-Alive
Content-Type: text/plain
```

预检请求头头中最重要的部分有下面几个：

* `Host`: 要请求的域 
* `Origin`: 发起请求的域，`Host` 和 `Origin` 不一样，说明是跨域请求
* `Access-Control-Request-Method`: 正式的请求将要使用的方法
* `Access-Control-Request-Headers`: 正式请求将携带的自定义字段

服务器在收到这样的预检请求后就可以根据请求头决定是否允许即将发送的实际请求，在服务器的响应中，最重要的字段有以下几个：

* `Access-Control-Allow-Origin`： 服务器允许的域，允许所有域该值设置为 `*`
* `Access-Control-Allow-Methods`: 服务器允许的请求方法，允许所有方法设置为 `*`
* `Access-Control-Allow-Headers`: 服务器允许的请求头
* `Access-Control-Max-Age`: 该响应的有效时间为 86400 秒，也就是 24 小时。在有效时间内，浏览器无须为同一请求再次发起预检请求。

接受到响应后，浏览器会自动判断实际请求是否被允许，如果不被允许，将会报上面的错误。

对于简单请求，通过请求中的 `Origin` 和响应中的 `Access-Control-Allow-Origin` 就可以实现简单的访问控制，如果请求的 `Origin` 不在许可范围内，服务器会返回一个正常的响应，浏览器发现这个响应的头信息没有包含`Access-Control-Allow-Origin`字段，就知道出错了，从而抛出一个错误，被`XMLHttpRequest`的`onerror`回调函数捕获。注意，这种错误无法通过状态码识别，因为HTTP回应的状态码有可能是200。

### HTTP 缓存

> 缓存是一种保存资源副本并在下次请求时直接使用该副本的技术。当 web 缓存发现请求的资源已经被存储，它会拦截请求，返回该资源的拷贝，而不会去源服务器重新下载。这样带来的好处有：缓解服务器端压力，提升性能(获取资源的耗时更短了)。对于网站来说，缓存是达到高性能的重要组成部分。缓存需要合理配置，因为并不是所有资源都是永久不变的：重要的是对一个资源的缓存应截止到其下一次发生改变（即不能缓存过期的资源）。

缓存有很多种，以服务对象分类，缓存可以分为**私有缓存**和**共享缓存**，以行为分类，又可以把它分为**强制缓存**和**对比缓存**。

* 私有缓存：又叫浏览器缓存，只能用于单独用户。浏览器缓存拥有用户通过HTTP下载的所有文档。这些缓存为浏览过的文档提供向后/向前导航，保存网页，查看源码等功能，可以避免再次向服务器发起多余的请求。它同样可以提供缓存内容的离线浏览。
* 共享缓存：又叫代理缓存，共享缓存可以被多个用户使用。例如，ISP 或你所在的公司可能会架设一个 web 代理来作为本地网络基础的一部分提供给用户。这样热门的资源就会被重复使用，减少网络拥堵与延迟。
* 强制缓存：缓存数据未失效时，都可以使用缓存。
* 对比缓存：使用数据前需要请求服务器验证缓存是否失效。

#### 缓存控制

缓存的原理很简单：客户端在从服务器获取到数据后，可以选择将这些数据存储下来，下一次请求同样的数据时，就可以不请求服务器直接返回先前存储的数据了，正确使用缓存可以提高响应速度，降低服务器压力；

这里的客户端可以是浏览器（如私有缓存），也可以是请求链路上的中间代理（如共享缓存），但对服务器来说，他们都是一样的，而服务器并没有办法主动向客户端推送数据，这就导致必须有一种机制去保证缓存是“新鲜”的，HTTP 协议通过一些列的头字段实现了缓存控制，其中最重要的字段是 `Cache-Control`,他有以下几种值：

1. `Cache-Control: no-store`: 禁用缓存，缓存不会存储任何响应数据，每次请求都从服务器获取最新的数据。
2. `Cache-Control: no-cache`: 使用缓存，但需要服务器重新验证，此方式下，每次有请求发出时，缓存会将此请求发到服务器，服务器端会验证请求中所描述的缓存是否过期，若未过期（返回304），则缓存才使用本地缓存副本。
3. `Cache-Control: private`: 私有缓存，表示该响应是专用于某单个用户的，中间人不能缓存此响应，该响应只能应用于浏览器私有缓存中。
4. `Cache-Control: public`:表示该响应可以被任何中间人（比如中间代理、CDN等）缓存。若指定了"public"，则一些通常不被中间人缓存的页面（默认是private）（比如 带有HTTP验证信息（帐号密码）的页面 或 某些特定状态码的页面），将会被其缓存。
5. `Cache-Control: max-age=31536000`: 表示资源能被缓存的最大时间，单位秒。
6. `Cache-Control: must-revalidate`: 缓存在考虑使用一个陈旧的资源时，必须先验证它的状态，已过期的缓存将不被使用。

##### 强制缓存

在某个资源的响应中，如果 `Cache-Control:max-age=31536000`, 则表明这个资源在未来一年内再次请求可以直接从缓存中拿，如第一次请求 avatar.png 时，响应里标明最大有效时间为 600s (10 分钟)，第二次再次请求该资源时，从 size 列就可以看倒该资源直接从缓存返回。 

| 第一次，未使用缓存                                           | 第二次，使用强制缓存                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| ![](https://cdn.jsdelivr.net/gh/520MianXiangDuiXiang520/cdn@master/img/1610700222070-1610700222066.png)![image-20210115164159878](C:\Users\lenovo\AppData\Roaming\Typora\typora-user-images\image-20210115164159878.png) | ![](https://cdn.jsdelivr.net/gh/520MianXiangDuiXiang520/cdn@master/img/1610701195665-1610701195661.png)![](https://cdn.jsdelivr.net/gh/520MianXiangDuiXiang520/cdn@master/img/1610701231118-1610701231114.png) |

这里的缓存就是强制缓存，只要在10分钟内，都可以使用缓存的资源。

如果过了10分钟，缓存中的这个资源就可能是过期了的，这时就需要询问服务器这个资源是不是“新鲜”的，具体客户端会向服务器发起一个携带 `[If-None-Match](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/If-None-Match)` 头的请求：

![](https://cdn.jsdelivr.net/gh/520MianXiangDuiXiang520/cdn@master/img/1610702050715-1610702050705.png)

如果这个资源是“新鲜”的，服务器会返回 [`304`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/304) (Not Modified)（该响应不会有带有实体信息），如果服务器发现这个资源已经过期了，则会返回新的资源。

##### 对比缓存

与强制缓存不同，对比缓存每次使用缓存数据前都会向服务器查询该资源是否有效，但由于查询和响应大部分情况下都只包含头部，所以比起不使用缓存，对比缓存也可以大大提高响应速度和降低服务器压力。它依赖于下面几个头部字段：

* `Last-Modified`: 响应头字段，告诉客户端这个资源最后更新的时间
* `If-Modified-Since`: 请求头字段，如果请求头中携带了这个字段，服务器会将该字段的值和资源最后修改的时间做对比，如果最后修改的时间大于字段值，说明数据已经被修改，则响应 200， 返回最新的资源，否则，响应 304 告诉客户端资源未修改，可以使用缓存。

上面两个头部字段是根据修改时间判断资源是否是新鲜的，这样做的准确度不是很高，还有一组头部字段 `ETag` 和 `If-None-Match` 使用资源的唯一标识来判断资源是否被修改：

* `ETag`: 响应头字段，用于服务器告诉客户端资源的唯一标识（标识的生成规则由服务端确定）
* `If-None-Match`: 请求头字段，如果请求头中包含此字段，服务端会对比该字段的值与最新的资源的标识，如果不相同，说明资源被修改，响应 200， 返回最新的资源，否则，响应 304.

 `ETag` 和 `If-None-Match` 的优先级高于 `Last-Modified` 和 `If-Modified-Since`

除此之外，与缓存相关的还有一个请求头：`Vary`, 用来决定客户端使用新资源还是缓存资源，使用vary头有利于内容服务的动态多样性。例如，使用Vary: User-Agent头，缓存服务器需要通过UA判断是否使用缓存的页面。如果需要区分移动端和桌面端的展示内容，利用这种方式就能避免在不同的终端展示错误的布局。另外，它可以帮助 Google 或者其他搜索引擎更好地发现页面的移动版本，并且告诉搜索引擎没有引入[Cloaking](https://en.wikipedia.org/wiki/Cloaking)。

#### 使用缓存

说了这么多，我们应该怎么通过使用缓存来提高站点的性能呢？

首先，对于私有缓存，开发者一般是不需要关注的，浏览器会自动缓存请求成功的 GET 数据，用来支持后退等功能。我们一般关注的是共有缓存，也就是在代理服务器上缓存数据，客户端请求到代理服务器上后，就可以直接返回了，下面以 Nginx 为例，简单说明如何使用缓存。

```nginx
http {
    # 缓存配置
    proxy_cache_path /usr/share/nginx/cache levels=1:2 keys_zone=server_cache:10m max_size=5g inactive=60m use_temp_path=off;
    # 博客后端反代
    server {
        listen 8888 ssl http2;
        access_log /var/log/nginx/admin/access_fd.log smail;
        error_log /var/log/nginx/admin/error_fd.log;
        location ~ /api/ {
            proxy_cache server_cache;
            proxy_cache_valid 200 304 302 1h;
            proxy_cache_methods GET HEAD POST;
            add_header X-Proxy-Cache $upstream_cache_status;
            proxy_pass http://39.106.168.39:8888;
        }
        error_page 500 502 503 504 /50x.html;
        location = /50x.html {
            root html;
        }
    }
    }
}
```

如上，`proxy_cache_path` 用来配置缓存数据保存的路径，里面的主要字段含义如下：

* `levels`: 在单个目录中包含大量文件会降低文件访问速度，因此我们建议对大多数部署使用两级目录层次结构。如果未包含 `levels` Nginx会将所有文件放在同一目录中。
* `keys_zone`: 设置共享内存区域，用于存储缓存键和元数据,后面的参数表示该区域的大小，一般来说，1 MB区域可以存储大约8,000个 key 数据。
* `max-size`: 缓存能占的最大内存。
* `inactive`：指定项目在未被访问的情况下可以保留在缓存中的时间长度。在此示例中，缓存管理器进程会自动从缓存中删除1分钟未请求的文件，无论其是否已过期。默认值为10分钟（`10m`）。非活动内容与过期内容不同。Nginx 不会自动删除缓存header定义为已过期内容（例如 `Cache-Control:max-age=120`）。过期（陈旧）内容仅在指定时间内未被访问时被删除。访问过期内容时，Nginx 会从原始服务器刷新它并重置`inactive`计时器。

其次，我们在 Location 块中配置了几个值：

*  `proxy_cache`：定义用于缓存的共享内存区域。
* `proxy_cache_valid`: 指定哪些状态的响应可以被缓存。
* `proxy_cache_methods`: 哪些方法的请求可以被缓存。

除此之外，我们添加了一个响应头部字段 `X-Proxy-Cache` 用来查看缓存是否生效。

![](https://cdn.jsdelivr.net/gh/520MianXiangDuiXiang520/cdn@master/img/1610719622498-1610719622485.png)

这里只是简单对数据进行了缓存，服务端没有提供缓存验证的功能，所以可能出现服务端数据已经改变但缓存没更新的情况。

## HTTPS 细节

### 为什么使用 HTTPS

### HTTPS 的原理

#### 密码学基础

##### 对称加密和非对称加密

* 对称加密: 加密和解密时使用的密钥是一样的，比如 DES, 优点是速度快，缺点是在协商密钥时，可能会泄露密钥

* 非对称加密：有两个密钥，公钥和私钥，使用公钥加密，私钥解密，公钥是公开的，比如 RSA。

  > 非对称加密有一个形象的比喻：
  >
  > A有一份机密文件，想要发给B，发之前先向B要一个打开的保险柜，把文件装进保险柜锁住后再发给B，整个过程中保险柜密码只有B知道，这里的保险柜相当于公钥，保险柜密码相当于私钥。

##### CA机构和证书

公钥是公开的，那怎么证明这个公钥是属于你的呢？接上面的比喻，如果有一个中间人 C，在 B 向 A 发保险柜的时候将 B 的保险柜换成自己的发给 A，这样 C 就可以窃取到文件，A 如果想要验证这个保险柜是不是 B 的，就需要一个 A、B 都信任的第三方机构，B 在发给 A 之前请求第三方机构在保险箱上盖一个戳，A 收到后再请求第三方机构检查戳是不是真的就可以了，这里的第三方机构就是 CA　机构，这个戳就是证书，具体来说：

每个CA机构都会有自己的一组密钥对（CA 的公钥是通信双方都信任的），现在 B 有一个公钥，他要证明这个公钥是他的，就需要向 CA 机构请求一份该公钥的证书，请求时，B　需要向 CA 机构提供自己的信息以及要认证的公钥（这些信息会组成CSR文件），CA 机构收到请求后，会检查 CSR 的真实性，检查无误后，CA 会将 CSR 的内容哈希后用自己的私钥签名，然后将 CSR 中的信息和签名组合成证书发给 B。

所以一份证书中包含的典型内容包括：

1. 明文的证书持有者信息
2. 明文的公钥
3. CA 的签名
4. 证书用途，使用的算法，证书过期时间，颁发者信息，CRL分发点等

B 有了 CA 机构的证书，在向 A 发送公钥时就只需要发送证书了，A 收到证书，用 CA 机构的公钥解密签名，然后对证书中的明文数据以同样的算法做哈希，只需要对比两个哈希值就可以判断证书有没有被篡改了，如果证书没被篡改，则可以放心使用证书中的公钥与 B 通信了。

#### HTTPS 通信流程

![image-20210122163508612](C:\Users\lenovo\AppData\Roaming\Typora\typora-user-images\image-20210122163508612.png)

看上面的截图，前三行 [SYN], [SYN, ACK], [ACK] 是典型的 TCP 三次握手，那么在三次握手后，客户端向服务端以 TLSV1.2 协议向服务端发送了一个 `client Hello` 包，通过 `Client Hello`, 客户端会生成一个随机数，并告诉服务端自己支持的加密，哈希等算法，我们可以在这个报文里看到这些内容:

<img src="https://cdn.jsdelivr.net/gh/520MianXiangDuiXiang520/cdn@master/img/1611305883221-1611305883211.png" style="zoom:67%;" />

其中，Random 就是客户端选取的随机数，`Cipher Suites` 中就是客户端支持的算法。

接下来就是 `Server Hello`, 在这一步，服务端同样会生成一个随机数，并且会从客户端支持的算法中选取一种，通过 `Server Hello` 的方式告诉客户端：

<img src="https://cdn.jsdelivr.net/gh/520MianXiangDuiXiang520/cdn@master/img/1611306032992-1611306032983.png" style="zoom:67%;" />

可以看到 `Server Hello` 和 `Client Hello` 的报文内容区别不大，只是 `Client Hello` 中的 `Cipher Suite` 有许多项，而 `Server Hello` 的只有一项，因为服务端会选择安全性最高的加密方式，需要注意的是这里选择的是一组算法，以这里选择的 `0xc02f` 为例,它的名字叫 TLS_ECDHE_RSA_WITH_AES_128_GCM_ SHA256 (0xc02f) 其中包括：

* 密钥交换算法：ECDHE
* 身份验证算法：RSA
* 对称加密算法：AES_128_GCM
* 摘要算法：SHA256

在这之后，服务端在一个 TLS 包里进行了三个负载：

* Certificate：发送证书
* Server Key Exchange：包含密钥交换算法 DHE/ECDHE 所需要的额外参数。
* Server Hello Done：表明服务端相关信息发送结束，这之后服务端会等待客户端响应。

到这一步，客户端已经拿到了服务器的证书，会检查证书是否有效，如果证书失效，客户端浏览器会阻止后续操作，反之，客户端会继续与服务端协商对称加密密钥：

客户端向服务端发送一个响应（id = 67）包含三个负载：

* Client Key Exchange：类似 Server Key Exchange，客户端生成一个新的随机数（Premaster secret），并使用数字证书中的公钥加密后发给服务端。
* Change cipher Spec: 已被废弃，不携带数据
* Encrypted handshake message：这个步骤客户端和服务器在握手完后都会进行，以告诉对方自己在整个握手过程中收到了什么数据，发送了什么数据，保证中间没人篡改报文。

到现在为止，我们总结一下客户端和服务器做了什么：

1. 客户端生成了一个随机数 Client Random 发给了服务端
2. 服务端也生成了一个随机数 Server Random 发给了客户端，同时，双方还协商了以后要用到的哈希，加密算法。
3. 服务端把自己的证书发给了客户端。
4. 客户端又生成了一个新随机数，并用服务端证书中的公钥进行加密后发给了服务端。
5. 客户端和服务端通过互发 Encrypted handshake message 确保了数据没被 中间人篡改。

现在，根据三个随机数，客户端和服务器就会根据约定好的对称加密算法生成最终的对称加密密钥，后续的数据传输就会使用该密钥加密。

##### 总结

HTTPS 建立连接的过程总结如下：

1. TCP 三次握手
2. 客户端向服务器发送 `Client Hello` 包，包含 TLS 版本，客户端生成的随机数 Client Random, 客户端支持的算法等信息
3. 服务器向客户端发送 `Server Hello` 包，包含服务端生成的随机数 Server Random，服务端选择的算法等信息。
4. 服务端向客户端发送证书。
5. 客户端检查证书有效后，生成一个新的随机数 Premaster secret 并用证书中的公钥加密发给服务端。
6. 服务端使用自己的私钥解密 Premaster secret。
7. 客户端和服务端分别使用三个随机数，依照约定的算法生成对话密钥 session key。
8. 客户端和服务端使用 session key 加密后续的会话。

![](https://cdn.jsdelivr.net/gh/520MianXiangDuiXiang520/cdn@master/img/1611310775704-1611310775678.png)

### 使用 HTTPS

nginx 配置示例：

```nginx
    server {
        listen 443 ssl http2;
        server_name *.junebao.top;
        # 证书
        ssl_certificate 1_www.junebao.top_bundle.crt;
        # 私钥
        ssl_certificate_key 2_www.junebao.top.key;
        ssl_session_timeout 5m;
        ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
        ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:HIGH:!aNULL:!MD5:!RC4:!DHE;
        ssl_prefer_server_ciphers on;
        error_page 500 502 503 504 /50x.html;
        location = /50x.html {
            root html;
        }
    }
```



## HTTP/2 细节

### 实现

2015 年，HTTP/2 发布。HTTP/2 是现行 HTTP 协议（HTTP/1.x）的替代，但它不是重写，HTTP 方法/状态码/语义都与 HTTP/1.x 一样。HTTP/2 基于 SPDY3，专注于**性能**，最大的一个目标是在用户和网站间只用一个连接（connection）。

**那么SPDY3是什么呢？**

SPDY是谷歌自行研发的 SPDY 协议，主要解决 HTTP/1.1 效率不高的问题。谷歌推出 SPDY，才算是正式改造 HTTP 协议本身。降低延迟，压缩 header 等等，SPDY 的实践证明了这些优化的效果，也最终带来 HTTP/2 的诞生。

HTTP/2 由两个规范（Specification）组成：

1. Hypertext Transfer Protocol version 2 - [RFC7540](https://tools.ietf.org/html/rfc7540)
2. HPACK - Header Compression for HTTP/2 - [RFC7541](https://tools.ietf.org/html/rfc7541)

**那么HTTP2在HTTP1.1的基础上做了哪些改进**

- 二进制传输
- 请求和响应复用
- Header压缩
- Server Push（服务端推送）

#### 二进制传输

HTTP/2 采用二进制格式传输数据，而非 HTTP 1.x 的文本格式，二进制协议解析起来更高效。 HTTP / 1 的请求和响应报文，都是由起始行，首部和实体正文（可选）组成，各部分之间以文本换行符分隔。**HTTP/2 将请求和响应数据分割为更小的帧，并且它们采用二进制编码**。

新的二进制分帧机制改变了客户端与服务器之间交换数据的方式。 为了说明这个过程，我们需要了解 HTTP/2 的三个概念：

- *数据流*：已建立的连接内的双向字节流，可以承载一条或多条消息。
- *消息*：与逻辑请求或响应消息对应的完整的一系列帧。
- *帧*：HTTP/2 通信的最小单位，每个帧都包含帧头，至少也会标识出当前帧所属的数据流。

这些概念的关系总结如下：

- 所有通信都在一个 TCP 连接上完成，此连接可以承载任意数量的双向数据流。
- 每个数据流都有一个唯一的标识符和可选的优先级信息，用于承载双向消息。
- 每条消息都是一条逻辑 HTTP 消息（例如请求或响应），包含一个或多个帧。
- 帧是最小的通信单位，承载着特定类型的数据，例如 HTTP 标头、消息负载等等。 来自不同数据流的帧可以交错发送，然后再根据每个帧头的数据流标识符重新组装。

#### 请求和响应复用

在 HTTP/1.x 中，如果客户端要想发起多个并行请求以提升性能，则必须使用多个 TCP 连接，这是 HTTP/1.x 交付模型的直接结果，该模型可以保证每个连接每次只交付一个响应（响应排队）。 更糟糕的是，这种模型也会导致队首阻塞，从而造成底层 TCP 连接的效率低下。

HTTP/2 中新的二进制分帧层突破了这些限制，实现了完整的**请求和响应复用**：客户端和服务器可以将 HTTP 消息分解为互不依赖的帧，然后交错发送，最后再在另一端把它们重新组装起来。

在 HTTP/2 中，有了二进制分帧之后，HTTP /2 不再依赖 TCP 链接去实现多流并行了，在 HTTP/2 中：

- 同域名下所有通信都在单个连接上完成。
- 单个连接可以承载任意数量的双向数据流。
- 数据流以消息的形式发送，而消息又由一个或多个帧组成，多个帧之间可以乱序发送，因为根据帧首部的流标识可以重新组装。

这一特性，使性能有了极大提升：

- 同个域名只需要占用一个 TCP 连接，使用一个连接并行发送多个请求和响应,消除了因多个 TCP 连接而带来的延时和内存消耗。
- 并行交错地发送多个请求，请求之间互不影响。
- 并行交错地发送多个响应，响应之间互不干扰。
- 在 HTTP/2 中，每个请求都可以带一个 31bit 的优先值，0 表示最高优先级， 数值越大优先级越低。有了这个优先值，客户端和服务器就可以在处理不同的流时采取不同的策略，以最优的方式发送流、消息和帧。

![](https://cdn.jsdelivr.net/gh/kklll/Resources@master/pics/2019-03-06-4.png)

#### Header压缩

在 HTTP/1 中，我们使用文本的形式传输 header，在 header 携带 cookie 的情况下，可能每次都需要重复传输几百到几千的字节。为了减少这块的资源消耗并提升性能，HTTP/2 使用 HPACK 压缩格式压缩请求和响应标头元数据，这种格式采用两种强大的技术：

1. 这种格式支持通过**静态霍夫曼代码对传输的标头字段进行编码**，从而减小了各个传输的大小。
2. 这种格式要求客户端和服务器同时维护和更新一个包含之前见过的标头字段的**索引列表**（换句话说，它可以建立一个共享的压缩上下文），此列表随后会用作参考，对之前传输的值进行有效编码。

利用霍夫曼编码，可以在传输时对各个值进行压缩，而利用之前传输值的索引列表，我们可以通过传输索引值的方式对重复值进行编码，索引值可用于有效查询和重构完整的标头键值对。

作为一种进一步优化方式，HPACK 压缩上下文包含一个静态表和一个动态表：静态表在规范中定义，并提供了一个包含所有连接都可能使用的常用 HTTP 标头字段（例如，有效标头名称）的列表；动态表最初为空，将根据在特定连接内交换的值进行更新。 因此，为之前未见过的值采用静态 Huffman 编码，并替换每一侧静态表或动态表中已存在值的索引，可以减小每个请求的大小。

注：在 HTTP/2 中，请求和响应标头字段的定义保持不变，仅有一些微小的差异：所有标头字段名称均为小写，请求行现在拆分成各个 `:method`、`:scheme`、`:authority` 和 `:path` 伪标头字段。

如需了解有关 HPACK 压缩算法的完整详情，请参阅 [IETF HPACK - HTTP/2 的标头压缩](https://tools.ietf.org/html/draft-ietf-httpbis-header-compression)。

#### Server Push

HTTP/2 新增的另一个强大的新功能是，服务器可以对一个客户端请求发送多个响应。 换句话说，除了对最初请求的响应外，服务器还可以向客户端推送额外资源如下图所示，而无需客户端明确地请求。

为什么在浏览器中需要一种此类机制呢？一个典型的网络应用包含多种资源，客户端需要检查服务器提供的文档才能逐个找到它们。 那为什么不让服务器提前推送这些资源，从而减少额外的延迟时间呢？ 服务器已经知道客户端下一步要请求什么资源，这时候服务器推送即可派上用场。

事实上，如果您在网页中内联过 CSS、JavaScript，或者通过数据 URI 内联过其他资产（请参阅[资源内联](https://hpbn.co/http1x/#resource-inlining)），那么您就已经亲身体验过服务器推送了。 对于将资源手动内联到文档中的过程，我们实际上是在将资源推送给客户端，而不是等待客户端请求。 使用 HTTP/2，我们不仅可以实现相同结果，还会获得其他性能优势。 推送资源可以进行以下处理：

- 由客户端缓存
- 在不同页面之间重用
- 与其他资源一起复用
- 由服务器设定优先级
- 被客户端拒绝

##### 服务端推送如何实现

所有服务器推送数据流都由 `PUSH_PROMISE` 帧发起，表明了服务器向客户端推送所述资源的意图，并且需要先于请求推送资源的响应数据传输。 这种传输顺序非常重要：客户端需要了解服务器打算推送哪些资源，以免为这些资源创建重复请求。 满足此要求的最简单策略是先于父响应（即，`DATA` 帧）发送所有 `PUSH_PROMISE` 帧，其中包含所承诺资源的 HTTP 标头。

在客户端接收到 `PUSH_PROMISE` 帧后，它可以根据自身情况选择拒绝数据流（通过 `RST_STREAM` 帧）。 （例如，如果资源已经位于缓存中，便可能会发生这种情况。） 这是一个相对于 HTTP/1.x 的重要提升。 相比之下，使用资源内联（一种受欢迎的 HTTP/1.x“优化”）等同于“强制推送”：客户端无法选择拒绝、取消或单独处理内联的资源。

使用 HTTP/2，客户端仍然完全掌控服务器推送的使用方式。 客户端可以限制并行推送的数据流数量；调整初始的流控制窗口以控制在数据流首次打开时推送的数据量；或完全停用服务器推送。 这些优先级在 HTTP/2 连接开始时通过 `SETTINGS` 帧传输，可能随时更新。

### 过渡到 HTTP/2

上面说了这么多，我们要如何启用HTTP2呢？

如果你使用的是 nginx，那么你只需要加一个 `http2` 即可：

```nginx
server {
    listen 8888 ssl http2;
    server_name *.junebao.top;
    # ...
}
```

如果你使用 Golang 的 Gin 框架，他默认支持 HTTP/2，你可以使用 `RunTLS()` 使用 HTTP/2,如下：

```go
package main

import (
    "github.com/gin-gonic/gin"
)

func main() {
    engine := gin.Default()
    engine.GET("./", func(context *gin.Context) {
        context.JSON(200, map[string]string{"msg": "ok"})
    })
    // 服务端推送
    engine.Static("/static", "./static")
    engine.GET("/push", func(context *gin.Context) {
        pusher := context.Writer.Pusher()
        if pusher != nil {
            err := pusher.Push("/static/test.js", nil)
            if err != nil {
                log.Println("push fail", err)
            }
        }
        context.JSON(200, map[string]string{"msg": "ok"})
    })
    engine.RunTLS(":8888", "./root_cer.cer", "./root_private_key.pem")
}
```

如果你使用的是 spring boot 内置的 Tomcat 服务器，那么只需要在配置文件中添加配置：

```yaml
server:
  http2:
    enabled: on
```

只有 Tomcat 9 版本之后版本才支持 HTTP/2 协议。在 conf/server.xml 中增加内容：

```xml
<Connector port="8443" protocol="org.apache.coyote.http11.Http11AprProtocol" maxThreads="150" SSLEnabled="true">
<UpgradeProtocol className="org.apache.coyote.http2.Http2Protocol"/>
<SSLHostConfig honorCipherOrder="false">
<Certificate certificateKeyFile="conf/ca.key" certificateFile="conf/ca.crt"/>
</SSLHostConfig>
</Connector>
```

## HTTP/3 细节

### 为什么要出现HTTP3

虽然 HTTP/2 解决了很多之前旧版本的问题，但是它还是存在一个巨大的问题，主要是底层支撑的 `TCP 协议`造成的。

上文提到 HTTP/2 使用了多路复用，一般来说同一域名下只需要使用一个 TCP 连接。但当这个连接中出现了丢包的情况，那就会导致 HTTP/2 的表现情况反倒不如 HTTP/1 了。

因为在出现丢包的情况下，整个 TCP 都要开始等待重传，也就导致了后面的所有数据都被阻塞了。但是对于 HTTP/1.1 来说，可以开启多个 TCP 连接，出现这种情况反到只会影响其中一个连接，剩余的 TCP 连接还可以正常传输数据。

那么可能就会有人考虑到去修改 TCP 协议，其实这已经是一件不可能完成的任务了。因为 TCP 存在的时间实在太长，已经充斥在各种设备中，并且这个协议是由操作系统实现的，更新起来不大现实。

基于这个原因，**Google 就更起炉灶搞了一个基于 UDP 协议的 QUIC 协议，并且使用在了 HTTP/3 上**，HTTP/3 之前名为 HTTP-over-QUIC，从这个名字中我们也可以发现，HTTP/3 最大的改造就是使用了 QUIC（快速 UDP Internet 连接）。

### QUIC 

> QUIC（Quick UDP Internet Connection）是谷歌制定的一种基于UDP的低时延的互联网传输层协议。在2016年11月国际互联网工程任务组(IETF)召开了第一次QUIC工作组会议，受到了业界的广泛关注。这也意味着QUIC开始了它的标准化过程，成为新一代传输层协议 。

优势：

1. 高效地建立连接: 将 TLS 协商密钥和协议作为打开连接握手地一部分，加上对 client Hello 地缓存，在大部分情况下，QUIC 建立连接只需要 0RTT，而普通的 HTTPS 则至少需要 2RTT
2. 改进地拥塞控制方案：TCP 拥塞控制包括：慢启动，拥塞避免，快速重传，快速恢复，QUIC 在 UDP 基础上实现了相关算法并做了改进，使之具有可插拔，高效地特点。
3. 基于 stream 和 connecton 级别的流量控制。
4. 没有 TCP 队头阻塞地多路复用：HTTP/2 通过二进制分帧层避免了 HTTP 队头阻塞，但由于依然使用 TCP 协议，就避免不了 TCP 队头阻塞，QUIC 基于 UDP，多个 stream 之间没有依赖。这样假如 stream2 丢了一个 udp packet，也只会影响 stream2 的处理。不会影响 stream2 之前及之后的 stream 的处理，这也就在很大程度上缓解甚至消除了队头阻塞的影响。
5. 加密认证地报文:TCP 协议头部没有经过任何加密和认证，所以在传输过程中很容易被中间网络设备篡改，注入和窃听。比如修改序列号、滑动窗口。这些行为有可能是出于性能优化，也有可能是主动攻击。但是 QUIC 的 packet 可以说是武装到了牙齿。除了个别报文比如 PUBLIC_RESET 和 CHLO，所有报文头部都是经过认证的，报文 Body 都是经过加密的.
6. 连接迁移:一条 TCP 连接是由四元组标识的（源 IP，源端口，目的 IP，目的端口）。什么叫连接迁移呢？就是当其中任何一个元素发生变化时，这条连接依然维持着，能够保持业务逻辑不中断。当然这里面主要关注的是客户端的变化，因为客户端不可控并且网络环境经常发生变化，而服务端的 IP 和端口一般都是固定的,而 QUIC 连接不再以 IP 及端口四元组标识，而是以一个 64 位的随机数作为 ID 来标识，这样就算 IP 或者端口发生变化时，只要 ID 不变，这条连接依然维持着，上层业务逻辑感知不到变化，不会中断，也就不需要重连。由于这个 ID 是客户端随机产生的，并且长度有 64 位，所以冲突概率非常低。
7. 向前纠错: 每个数据包除了它本身的内容之外，还包括了部分其他数据包的数据，因此少量的丢包可以通过其他包的冗余数据直接组装而无需重传。向前纠错牺牲了每个数据包可以发送数据的上限，但是减少了因为丢包导致的数据重传，因为数据重传将会消耗更多的时间(包括确认数据包丢失、请求重传、等待新数据包等步骤的时间消耗);假如说这次我要发送三个包，那么协议会算出这三个包的异或值并单独发出一个校验包，也就是总共发出了四个包。当出现其中的非校验包丢包的情况时，可以通过另外三个包计算出丢失的数据包的内容。**当然这种技术只能使用在丢失一个包的情况下，如果出现丢失多个包就不能使用纠错机制了，只能使用重传的方式了**。
8. 证书压缩等.

可见HTTP3在效率上和安全性上都有了很大程度上的修改，但是由于目前这个标准还在论证中，Nginx等也只是在测试版中加入了对HTTP3的支持，等到技术真正的论证实现完成，我们就可以使用上快速且安全的HTTP3协议了，期待着这一天的到来。

## 参考

[mozilla 开发文档](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Basics_of_HTTP/Evolution_of_HTTP)

[谷歌开发文档 HTTP2 简介](https://developers.google.com/web/fundamentals/performance/http2?hl=zh-cn)

[Nginx缓存最佳实践](https://blog.text.wiki/2017/04/10/nginx-cache.html)

[让互联网更快：新一代QUIC协议在腾讯的技术实践分享](http://www.52im.net/thread-1407-1-1.html)