# Redis主从复制

为了避免单点Redis服务器故障，准备多台服务器，互相连通，将数据复制多个副本保存在不同的服务器上，连接在一起，并保证数据是同步的，即使有其中一台服务器宕机，其他服务器依然可以继续提供服务，实现Redis的**高可用**，同时实现数据**冗余备份**。

<!-- more -->

互联网“三高”架构

* 高并发
* 高性能
* 高可用：可用性目标99.999%，即每年服务器宕机时长低于315秒



单机Redis的风险和问题

* 机器故障（硬盘故障，系统崩溃）造成数据丢失
* 容量瓶颈：

## 主从复制

为了解决单机Redis的这些问题，提出主从复制的概念，首先有一个master负责写，然后master中的数据及时有效的复制到slave中，slave只负责读。这是一个一对多的结构；将master的数据复制到slave的过程就叫“主从复制”

![image-20200225084515491](image/Untitled/image-20200225084515491.png)

> * master 主节点，提供数据方
>   * 与master连接的客户端叫主客户端
> * slave 从节点， 接收数据方
>   * 与slave连接的客户端叫从客户端

> ## 高可用集群
>
> 1. 如果slave突然宕机，那其他的slave就可以替代
>
> 2. 如果master宕机，就会从slave中选举出一个master
>
> 3. 如果master压力过大，可以在某个slave下追加slave，当前slave就可以作为下一层slave的master
>
>    ![image-20200225093015054](image/Untitled/image-20200225093015054.png)
>
> 4. 为了提高master的可用性，可以使用哨兵让多台服务器做master
>
>    ![image-20200225093141396](image/Untitled/image-20200225093141396.png)
>
>    

主从复制的作用

* 实现读写分离：提高服务器读写能力
* 负载均衡：slave分担master的负载
* 故障恢复：master出故障时，会选举出新master
* 数据冗余：数据热备份
* 高可用的基础：基于主从复制，构建哨兵模式与集群，实现Redis高可用方案

## 主从复制的工作流程

### 1. 建立连接阶段

建立slave到master的连接，使master能够识别slave，并保存slave的端口号

* slave向master发送 `slaveof masierIP masterPort`指令，master接受到指令后会给slave一个响应，说明要连接的`masterIP` 和 `masterPort`是正确的，然后slave保存master的`IP`和`port`,建立一个master和slave的socket，slave会周期性的`ping`master，如果master在线，就会对slave的ping响应（`pong`）,如果master设有密码，slave和master还需要一个验证授权的过程，最后，slave向master发送`replconf listening-port <port>`master保存slave端口
* 大致流程
  1. slave 向 master 发送 `slaveof`指令
  2. master 响应指令
  3. slave 保存 master IP 和 port
  4. 建立socket
  5. 周期性ping和pong
  6. 认证与授权
  7. master保存slave的port

具体命令：

* 方式一：客户端发送指令

  ```powershell
  slaveof <masterip> <masterport>
  ```

* 方式二：启动服务器时设置参数

  ```
  ./redis-server --slaveof <masterip> <masterport>
  ```

* 方式三：使用配置文件

  ```conf
  slaveof <masterip> <masterport>
  ```

master 有密码的情况：

* 怎么让master有密码

  ```conf
  # master配置文件中配置
  requirepass <password>
  ```

* slave如果使用客户端发送命令的方式连接master

  ```
  auth <password>
  ```

* slave通过配置文件连接master

  ```
  masterauth <password>
  ```

### 2. 数据同步阶段

步骤：

1. **请求同步数据**

  数据同步阶段是由slave发起的，slave向master发送`psync2`请求同步数据

2. **master创建RDB文件**

  * 数据的同步还是依靠RDB持久化来实现的，master接受到slave的同步请求后，执行`gbsave`生成RDB文件。
  * 由于master需要腾出精力来响应slave的同步请求，为了保证不丢失客户端的请求，会创建一个复制缓冲区，在master响应slave期间，master的客户端请求会被保存到复制缓冲区

3. **master将RDB文件通过socket传给slave**

4. **slave根据RDB文件恢复数据**

  为了保证数据一致，slave接收到master的RDB文件后，会清空自己的所有数据，然后根据RDB文件恢复数据。

5. **请求部分同步数据**

  slave恢复结束后，会发送命令告知master，但这时master命令缓冲区中的数据还没有同步到slave，所以等slave第一次恢复完后，master会把复制缓冲区中的命令以AOF的方式给slave

6. **恢复部分同步数据**

  slave接受到master发来的AOF后，先会执行`bgrewriteaof`来进行一次重写，以加快恢复过程，回复完成后，master和slave的数据就同步了，数据同步阶段结束

#### 全量复制和部分复制

上面的步骤中，前四步所进行的就是全量复制，在这个阶段，使用的是RDB，同步的是master中之前所有的数据。

第五步和第六步所执行的就是**部分复制**，这个阶段使用的是AOF，同步的内容是master命令缓冲区中的命令  

#### 注意

1. 数据同步应该避开流量高峰期，避免造成master阻塞

2. 复制缓冲区设定应该合理，过小会导致数据溢出，如果进行部分复制时发现数据已经丢失，就必须重新进行全量复制，导致slave陷入死循环，复制缓冲区大小默认1MB,可以通过下面的配置修改

   ```
   repl-backlog-size 1mb
   ```

3. master单机占用内存不应该过大，建议使用50%~70%的内存，留下30%~50%用于执行bgsave命令和创建复制缓冲区

4. 为了避免slave在数据同步期间服务器响应阻塞或数据不同步，建议关闭此期间的对外服务

   ```
   slave-servr-stale-data yes|no
   ```

5. 数据同步阶段，master也会给slave发送消息，这时master可以理解为slave的一个客户端，如ping

6. 多个slave同时与master进行数据同步，会导致master发送的RDB或AOF文件过多，对带宽造成巨大冲击，如果master带宽不足，数据同步需要适量错峰

7. 当slave过多时，建议调整拓扑结构，如将一对多结构调整为树状结构，让中间节点分担根master的负载，但这样会导致顶层master和底层的slave间数据延时增加，数据一致性变差，应综合考虑业务对数据一致性的要求和服务器实际能力谨慎选择。



### 3.命令传播阶段（master把自己的数据与slave反复同步）

