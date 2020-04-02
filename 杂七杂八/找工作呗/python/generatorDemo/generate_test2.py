from queue import Queue

my_queue = Queue(maxsize=5)


async def producer():
    while True:
        while not my_queue.empty():
            my_queue.get()
            print(f'消费者消费：{my_queue.qsize()}')
        await consumer()


async def consumer():
    while True:
        while not my_queue.full():
            my_queue.put("product")
            print(f'生产者生产：{my_queue.qsize()}')
        await producer()


if __name__ == '__main__':
    pro = producer()
    con = consumer()
    for i in range(10):
        pro.send(None)
        con.send(None)
