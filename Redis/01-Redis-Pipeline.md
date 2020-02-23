# Redis-Pipeline

正常的Redis 命令的生命周期是 Client 给 Server 发一条命令，Server 执行后把结果反馈给 Client,但这个过程中， Client 和 Server 之间的通信会花费大量时间，pipeline 的思路就是每一次 Client 和 Server 通信不再是一次发一条命令（/结果）而是把一批命令打包传输给 Server,然后Server把这些命令按顺序执行的结果反馈给 Client

<!--more -->

pipeline 并不是原子命令，在执行时，他是以子命令的形式穿插在Redis正在执行的其他命令之间的

通过python测试，效果非常明显

```python
import redis
# run_time 是我自己写的一个装饰器，用来返回被装饰对象的执行时间
from my_python_package.Modifys import run_time


def redis_connection(address: str, port: int, password: str):
    return redis.StrictRedis(address, port, password=password)


@run_time
def execute_multiple_commands_without_pipes(client):
    for i in range(1000):
        client.set(f"string{i}", i)


@run_time
def execute_multiple_commands_with_pipes(client):
    pipeline = client.pipeline()
    for i in range(1000):
        pipeline.set(f"string with pipes{i}", i)
    pipeline.execute()


if __name__ == '__main__':
    client = redis_connection("0.0.0.0", 8100, "password")
    # execute_multiple_commands_without_pipes(client)  # execute_multiple_commands_without_pipes runs at:35.10040497779846 s
    execute_multiple_commands_with_pipes(client)  # execute_multiple_commands_with_pipes runs at:0.17360401153564453 s

```

同样是执行1000次写入，使用pipeline效率提高了两百多倍。多出来的这些时间就是节省的网络传输的时间，