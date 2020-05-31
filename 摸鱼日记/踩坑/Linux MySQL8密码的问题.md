## Linux 安装MySQL

```shell
sudo apt install mysql-server
sudo apt install mysql-client
```

## 修改（设定）初始密码

1. 修改`/etc/mysql/mysql.conf.d/mysqld.cnf`文件，在`[mysqld]`中加入`skip-grant-tables`允许无密码登录。
2. `mysql -u root -p`
3. `use mysql`
4. `select user, plugin from user;`会发现root的plugin是`auth_socket`
5. `ALTER user 'root'@'localhost' IDENTIFIED WITH caching_sha2_password BY 'xxxxx';`
6. 刷新`flush privileges`
7. 退出MySQL命令行
8. 重启MySQL服务`service mysql restart`

