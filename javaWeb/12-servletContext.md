# ServletContext

该对象代表整个Web应用，可以用来与servlet容器（服务器）通信，通过`getServletContext()`获取

## 1. 功能

### 获取MIME类型

#### MIME类型

在互联网通信过程中定义的一种文件数据类型，格式是`大类型/小类型` 如`text/html`或`image/jpg`

获取MIME类型：

```java
String getMimeType(String file)
```

示例

```java
public class TestMime extends HttpServlet {
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) {
        ServletContext context = this.getServletContext();
        String fileName = "01.jpeg";
        String mimeType = context.getMimeType(fileName);
        System.out.println(mimeType);// image/jpeg
    }
     
}
```


### 域对象：共享数据

1. `setAttribute(String name, Object obj)` 存储数据
2. `Object getAttribute(String name)` 通过键值获取数据
3. `void removeAttribute(String name)` 通过键移除键值对

与request域不同的是，ServletContext域是整个web应用，也就是所以用户共享这个数据，服务器开启时创建，关闭时销毁。要谨慎使用。

### 获取文件真实路径（服务器路径）

```
String realPath = getRealPath(String filePath);
```

