# MySQL在Docker下的安装使用

1. 安装：

   ```
   docker pull mysql
   ```

2. 启动容器

   ```
   docker run -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 -v /dataVolume/mysql/data:/var/lib/mysql -v /dataVolume/mysql/logs:/var/log/mysql  mysql
   ```

3. 容器内启动MySQL服务

   ```
   1. 以终端方式重新进入容器
   docker exec -it 容器名/容器ID /bin/bash
   
   2. 交互方式进入mysql
   mysql -uroot -p
   
   3. 允许远程连接root账户
   USE mysql;
   UPDATE USER SET host='%' WHERE user='root';
   
   3. 修改root用户密码
   ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'newpassword';
   
   ```

4. 如果是云服务器，需要修改安全组策略，把MySQL的端口释放出来

5. 使用Navicat连接mysql