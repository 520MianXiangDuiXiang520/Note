# CSRF

[参考掘金](https://juejin.im/post/5bc009996fb9a05d0a055192)

## CSRF攻击

### 什么是CSRF

跨站请求伪造

### 攻击流程：

* 受害者正常登录站点a，保留cookie
* 攻击者诱导受害者访问恶意站点b
* 站点b向a发送请求，由于受害者的cookie还在，浏览器会默认为b携带a的cookie
* b以受害者的身份请求a站点

### CSRF类型

* get
* post
* 链接类型

### 特点

* 攻击者不能拿到cookie
* 攻击一般从第三方网站发起

## CSRF防御

### 同源检测

Referer，判断头部的Referer是否是同源地址

### Token

用户登录时产生一个随机值，加入到所有的a和from标签之后，并保存到服务器session中，每次请求判断token是否有效

* 优点：比同源检查有效
* 缺点：分布式无法使用，占用服务器内存

### 分布式校验

Token值由userid，时间戳等加密形成，服务器不需要存储Token，只用在用户请求时计算token的userid是否存在即可

* 缺点：使用麻烦，每个a和from都得加，js动态加载的页面需要手工写

### 双重cookie校验

* 在用户访问网站页面时，向请求域名注入一个Cookie，内容为随机字符串
* 在前端向后端发起请求时，取出Cookie，并添加到URL的参数中
* 后端接口验证Cookie中的字段与URL参数中的字段是否一致，不一致则拒绝。

### Samesite Cookie属性

Samesite=Strict
严格模式

Samesite=Lax
宽松模式