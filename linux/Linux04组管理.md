# 组管理

* 所有创建删除组的操作都要使用超级用户权限

|操作|命令|
|----|----|
|添加组|groupadd groupname|
|删除组|groupdel groupname|
|确认组信息|cat /etc/group|
|修改文件/目录所属组|chgrp -R grpname 文件/目录名|

```
junbao111@ubuntu:~/Desktop$ mkdir Python
junbao111@ubuntu:~/Desktop$ sudo groupadd python
[sudo] junbao111 的密码： 
junbao111@ubuntu:~/Desktop$ cd /etc/group
bash: cd: /etc/group: 不是目录
junbao111@ubuntu:~/Desktop$ cat /etc/group
root:x:0:
·
·
·
python:x:1001:
junbao111@ubuntu:~/Desktop$ chgrp -R python Python/
chgrp: 正在更改'Python/' 的所属组: 不允许的操作
junbao111@ubuntu:~/Desktop$ sudo chgrp -R python Python/
junbao111@ubuntu:~/Desktop$ ls
Python
junbao111@ubuntu:~/Desktop$ ls -l
总用量 4
drwxr-xr-x 2 junbao111 python 4096 3月  11 20:07 Python
junbao111@ubuntu:~/Desktop$ 

```