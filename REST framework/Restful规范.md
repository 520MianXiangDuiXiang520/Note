# Restful 规范

## REST

Representational State Transfer(表象层状态转变)

## RESTful原则

RESTful就是对对接口的约束规范，有六大原则

1. C-S架构：数据存储在Server端，Client只使用，使得客户端代码可移植性强，服务端可拓展性强，两端可单独开发，互不干扰
2. 无状态：
3. 统一的接口：
4. 一致的数据格式
5. 系统分层
6. 可缓存

## 具体

1. url书写规范

```txt
# 域名/api/版本号/数据？参数
http://www.demo.com/api/v1/index?token=vhvh-bh-hbh
```

一条数据使用一个url，具体操作根据methor区分

2. 统一的数据格式

* code: http状态码
* status：包含"success","fail"或"error"
* message:状态值为"fail"或"error"时包含错误信息
* data: 包含响应主体，请求失败应包含错误信息或null

```json
{
    "code": 200,
    "message": "success",
    "data": {
        "token": "b87njug-jnjkhbwc-hugbhxs",
        "link": "http://www.demo.com/api/v1/index?token=vhvh-bh-hbh"
    }
}
```

```json
{
    "code": 401,
    "message": "error",
    "data": {
        "error_info": "缺乏用户凭证"
    }
}
```

1. 
2. 建议使用https
3. 建议使用专用域名（子域名【跨域问题】或专用url）
4. 版本
5. 面向资源编程（url名词）
6. method： get post put patch delete
7. 过滤，url加条件
8. 状态码code
9. 错误处理
10. 返回值