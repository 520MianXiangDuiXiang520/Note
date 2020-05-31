# Linux（Ubuntu 19.10）下 Qt5 连接 MySQL

1. 安装好 MySQL 和 Qt

2. Qt 连接 MySQL 的代码

   ```c++
   QSqlDatabase d=QSqlDatabase::addDatabase("QMYSQL");//加载mysql驱动，这个字符串是固定的
   d.setHostName("127.0.0.1");
   d.setDatabaseName("mysql");        //数据库名称
   d.setPort(3306);                     //数据库端口，如果没有更改/etc/mysql/my.cnf就不用改
   d.setUserName("root");
   d.setPassword("123467");
   if(d.open())
       qDebug()<<"数据库连接成功";
   else
       qDebug()<<"数据库连接失败";
   ```

   运行后发现报错：

   ```txt
   QSqlDatabase: QMYSQL driver not loaded
   QSqlDatabase: available drivers: QSQLITE QODBC QODBC3 QPSQL QPSQL7
   ```

   原因是没有 MySQL驱动 或 MySQL 驱动版本不对，驱动放在`/home/junebao/Qt/5.14.2/gcc_64/plugins/sqldrivers`:

   有两个文件：

   1. `libqsqlmysql.so.debug`
   2. `libqsqlmysql.so`

   这两个文件不存在或版本与 Qt 版本不匹配都会导致上面的错误

## 解决 QMYSQL driver not loaded

官方文档：

![UTOOLS1590741069581.png](http://yanxuan.nosdn.127.net/dc124a7672424ccfcc9efe4ec81e881a.png)

1. 到`~/Qt/5.14.2/Src/qtbase/src/plugins/sqldrivers` 目录下 执行 `qmake -- MYSQL_PREFIX=/usr/local`

   * `~/Qt/5.14.2`是 Qt 的下载目录

   * `usr/local`是 MySQL 的安装目录
   * 如果出现`qtbase/src/plugins/sqldrivers/sqldrivers.pro:16: Unknown test function: qtConfig` 是因为默认链接的 `qmake`可能是 Qt4 的，可以使用 Qt5 qmake 的完整路径执行：**` ~/Qt/5.14.2/gcc_64/bin/qmake -- MYSQL_PREFIX=/usr/local`**

2. 执行 `make sub-mysql`

   * make 的过程中可能会缺依赖，缺啥下啥就好了

3. 执行完后在`~/Qt/5.14.2/Src/qtbase/plugins/sqldrivers`目录（和上面不是同一个目录）下会出现`libqsqlmysql.so.debug`和`libqsqlmysql.so`两个文件

   * 如果这一步没有生成那两个文件，回到第一步试着执行`~/Qt/Qt5.14.2/5.11.2/gcc_64/bin/qmake "INCLUDEPATH+=/usr/include/mysql" "LIBS+=-L/usr/lib/x86_64-linux-gnu/ -lmysqlclient" mysql.pro`

4. 把他们复制到`/home/junebao/Qt/5.14.2/gcc_64/plugins/sqldrivers`下面就好了

## 环境

* OS：Ubuntu 19.10.1(64位)
* Qt: 5.14.2
* MySQL: 8.0.20 

