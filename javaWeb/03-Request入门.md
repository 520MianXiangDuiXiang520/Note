# Request(获取用户发出的请求数据)

## 继承关系

```java
interface ServletRequest{}
interface HttpServletRequest extends ServletRequest{}
class org.apache.catalina.connector.RequestFacade implements HttpServletRequest{}
```

## 功能

### 获取请求行数据

假设请求行为

```txt
GET /demo/demo1?username=zhangsan HTTP/1.1
```

1. 获取请求方式 GET

```java
String getMethod()
```

2. 获取虚拟目录 /demo

```java
String getContextPath()
```

3. 获取Servlet路径 /demo1

```java
String getSeleletPath()
```

4. 获取get方式请求的参数 username=zhangsan

```java
String getQueryString()
```

5. 获取请求URI /demo/demo1

```java
String getRequestURI()  // demo/demo1
StringBuffer getRequestURL() // http://localhost/dem0/demo1
```

6. 获取协议及版本 HTTP/1.1

```java
String getProtocol()
```

7. 获取客户机IP

```java
String getRemoteAddr()
```

### 获取请求头数据

1. 通过请求头名称获取请求头

```java
String getHeader(String name)
```

2. 获取所有请求头名称(Enumeration是一个“迭代器”)

```java
Enumeration<String> getHeaderNames()
```

### 获取请求体参数

1. 获取字符输入流（只能操作字符数据）

```java
BufferedReader getReader()
```

2. 获取字节输入流（可操作所有类型的数据）

```java
ServletInputStream getInputStream()
```

### 其他常用方法

#### 获取请求参数的通用方式

1. 根据参数名称获取参数值(GET)

```java
String getParameter(String name)
```

2. 根据参数名获取参数值数组

```java
String[] getParameter(String name)
```

3. 获取所有请求参数名称

```java
Enumeration<String> getparameterNames()
```

4. 获取所有参数的Mep集合

```java
Map<String, String[]> getParameterMap()
```

5. 解决post中文乱码问题

```java
setCharacterEncoding("utf-8")
```

#### 请求转发

服务器内部的资源跳转

先通过request对象的`getRequestDispatcher()`方法获取一个请求转发器（RequestDispatcher
）对象，再调用他的`forward()`方法转发

```java
req.getRequestDispatcher("/Demo3").forward(req, resp);
```

#### 数据共享

1. 域对象： 一个有作用范围的对象
2. request域：一次请求的范围（转发是一次请求）

方法：

1. `setAttribute(String name, Object obj)` 存储数据
2. `Object getAttribute(String name)` 通过键值获取数据
3. `void removeAttribute(String name)` 通过键移除键值对
