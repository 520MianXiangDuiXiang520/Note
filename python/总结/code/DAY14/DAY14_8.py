from threading import Condition, Thread
import time


def printFoo():
    print('foo', end='')
    time.sleep(0.5)


def printBar():
    print('bar', end='')
    time.sleep(0.5)


class FooBar:
    def __init__(self, n):
        self.n = n
        self._lock = Condition()


    def foo(self, printFoo) -> None:
        self._lock.acquire()
        for i in range(self.n):
            printFoo()
            # 这里要先等待
            self._lock.wait()
            self._lock.notify_all()
        self._lock.release()


    def bar(self, printBar) -> None:
        self._lock.acquire()
        for i in range(self.n):
            printBar()
            # 这里要先唤醒其他线程，
            self._lock.notify_all()
            self._lock.wait()
        self._lock.release()

if __name__ == '__main__':
    n = 10
    foobar = FooBar(n)
    t1 = Thread(target=foobar.foo, args=(printFoo,))
    t2 = Thread(target=foobar.bar, args=(printBar,))
    # t2.start()
    t1.start()
    t2.start()
