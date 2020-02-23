import redis
from my_python_package.Modifys import run_time


def redis_connection(address: str, port: int, password: str):
    return redis.StrictRedis(address, port, password=password)


@run_time
def execute_multiple_commands_without_pipes(client):
    # for i in range(1000):
        # client.set(f"string{i}", i)
    for i in range(1000):
        client.delete(f"string{i}")


@run_time
def execute_multiple_commands_with_pipes(client):
    pipeline = client.pipeline()
    # for i in range(1000):
    #     pipeline.set(f"string with pipes{i}", i)
    for i in range(1000):
        pipeline.delete(f"string with pipes{i}")
    pipeline.execute()


if __name__ == '__main__':
    client = redis_connection("39.106.168.39", 8100, "redis19990805")
    execute_multiple_commands_without_pipes(client)  # execute_multiple_commands_without_pipes runs at:35.10040497779846 s
    # execute_multiple_commands_with_pipes(client)  # execute_multiple_commands_with_pipes runs at:0.17360401153564453 s




