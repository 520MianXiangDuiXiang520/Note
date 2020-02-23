from MyRedis.PublishAndSubscribe.Channel import Channel
from MyRedis.RedisTool import RedisTool


class Publisher:
    def __init__(self, conn):
        self._conn = conn

    def publish(self, channel: Channel, mess: str):
        # 向特定频道发布消息
        self._conn.publish(channel.name, mess)


if __name__ == '__main__':
    cctv1 = Channel("CCTV1")
    client = RedisTool.redis_connection("39.106.168.39", 8100, "redis19990805")
    publisher = Publisher(client)
    while True:
        publisher.publish(cctv1, input("请输入要发送的消息："))
