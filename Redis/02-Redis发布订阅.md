# Redis 发布订阅

Redis 发布订阅可以用在像消息通知，群聊，定向推送，参数刷新加载等业务场景

<!-- more -->

发布订阅模型有三个角色：

1. 发布者（Publisher）
2. 订阅者(Subscriber)
3. 频道(channel)

每个订阅者可以订阅多个频道，发布者可以在某个频道里发布消息，订阅者会接受到自己订阅频道里发布的消息。

## 相关命令（[参考](https://chenxiao.blog.csdn.net/article/details/104195908)）

```redis
publish channel message         发布消息
subscribe [channel]             订阅频道
unsubscribe [channel]           取消订阅
psubscribe [pattern...]         订阅指定模式的频道
punsubscribe [pattern...]       退订指定模式的频道
pubsub channels                 列出至少有一个订阅者的频道
pubsub numsub [channel...]      列表给定频道的订阅者数量
pubsub numpat                   列表被订阅模式的数量 
```

在终端使用示例

```shell
# 在 终端1 订阅cctv1
127.0.0.1:8100> subscribe cctv1
Reading messages... (press Ctrl-C to quit)
1) "subscribe"
2) "cctv1"
3) (integer) 1
```

```shell
# 在 终端2 向cctv1 发布消息
127.0.0.1:8100> publish cctv1 "this is cctv1"
(integer) 1
```

```shell
# 终端1 接受到终端2发的消息
127.0.0.1:8100> subscribe cctv1
Reading messages... (press Ctrl-C to quit)
1) "subscribe"
2) "cctv1"
3) (integer) 1
1) "message"
2) "cctv1"
3) "this is cctv1"
```

## python 实现

```python
from PublishAndSubscribe.Channel import Channel
from PublishAndSubscribe.RedisTool import RedisTool


class Subscriber:
    def __init__(self, conn):
        self._conn = conn

    def subscribe(self, channel: Channel):
        # 获取发布/订阅对象
        pub = self._conn.pubsub()
        # 选择要订阅的频道
        pub.subscribe(channel.name)
        while True:
            # 接收消息
            msg = pub.parse_response()
            print(msg)


if __name__ == '__main__':
    client = RedisTool.redis_connection("0.0.0.0", 8100, "password")
    cctv1 = Channel("CCTV1")
    Subscriber(client).subscribe(cctv1)

```

```python
from PublishAndSubscribe.Channel import Channel
from PublishAndSubscribe.RedisTool import RedisTool


class Publisher:
    def __init__(self, conn):
        self._conn = conn

    def publish(self, channel: Channel, mess: str):
        # 向特定频道发布消息
        self._conn.publish(channel.name, mess)


if __name__ == '__main__':
    cctv1 = Channel("CCTV1")
    client = RedisTool.redis_connection("0.0.0.0", 8100, "password")
    publisher = Publisher(client)
    while True:
        publisher.publish(cctv1, input("请输入要发送的消息："))

```

```python
class Channel:
    def __init__(self, name: str):
        self.name = name
```

```python
import redis


class RedisTool:
    @staticmethod
    def redis_connection(address: str, port: int, password: str):
        """
        用来连接Redis
        Args:
            address: Redis 服务端IP地址
            port: [int] Redis 服务端口
            password: Redis client 登录凭证
        Return:
            type[Redis]: 返回一个redis对象
        """
        return redis.StrictRedis(address, port, password=password)
```

* 为了简便在订阅者和发布者两处都实例化了一个“CCTV1”的频道，虽然用起来不会有什么问题（Redis中简单的通过字符串区分频道），但在实际中这应该是同一个对象。
