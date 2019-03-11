# 创建用户

用户管理所有命令必须使用 sudo

|命令|作用|
|----|----|
|useradd -m -g 组 用户名|新建用户|
|passwd 用户名|设置用户密码|
|userdel -r 用户名|删除用户|

* -m 自动创建家目录，并且设置相应权限
* -g 增加组，如果不指定，会自动创建一个与用户同名的组
* 创建用户必须指定密码，否则新用户无法登录。
* -r 自动删除用户家目录

```
junbao111@ubuntu:~/Desktop$ sudo useradd -m -g python lenovo
[sudo] junbao111 的密码： 
junbao111@ubuntu:~/Desktop$ ls /etc/passwd
/etc/passwd
junbao111@ubuntu:~/Desktop$ cat /etc/passwd
root:x:0:0:root:/root:/bin/bash
···
lenovo:x:1001:1001::/home/lenovo:/bin/sh
junbao111@ubuntu:~/Desktop$ sudo passwd lenovo
输入新的 UNIX 密码： 
重新输入新的 UNIX 密码： 
passwd：已成功更新密码

junbao111@ubuntu:~/Desktop$ ls -lh /home
总用量 8.0K
drwxr-xr-x 21 junbao111 junbao111 4.0K 3月  10 21:40 junbao111
drwxr-xr-x  2 lenovo    python    4.0K 3月  11 20:34 lenovo


```
## 查看用户信息

### 1.
```
id [username]
```


用户代号：/etc/passwd
组代号：/etc/group

```

junbao111@ubuntu:~/Desktop$ id lenovo
uid=1001(lenovo) gid=1001(python) 组=1001(python)


junbao111@ubuntu:~/Desktop$ cat /etc/passwd | grep junbao111
junbao111:x:1000:1000:面向对象,,,:/home/junbao111:/bin/bash

junbao111@ubuntu:~/Desktop$ cat -n /etc/passwd | grep lenovo
    43	lenovo:x:1001:1001::/home/lenovo:/bin/sh
junbao111@ubuntu:~/Desktop$ 

junbao111@ubuntu:~/Desktop$ cat -n /etc/group |grep junbao111
     5	adm:x:4:syslog,junbao111
    18	cdrom:x:24:junbao111   #允许访问光驱
    21	sudo:x:27:junbao111    # 允许使用sudo
    23	dip:x:30:junbao111
    35	plugdev:x:46:junbao111
    55	lpadmin:x:116:junbao111
    65	junbao111:x:1000:
    66	sambashare:x:126:junbao111

```
通过在passwd文件中查找，找到以上用户信息，passwd文件中以`:`分割组信息，信息内容如下：
* junbao111 : 用户名
* x：密码
* 1000（第一个）：用户代号
* 1000（第二个）：组代号
* 面向对象,,,：全名，未设置就使用用户名
* /home/junbao111：家目录
* /bin/bash:登录使用的Shell,就是登录之后使用的终端命令，默认bash

### 2.
who和whoami
* who: 显示所有用户
* whoami:询问系统我是谁

```
junbao111@ubuntu:~/Desktop$ who
junbao111 :0           2019-03-09 18:36 (:0)
junbao111 pts/1        2019-03-10 20:04 (192.168.47.1)

junbao111@ubuntu:~/Desktop$ who
junbao111 :0           2019-03-09 18:36 (:0)
junbao111 pts/1        2019-03-10 20:04 (192.168.47.1)
lenovo   pts/2        2019-03-11 21:06 (192.168.47.1)
```
上一个是创建lenovo后未登陆过的，下一个是用Xshell远程登录lenovo用户后的，括号中0代表在本机登录，否则代表登录地IP地址

### 3. usermod
* 主组，新建用户时指定的，在etc/passwd第四列
* 附加组：在etc/group最后一列，用于指定用户附加权限

为用户添加附加组——usermod

1. 格式：

```

# 修改用户主组
usermod -g 组 用户名

# 修改用户附加组
usermod -G 组 用户名

# 修改用户登录shell
usermod -s /bin/bash

```
2. 例：
在查看junbao111用户信息时，附加组有很多
```
junbao111@ubuntu:~/Desktop$ id
uid=1000(junbao111) gid=1000(junbao111) 组=1000(junbao111),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),116(lpadmin),126(sambashare)

```
在group中检索
```
junbao111@ubuntu:~/Desktop$ cat -n /etc/group |grep junbao111
     5	adm:x:4:syslog,junbao111
    18	cdrom:x:24:junbao111
    21	sudo:x:27:junbao111
    23	dip:x:30:junbao111
    35	plugdev:x:46:junbao111
    55	lpadmin:x:116:junbao111
    65	junbao111:x:1000:
    66	sambashare:x:126:junbao111

```
注意，前面的sudo等是组名，后面的junbao111是用户名，意思是这个组里有这个用户，比如sudo中只有一个用户，那lenovo应该不能使用sudo命令，在Xshell中实验一下
```

$ pwd
/home/lenovo
$ sudo useradd -m -d -g python zhangsan
[sudo] password for lenovo: 
lenovo is not in the sudoers file.  This incident will be reported.

```
错误提示lenovo用户不再sudoers中，我们可以使用usermod修改用户附加组
```
junbao111@ubuntu:~/Desktop$ usermod -G sudo lenovo
usermod: Permission denied.
usermod：无法锁定 /etc/passwd，请稍后再试。
junbao111@ubuntu:~/Desktop$ sudo usermod -G sudo lenovo
[sudo] junbao111 的密码： 
junbao111@ubuntu:~/Desktop$ 

```
记得加sudo  

查看group文件
```
junbao111@ubuntu:~/Desktop$ cat /etc/group |grep sudo
sudo:x:27:junbao111,lenovo

```
sudo中的用户添加了lenovo,要执行权限，需要重新登录，在Xshell中重新登录后重新创建用户
```
$ sudo useradd -m -g python zhangsan
[sudo] password for lenovo: 
Sorry, try again.
[sudo] password for lenovo: 
$ passwd zhangsan
passwd: You may not view or modify password information for zhangsan.
$ sudo passwd zhangsan
Enter new UNIX password: 
Retype new UNIX password: 
passwd: password updated successfully
$ 

```
可以了...

##### 设置Shell
在乌班图中我们的终端命令是这样的
```
junbao111@ubuntu:~/Desktop$ ·····
```
但在Xshell中lenovo的终端命令则是这样的
```
$ .....
```
并且在按删除，上下左右键等时是这样的
```
$ ^[[A^[[B^[[D^[[C^H

```
这不是Xshell这个软件的原因,,,把用户切换回junbao111时显示和乌班图是一样的，这是由于两个用户所用的shell不同，就是passwd最后的那个，默认用户使用dash,应为dash更方便，但dash在window下显示会出现上面的情况，我们可以把shell改成junbao111用的bash，这个软件在bin目录下
```
$ sudo usermod -s /bin/bash lenovo
[sudo] password for lenovo: 
$ 

# 重新连接后

lenovo@ubuntu:~$ pwd
/home/lenovo
lenovo@ubuntu:~$ 

```

### 4. which，查看执行命令所在位置
```
junbao111@ubuntu:~/Desktop$ which ls
/bin/ls
junbao111@ubuntu:~/Desktop$ which passwd
/usr/bin/passwd
junbao111@ubuntu:~/Desktop$ 

```
* usr目录：
  * 在Linux中，大部分可执行文件都保存在`/bin`,`/sbin`,`/usr/bin`,`/usr/sbin`中
  * `/bin`是二进制执行文件目录，用于具体应用
  * `/sbin`是系统管理员专用二进制执行文件目录，用于系统管理 
  * `usr/bin`涉及后期安装的软件
  * `usr/sbin`超级用户一些管理程序

```
junbao111@ubuntu:~/Desktop$ ls -lh /bin
总用量 13M
-rwxr-xr-x 1 root root 1.1M 4月   5  2018 bash
-rwxr-xr-x 1 root root 732K 8月  29  2018 brltty
# 对root可读可写可执行，对普通用户刻度可执行

junbao111@ubuntu:~/Desktop$ ls -lh /sbin
总用量 12M
-rwxr-xr-x 1 root root     112 3月   2  2018 acpi_available
-rwx r-x r-x 1 root root     56K 10月 16 04:29 agetty


junbao111@ubuntu:~/Desktop$ ls -lh /usr/bin
总用量 156M
-rwxr-xr-x 1 root root     51K 1月  18  2018 '['
-rwxr-xr-x 1 root root      96 11月 12 22:31  2to3-2.7

junbao111@ubuntu:~/Desktop$ ls -lh /usr/sbin
总用量 16M
-rwxr-xr-x 1 root root  2.9K 9月  28 02:20 aa-remove-unknown
-rwxr-xr-x 1 root root  8.5K 9月  28 02:20 aa-status


```

### 5.切换用户

|命令|作用|说明|
|-|-|-|
|`su [-用户名]`|切换用户，并切换目录|不加减号不切换目录，不加用户名直接切换到root|
|exit|退出|


```
junbao111@ubuntu:~/Desktop$ whoami
junbao111
junbao111@ubuntu:~/Desktop$ su - zhangsan
密码： 
$ whoani
-su: 1: whoani: not found
$ pwd
/home/zhangsan
$ exit
junbao111@ubuntu:~/Desktop$ whoami
junbao111
junbao111@ubuntu:~/Desktop$ pwd
/home/junbao111/Desktop
junbao111@ubuntu:~/Desktop$ 


# 不加减号
junbao111@ubuntu:~/Desktop$ su lenovo
密码： 
lenovo@ubuntu:/home/junbao111/Desktop$ pwd
/home/junbao111/Desktop
lenovo@ubuntu:/home/junbao111/Desktop$ 

# 不加用户名

junbao111@ubuntu:~/Desktop$ sudo passwd
[sudo] junbao111 的密码： 
输入新的 UNIX 密码： 
重新输入新的 UNIX 密码： 
passwd：已成功更新密码
junbao111@ubuntu:~/Desktop$ su
密码： 
root@ubuntu:/home/junbao111/Desktop# whoami
root
root@ubuntu:/home/junbao111/Desktop# 


```
root的密码是每次开机随机更新的，可以使用`sudo passwd`修改，**不推荐使用root登录**