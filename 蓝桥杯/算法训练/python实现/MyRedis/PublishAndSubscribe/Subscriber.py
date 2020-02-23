from MyRedis.PublishAndSubscribe.Channel import Channel
from MyRedis.redis_pipeline import redis_connection


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
    client = redis_connection("39.106.168.39", 8100, "redis19990805")
    cctv1 = Channel("CCTV1")
    Subscriber(client).subscribe(cctv1)
