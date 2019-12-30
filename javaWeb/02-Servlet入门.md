# Servlet入门

Servlet（Server applet）【允许在服务器端的小程序】是一个定义了使Java类能被浏览器访问的规则的接口。

实质：一个接口，实现这个接口的类就能被tomcat所识别

```java
package top.junebao;

import javax.servlet.*;
import java.io.IOException;

public class Demo implements Servlet {
    /**
     * 初始化方法，在servlet被创建时执行，只执行一次
     * @param servletConfig
     * @throws ServletException
     */
    @Override
    public void init(ServletConfig servletConfig) throws ServletException {
        System.out.println("init___");
    }

    @Override
    public ServletConfig getServletConfig() {
        return null;
    }

    /**
     * 用来提供服务的方法，每一次servlet被访问时都会执行
     * @param servletRequest
     * @param servletResponse
     * @throws ServletException
     * @throws IOException
     */
    @Override
    public void service(ServletRequest servletRequest, ServletResponse servletResponse) throws ServletException, IOException {
        System.out.println("hhhhhh");
    }

    @Override
    public String getServletInfo() {
        return null;
    }

    /**
     * 销毁方法，服务器关闭时执行，只执行一次
     */
    @Override
    public void destroy() {
        System.out.println("destroy");
    }
}

```

## servlet配置

servlet的配置在web.xml中，需要为Java类与url资源绑定起来（类似于Django的url调度器）：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee http://xmlns.jcp.org/xml/ns/javaee/web-app_4_0.xsd"
         version="4.0">
    <servlet>
        <servlet-name>demo1</servlet-name>
        <!-- 绑定Java类 -->
        <servlet-class>top.junebao.Demo</servlet-class>
    </servlet>
    <servlet-mapping>
        <servlet-name>demo1</servlet-name>
        <url-pattern>/demo</url-pattern>
    </servlet-mapping>
</web-app>
```

## servlet的生命周期

### 创建

servlet创建的时机可以在`web.xml`中通过`<load-on-startup></load-on-startup>`设置，如果值为负数（默认），就是在第一次访问时创建，如果为0或正数，则在服务器开启时创建

```xml
<servlet>
    <servlet-name>demo1</servlet-name>
    <servlet-class>top.junebao.Demo</servlet-class>
<!--        设置servlet加载的时机-->
    <load-on-startup>5</load-on-startup>
</servlet>
```

servlet是单例的，多个用户同时访问时存在安全问题，尽量不要再servlet中定义成员变量，哪怕定义也不能去修改。

### 销毁

服务器正常关闭时，执行destroy()方法

## servlet3.0注释配置

```java
import javax.servlet.*;
import javax.servlet.annotation.WebServlet;
import java.io.IOException;

@WebServlet("/demo2")
public class Demo implements Servlet {
}
```

可以配置多个

```java
@WebServlet({"/xxx", "/xo", "/xoxx/xx"})
public class Demo implements Servlet {
}
```

也可以使用通配符(`*`的优先级很低，只有别的都匹配不到才会匹配`*`)

```java
@WebServlet("/*")
public class Demo implements Servlet {
}
```

也可以匹配特定后缀（不能写`/`）

```java
@WebServlet("*.do")
public class Demo implements Servlet {
}
```

## servlet的继承体系结构

```java
interface Servlet{} 
abstract class GenericServlet implements Servlet{}
abstract class HttpServlet extends GenericServlet{}
```

* GenericServlet将Servlet中除了service之外的方法都做了空白实现
* HttpServlet 分装了判断请求方式的代码,什么请求的逻辑只需要写`doPost()`,`doGet()`等方法就行

```java
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

@WebServlet("/http")
public class Demo3 extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
//        super.doGet(req, resp);
        System.out.println("get");
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
//        super.doPost(req, resp);
        System.out.println("post");
    }
}
```
