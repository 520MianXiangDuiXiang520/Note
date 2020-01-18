# Response对象

功能：设置响应消息

1. 设置响应行
  * 设置状态码：`setStatus(int sc)`
2. 设置响应头: `setHeader(String name, String value)`
3. 设置响应体: 
  1. 获取输出流
    * 字符输出流 `PrintWriter getWriter()`
    * 字节输出流 `ServletOutputStream getOutputStream()`
  2. 使用输出流将数据输出到浏览器

## 使用

### 重定向

原理

```java
response.setStatus(302);
response.setHeader("location", "/newServlet");
```

封装简化

```java
response.sendRedirect("/newServlet");
```

### 设置编码

```java
response.setContentType("text/html;charset=utf-8");
```