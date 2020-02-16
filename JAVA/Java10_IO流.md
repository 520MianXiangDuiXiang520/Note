# Java IO流

## 1. 是什么

* IO: input/output
* 流：管道

IO流可以理解为Java程序进行数据传输的管道

## 2. File 类概述

计算机中所有数据都是通过文件储存的，Java把文件也当作一个对象，对应的类就是File类，在`java.io`包下

> 是文件和目录路径的抽象表示

### 2.1 构造方法

> File​(String pathname) 通过将给定的路径名字符串转换为抽象路径名来创建新的 File实例。  通过将给定的路径名字符串转换为抽象路径名来创建新的File实例。 如果给定的字符串是空字符串，则结果是空的抽象路径名。

```java
public static void main(String[] args) {
        // Java 中一个 “\” 表示转义开始
        File file = new File("E:\\桌面文件\\JAVA\\src\\demo.txt");
    }
```


> File​(String parent, String child) 从父路径名字符串和子路径名字符串创建新的 File实例。 

```java
File file1 = new File("E:\\桌面文件\\JAVA\\src", "demo.txt");
```

第一个参数传入父级路径字符串，第二个参数传入相对父级路径的子路径名
 

> File​(File parent, String child) 从父抽象路径名和子路径名字符串创建新的 File实例。 

```java
File file2 = new File("E:\\桌面文件\\JAVA\\src");
File file3 = new File(file2, "demo.txt");
```

File​(URI uri) 通过将给定的 file: URI转换为抽象路径名来创建新的 File实例。 

### 2.2 成员方法

#### 2.2.1 创建

|成员方法|功能|参数介绍|返回值介绍|异常|备注|
|----------|---|----|------|----|----|----|
|`public boolean createNewFile()`|创建文件，如果存在就不创建|——|创建成功返回true,文件存在或创建失败返回false|`IOException`|路径不存在抛出IOException异常|
|`public boolean mkdir​()`|创建文件夹|无|返回是否创建成功|`IOException`|父路径不存在返回false|
|`public boolean mkdirs​()`|创建多级目录|无|返回是否成功|`IOException`|路径不存在就创建|

#### 2.2.2 删除

|成员方法|功能|参数介绍|返回值介绍|异常|备注|
|----------|---|----|------|----|----|----|
|`public boolean delete​()`|删除文件或文件夹|无|返回是否删除成功||1. 文件不存在返回false 2. 删除文件夹时只能删除空文件夹|

#### 2.2.3 重命名或移动

|成员方法|功能|参数介绍|返回值介绍|异常|备注|
|----------|---|----|------|----|----|----|
|`public boolean renameTo​(File dest)`|重命名文件|dest:重命名文件的新的抽象路径名|返回是否重命名成功|可以使用这个方法实现移动（剪贴）功能|

#### 2.2.4 判断

|成员方法|功能|参数介绍|返回值介绍|异常|备注|
|----------|---|----|------|----|----|----|
|`public boolean isDirectory​()`|判断是否是目录|无|返回是否是目录||只有是目录且目录存在时返回true|
|`public boolean isFile​()`|判断是否是文件|无|返回是否是文件|||
|`public boolean isHidden​()`|判断是否是隐藏文件|无|··||UNIX中，以`.`开头的是隐藏文件，而window中，特殊标记过的是隐藏文件|
|`public boolean exists​()`|判断文件或目录是否存在|无|返回是否存在|||
|`public boolean canWrite​()`|判断文件是否可写|无|返回是否可写|| |
|`public boolean canRead​()` |判断文件是否可读|无|返回是否可读|||
|`public boolean isAbsolute​()`|判断路径是否是绝对路径|无|||在UNIX系统上，如果前缀为"/" ，路径名是绝对的。 在Windows系统上，前面是盘符或`///`为绝对路径|

#### 2.2.5 获取功能
|成员方法|功能|参数介绍|返回值介绍|异常|备注|
|----------|---|:----:|:------:|:----:|----|----|
|`public String getName​()`|返回文件或目录名称|无|String||这个方法只是对路径字符串的分割操作，不检查路径是否存在|
|`public String getParent​()`|返回文件或文件夹父路径名字符串|无|String||也只是字符串的分割操作，不检查路径或文件是否真实存在|
|`public File getParentFile​()`|返回文件或文件夹的父路径的File对象|无|File||内部调用的是getParent()方法|
|`public String getPath​()`|返回文件路径|无|String|||
|`public String getAbsolutePath​()`|返回绝对路径|无|String||同样不关心文件是否存在|
|`public File getAbsoluteFile​()`|返回绝对形式的File对象|无|File|||
|`public String getCanonicalPath​()`|返回文件规范路径名字符串|无|String|IOException|先转换成绝对路径，然后删除`.`,`..`等冗余名称等。。|
|`public File getCanonicalFile​()`|返回文件规范路径名的File对象|||IOException||
|`public long lastModified​()`|返回文件上次修改时间|无|Long 返回一个时间戳||如果文件不存在返回0|
|`public long length​()`|返回文件长度|无|Long 文件长度，以字节为单位||文件不存在返回0|
|`public String[] list​([FilenameFilter filter])`|返回该目录下所有文件和目录的数组|可以传入一个FilenameFilter filter，表示列出满足过滤器的文件或目录名||||
|`public File[] listFiles​([FilenameFilter filter])`|类似于上面|||||

#### 2.2.6 设置

以set开头的一些成员方法，不整理了

## 3. IO流的分类

1. 根据数据流向分：输入流，输出流
  * 相对于当前程序而言
2. 按照内容分：字节流，字符流
  * 字节数据：二进制
    * 字节输入流：abstract InputSteam
    * 字节输出流: abstract OutputSteam
  * 字符数据：文本
    * 字符输入流：Reader
    * 字符输出流：Writer

## 4. 字节输出流

字节输入流的基类是`abstract Class OutputStream`,由他派生的有`FileOutputStream`, `ByteArrayOutputStream`  `FilterOutputStream` ， `ObjectOutputStream`， `PipedOutputStream`等。

成员方法：

1. `void close()`: 关闭输出流，并释放与之相关的系统资源
2. `void flush​()`: 刷新此输出流并强制任何缓冲的输出字节被写出。 
3. `void write(bite[] b)`: 将字节数组中的内容写入输出流
4. `void write​(byte[] b, int off, int len)`: 将字节数组中第`off ~ off+len`的内容写入输出流。

### 4.1 FileOutPutStream

作用：将字节写入到文件

#### 4.1.1 常用构造方法

* `FileOutputStream​(File file)`和`FileOutputStream​(String nane)`:将字节流输出到特定的文件
* `FileOutputStream​(File file, boolean append)`和`FileOutputStream​(String name, boolean append)`: 第二个参数append是追加写开关，append为true时，写的方式为追加写，否则为覆盖写。

#### 4.1.2 成员方法

`void write​(int b)`： 将指定的字节写入此文件输出流

```java
public static void main(String[] args) throws IOException {
        FileOutputStream fos = new FileOutputStream(new File("demo2.txt"));
        byte[] bytes = "Hello IO".getBytes();
        fos.write(bytes);
        fos.close();

        FileOutputStream fos2 = new FileOutputStream(new File("demo2.txt"), true);
        fos2.write(36);
        
        // 默认查看ASCII,如果有负数，或者超过127，就会按照系统编码规则，和后面的一个或两个一起组成一个
        byte [] bytes1 = {37, 38, 39, 40, 41, -42, 43, 44};
        fos2.write(bytes1);
        fos2.write("\n".getBytes());
        fos2.write(bytes1, 2, 2);
        fos2.close();
    }
```

## 5. 字节输入流

基类是`abstract class InputStream`由他派生的有 AudioInputStream ， ByteArrayInputStream ， FileInputStream ， FilterInputStream ， InputStream ， ObjectInputStream ， PipedInputStream ， SequenceInputStream ， StringBufferInputStream 

常用成员函数

1. `int available​()`:
2. `void close​()`:
3. `void mark​(int readlimit)`:
4. `boolean markSupported​()`:
5. `int read​(byte[] b)`: 从输入流中读取一些字节数，放入 b 。 返回读取到的有效字节个数，没有读取到返回-1，每次读取的字节个数取决于b的长度，一般定义为1024的整数倍，b起缓冲作用。

```java
 public static void main(String[] args) throws IOException {
        FileInputStream fis = new FileInputStream("demo2.txt");
        int len = 0;
        byte [] bytes = new byte[1024];
        while((len = fis.read(bytes)) != -1){
            System.out.println(new String(bytes, 0, len));
        }
        fis.close()
    }
```
6. `int read​(byte[] b, int off, int len)`:从输入流从off开始读取最多 len个字节的数据到字节数组。 
7. `byte[] readAllBytes​()`: 从输入流读取所有剩余字节。  
8. `int readNBytes​(byte[] b, int off, int len)`: 将所请求的字节数从输入流读入给定的字节数组。  
9. `void reset​()`: 将此流重新定位到最后在此输入流上调用 mark方法时的位置。  
10. `long skip​(long n)`: 跳过并丢弃来自此输入流的 n字节的数据。  
11. `long transferTo​(OutputStream out)`: 从该输入流中读取所有字节，并按读取的顺序将字节写入给定的输出流 



### 5.1 FileInputStream

#### 5.1.1 常用构造方法

`FileInputStream​(File file)`和`FileInputStream​(String name)`: 创建一个文件字节输入流对象，并指向file

#### 5.1.2 成员方法

## 6. 字节输入流

为什么

## 7. 字节输出流

