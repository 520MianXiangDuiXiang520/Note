# Tomcat的使用

## 下载与安装

[下载地址](http://mirror.bit.edu.cn/apache/tomcat/tomcat-8/v8.5.50/bin/apache-tomcat-8.5.50-windows-x64.zip)

安装直接解压压缩包（不能有中文路径）

## 配置
1. 启动：
  * windows `bin/startup.bat`
  * linux `bin\startup.sh`
2. 关闭：
  * 正常关闭：`bin/shutdown.bat`
3. 修改默认端口：

tomcat默认8080端口，修改`conf/server.xml`中的一下字段修改默认端口

```xml
<Connector port="8080" protocol="HTTP/1.1"
            connectionTimeout="20000"
            redirectPort="8443" />
```

### 项目发布

1. 直接将项目放在`webapps`目录下
2. 打包成`war`包放在`webapps`下，自动解压
3. 配置`conf/server.xml`在`<Host>`中配置

```xml
<Content doBase="E:\phpstudy_pro\WWW\FPMS" path="/fpms"/>
```

4. `conf\catalina\localhost`下创建任意名称的xml文件

```xml
<Content doBase="E:\phpstudy_pro\WWW\FPMS/>
```