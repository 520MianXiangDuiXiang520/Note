# 初识Shell

* Shell 是一个用 C 语言编写的程序，它是用户使用 Linux 的桥梁。Shell 既是一种命令语言，又是一种程序设计语言。

* Shell 是指一种应用程序，这个应用程序提供了一个界面，用户通过这个界面访问操作系统内核的服务。

## 第一个Shell程序

* 听说初学一门语言首先输出 “Hello World”日后出Bug的概率会减少，所以....

```shell

#!bin/bash
echo "hello world"

```

运行后：

```txt

junbao@ubuntu:~/Desktop/Shell$ sh shell_01.sh 
hello world

```

* `#!`: 告诉系统其后路径所指定的程序即是解释此脚本文件的 Shell 程序,也可以是`#!bin/bash`,因为我们并不区分Bourne Shell 和 Bourne Again Shell