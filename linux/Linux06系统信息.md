# 时间日期

|序号|命令|作用|
|----|----|----|
|01|dete|查看当前系统时间|
|02|cal [-y]|查看本月日历,加-y可查看一年的|

```
junbao111@ubuntu:~$ date
2019年 03月 12日 星期二 14:34:45 CST
junbao111@ubuntu:~$ cal
      三月 2019         
日 一 二 三 四 五 六  
                1  2  
 3  4  5  6  7  8  9  
10 11 12 13 14 15 16  
17 18 19 20 21 22 23  
24 25 26 27 28 29 30  
31                    
junbao111@ubuntu:~$ 


```
# 磁盘信息

|序号|命令|作用|
|----|---|----|
|01|df -h|显示磁盘剩余空间|
|02|`du -h[目录名]`|显示目录下的文件夹大小|

```
junbao111@ubuntu:~$ df -h
文件系统        容量  已用  可用 已用% 挂载点
udev            964M     0  964M    0% /dev
tmpfs           197M  1.8M  196M    1% /run
/dev/sda1        59G  8.7G   48G   16% /
tmpfs           985M     0  985M    0% /dev/shm
tmpfs           5.0M  4.0K  5.0M    1% /run/lock
tmpfs           985M     0  985M    0% /sys/fs/cgroup

······

junbao111@ubuntu:~$ 

junbao111@ubuntu:~/Desktop$ du -h Python/
4.0K	Python/
junbao111@ubuntu:~/Desktop$ 

```
# 进程信息

* 进程：当前正在进行的程序

|序号|命令|作用|
|----|---|----|
|01|ps aux|查看进程详细状况|
|02|top|动态显示运行中的进程并排序|
|03|`kill [-9] 进程代号`|终止指定代号进程|

* ps 不加任何参数会显示当前用户通过终端正在运行的进程
  * a：显示终端所有进程，包括其他用户进程
  * u：显示进程详细情况
  * x：显示没有控制终端的进程
* -9表示强行终止
* top 按q退出


```

junbao111@ubuntu:~/Desktop$ ps au
USER        PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND

junbao1+  16820  0.0  0.2  29836  5028 pts/0    Ss   14:34   0:00 bash
junbao1+  16930  0.0  0.2  29704  4524 pts/1    Ss+  15:04   0:00 bash
junbao1+  16938  0.0  0.1  46780  3464 pts/0    R+   15:04   0:00 ps au
junbao111@ubuntu:~/Desktop$ kill 16930

```