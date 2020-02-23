from MyRedis.RedisTool import RedisTool


class RedisHLL:
    def __init__(self):
        self._conn = RedisTool.redis_connection("39.106.168.39", 8100, "redis19990805")

    def hll_test(self):
        self._conn.pfadd('test', "junebao", "python", "redis", "hyperloglog", "java")
        count = self._conn.pfcount("test")
        print(count)


if __name__ == '__main__':
    RedisHLL().hll_test()