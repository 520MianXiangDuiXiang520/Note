from queue import Queue

my_queue = Queue(maxsize=5)


def producer():
    while True:
        while not my_queue.empty():
            my_queue.get()
            print(f'消费者消费：{my_queue.qsize()}')
        yield


def consumer():
    while True:
        while not my_queue.full():
            my_queue.put("product")
            print(f'生产者生产：{my_queue.qsize()}')
        yield


if __name__ == '__main__':
    pro = producer()
    con = consumer()
    for i in range(10):
        next(con)
        next(pro)
