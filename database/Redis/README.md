# Redis

## Redis是什么，为什么用

Redis 是一个开源免费的，遵循BSD协议，是一个高性能（NOSQL）的 key-value数据库， 由C语言编写。提供多种语言的API，

* SQL: 关系型数据库
* NOSQL： 非关系型数据库（为了解决大规模数据集合多种数据种类带来的挑战，尤其是大数据应用难题）

### NoSQL

NoSQL数据库的四大分类

1. 键值型（Key-Value）: Redis, Oracle SDB
2. 列存储数据库：应对分布式村纯的海量数据，键任然存在，但他们的特点是指向了多个列，这些列是由列家族来安排的，如HBase
3. 文档型数据库：MongoDB
4. 图形数据库：Neo4J

NoSQL 的应用场景：

1. 数据模型简单
2. 需要更强大灵活的IT系统时
3. 对数据库性能要求较高的环境
4. 不需要高度的数据一致性
5. 对于给定的Key,能比较容易映射复杂值的环境

Redis的优势

1. 支持数据持久化
2. 支持多种数据结构存储（list, set, zsit,hash）
3. 支持数据备份，集群等高可用功能

Redis的特点

1. 性能极高 读写速度110000次/s，81000次/s
2. 丰富的数据类型 String, List, Hash, Set, Ordered Set等
3. 原子性， 所有操作都是原子性的。
4. 功能丰富

## Redis安装及配置文件

### Redis安装

Redis 基于C语言，安装之前应该确保安装了gcc

```txt
sudo apt install gcc
```

从[官网下载](https://redis.io/download)安装压缩包

```shell
#解压
tar -zxaf redis-5.0.7.tar.gz
# 编译安装
cd redis-5.0.7/
make PREFIX=/usr/local/redis install
```

在`usr/local`目录下就会怎加`redis/bin`目录

### Redis 配置文件

位置： 是解压目录下的`redis.conf`,把它复制到redis安装目录下

```txt
cp redis.conf /usr/local/redis
```

常用配置：

```conf
# 设置Redis是否以守护进程运行,设置为yes以守护进程运行
daemonize no
# 当Redis以守护进程方式运行时，会把pid写道指定文件，通过修改pidfile修改
pidfile /var/run/redis_6379.pid
# 监听的端口号 默认6379
port 6379
# 绑定主机地址
bind 127.0.0.1
# 设置客户端闲置多长时间后连接关闭,0表示关闭该功能
timeout 300
# 指定日志记录级别，支持debug,verbose,notice,warning, 默认verbose
loglevel verbose
# 日志记录方式， 默认为标准输出
logfile stdout
# 设置数据库数量
databases 16
# 指定多长时间内，有多少次更新操作，就将数据同步到数据文件，可以多个条件配合，只要满足其中一个就会持久化一次
# save 900 1     : 每900s有一个修改就持久化一次
# save 300 10    : 每300s有10个更改
# save 60 10000  : 每60s有10000个更改
save  <seconds> <changes>
# 设置持久化时本地数据库文件名
dbfilename dump.rdb
# 指定本地数据库文件存放目录
dir ./
# 设置当主机为 slave 服务时， 设置 master 服务的IP及端口，在 Redis 启动时，他会自动从 master 同步数据
slaveof <masterip> <masterport>
# 当 master 设置了密码保护时，  slave 服务连接 master 时的密码
masterauth <master-password>
# redis 密码， 默认关闭
requirepass foobared
# 设置最大连接数（并发线程）, 默认无限制
maxclients 10000, 建议1G不要超过256MB-512MB 
# 指定最大内存限制
maxmemory <bytes>
```

### 启动，关闭命令

启动服务端

```shell
# 以redis.conf里设置的配置启动redis服务端
./redis-server ./redis.conf
```

启动客户端

```shell
# IP 端口默认未 127.0.0.1:6379
./redis-cli [-h IP地址][ -p 端口][ -a 密码]
```

正常关闭

```shell
# 客户端输入
shutdown
```

### 常用命令

1. `del key`: 删除key, 返回删除的key的个数
2. `DUMP key`: 序列化给定的key，返回序列化后的结果
3. `EXISTS key`: 检查key是否存在，存在返回1，不存在返回0
4. `EXPIRE key seconds`:给key设置剩余生存时间，以s为单位
5. `PEXPIRE key seconds`:给key设置剩余生存时间，以ms为单位
6. `TTL key`: 返回key剩余时间，-1代表永久， -2代表无效
7. `PTTL key`: 返回key剩余时间，ms为单位
8. `PERSIST key`: 移除 key 过期时间，设为永久有效
9. `KEYS pattern`: 以通配符方式查询满足的所有key， `*`表示全部， `?`表示任意字符
10. `RANDOM KEY`: 从当前数据库中随机返回一个 key
11. `RENAME key newkey`: 修改Key的名称
12. `MOVE key db`: 把当前数据库的key移到数据库db中 
13. `SELECT db`: 切换数据库
14. `TYPE key`: 返回key的类型

### Key的命名规范

1. 不要太长，尽量不要超过1024字节
2. 也不要太短，否则不容易体现用途，降低可读性
3. 使用统一的命名规范，如`user:123:password`

## Redis常用数据类型及应用场景

### String

String 是 redis 最基本的数据类型，一个key对应一个value; 一个键最大能储存512MB 
string 是二进制安全的，它可以包含任何数据，如jpg图片或序列化对象  

> #### 二进制安全
> 二进制安全是指在传输数据时，能够保证二进制数据的安全性，也就是保证二进制数据不被篡改，编译，如果被攻击，也能够及时检测出来
>
> 二进制安全的特点
>  1. 编码解码发生在客户端，执行效率高
>  2. 不需要频繁编解码，不会出现乱码

#### 常用命令

1. `SET key_name value`: 赋值，用于给key设置储存值，如果值已经存在，就会覆盖旧值，且无视类型
2. `SETNX key value`: 只有在 key 不存在时设置 key 的值， 如果存在失效（解决分布式锁的方案之一）
3. `MSET key value [key value ...]`: 同时设置一个或多个key
4. `GET key`: 获取指定key的值，如果key不存在， 返回nil,如果key存储的值的类型不是一个string类型，会返回一个错误
5. `CETRANCE key start end`: 用于获取存储在 key 中字符串的子字符串，字符串的截取范围由 start 和 end 两个偏移量决定
6. `GETBIT key offset`: 对 key 所储存的字符串值，获取指定偏移量上的位（bit）
7. `MGET key1 [key2...]`:获取多个key的值
8. `GETSET key value`: 先读再写，返回旧值
9. `STRLEN key`: 返回key所储存的字符串的长度
10. `INCR key`: 将key中储存的数字值增1，如果key不存在，那么key的值会被先初始化为0，再执行 INCR 操作
11. `INCRBY key 增量`：ey中储存的数字值增加指定增量
12. `DECR key`: 自减
13. `DECRBY key 减量`: 自减指定量
14. `APPEND key value`: 把value追加到指定key的末尾，如果key不存在，为其赋值

#### 应用场景

1. 保存单个字符串或JSON字符串数据
2. 应为是二进制安全的，所以可以用来保存图片等内容
3. 用作计数器：INCR等指令具有原子性，可以实现原子计数的效果，也不会存在线程问题

### Hash

可以把Hash数据类型类比面向对象中的对象（JavaBean）

#### 常用命令

1. `HSET key field value`: 为指定的key设置 field-value
2. `HMSET key field value [field1 value1 ...]`: 为key设定多个field-value
3. `HGET key field`:获取指定key中的field字段
4. `HMGET key field[ field1...]`: 获取key中的多个field
5. `HGETALL key`: 获取key中所有field和value
6. `HKEYS key`: 获取key中所有field
7. `HLEN key`: 获取key对应字段的数量
8. `HDEL key field`: 删除指定field
9. `HSETNX key field value`
10. `HINCRBY key field 增量`
11. `HINCRBYFLOAT key field 增量`： 为key对应的指定浮点field加上增量
12. `HEXISTS key field`: 判断key对应的field是否存在

#### 应用场景

1. 常用于存储一个对象

### List

Redis 列表是简单的字符串列表，按照插入顺序排序，你可以添加一个元素到列表的头部或尾部，一个列表中最多可以包含`(2^32)-1`个元素

#### 常用命令

##### 赋值语法

`LPUSH key value1 [value2...]`: 从左侧添加一个或多个值

`RPUSH key value1[ value2...]`: 从右侧添加

`LPUSHX key value`: 将一个值插入到已存在的列表头部，如果列表不存在，操作无效

`RPUSHX key value`: 将一个值插入到已存在的列表尾部，如果列表不存在，操作无效

##### 取值语法

`LLEN key`: 获取列表长度

`LINDEX key index`: 通过索引获取列表中的元素

`LRANCE key start stop`: 获取列表中指定范围的元素（负数表示从后往前数）

##### 删除语法

`LPOP key`: 移除并获取列表的第一个元素（从左侧删除）

`RPOP key`: 移除并获取列表的最后一个元素（从右侧删除）

`BLPOP key1[ key2...] timeout`: 移除并获取列表第一个元素，如果列表没有元素会阻塞列表直到等待超时会发现可弹出元素为止。

`BRPOP key1[ key2...] timeout`: 移除并获取列表最后一个元素，如果列表没有元素会阻塞列表直到等待超时会发现可弹出元素为止。单位s

`LTRIM key start stop`: 只保留列表区间内的元素

##### 修改语法

`LSET key index value`: 通过索引修改元素值

`LINSERT key BEFORE|AFTER vorld value`: 将value插入到key中vorld的前面或后面

##### 其他命令

`RPOPLPUSH source destination`: 移除列表最后一个元素并将它添加到另一个列表并返回。

* `RPOPLPUSH a1 a2`: a1的最后一个元素移动到a2的最前面
* `RPOPLPUSH a1 a1`: 将最后的元素移动到最前面

#### 应用场景

1. 对数据量大的集合数据进行操作
  * 关注列表，粉丝列表，留言， 分页，热点新闻等
2. 任务队列
  * 用户下单流程

### Set（无序集合）

底层使用 intset 和hashtable 两种数据结构存储。

intset 内部是一个数组，而且存储数据时是由虚的，所以在查找数据时是通过二分查找来实现的。

#### 常用命令

##### 赋值语法

`SADD key member1[ member2...]`: 向集合中添加一个或多个元素

##### 取值语法

`SCARD key`: 获取集合成员数

`SMEMBERS key`: 返回集合中所有成员

`SISMEMBER key member`: 检查 member 是否是 key 的成员

`SRANDMEMBER key[count]`: 返回集合中一个或多个随机值

##### 删除语法

`SREM key member1[ member2]`: 移除一个或多个成员

`SPOP ket[count]`: 随机移除并返回集合中一个或多个成员

`SMOVE soure destination member`: 将member从source移动到destination

##### 运算语法

`SDIFF key1[ key2...]`: 返回所有集合的差集

`SDIFFSTORE dest key1[ key2...]`: 将差集保存到dest中

`SINTER key1[ key2...]`: 返回所有集合的交集

`SINTERSTORE dest key1[ key2...]`: 将交集保存到dest中

`SUNION key1[ key2...]`: 并集

`SUNIONSTORE dest key1[ key2...]`: 并集保存到dest中

#### 应用场景

* 两个集合数据需要进行计算时， 如共同关注，二度交友等
* 利用唯一性作唯一标识

### ZSET（有序集合）

#### 常用命令

`ZADD key score1 memeber1`

`ZCARD key` ：获取集合中的元素数量

`ZCOUNT key min max` 计算在有序集合中指定区间分数的成员数

`ZRANK key member`：返回有序集合指定成员的索引

`ZREVRANGE key start stop` ：返回有序集中指定区间内的成员，通过索引，分数从高到底

`ZREM key member [member …]` 移除有序集合中的一个或多个成员

`ZREMRANGEBYRANK key start stop` 移除有序集合中给定的排名区间的所有成员(第一名是0)(低到高排序）

`ZREMRANGEBYSCORE key min max` 移除有序集合中给定的分数区间的所有成员

#### 应用场景

排行榜，带权队列，存储成绩

## 其他功能

* 订阅发布
* 事务
* 数据淘汰策略
* 缓存与数据库
* 缓存穿透，缓存雪崩