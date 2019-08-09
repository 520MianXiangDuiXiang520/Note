# 生产者消费者模型
import threading
Product = []


class Producer(threading.Thread):
    """生产者，当生产的产品大于10时，生产者等待"""
    def __init__(self, condition):
        super().__init__()
        self._condition = condition

    @staticmethod
    def Production():
        Product.append('product')
        print(f'生产者：{len(Product)}')

    def run(self):
        self._condition.acquire()
        while True:
            if len(Product) == 5:
                self._condition.notify()
                self._condition.wait()
            self.Production()


class Consumers(threading.Thread):
    """消费者，当产品数小于5时，消费者等待"""
    def __init__(self, condition):
        super().__init__()
        self._condition = condition

    @staticmethod
    def Consumption():
        Product.pop(0)
        print(f'消费者:{len(Product)}')

    def run(self):
        self._condition.acquire()
        while True:
            if len(Product) == 1:
                self._condition.notify()
                self._condition.wait()
            self.Consumption()

if __name__ == '__main__':
    condition = threading.Condition()
    producer = Producer(condition)
    consumer = Consumers(condition)
    producer.start()
    consumer.start()


