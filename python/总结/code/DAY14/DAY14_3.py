import threading
import time

lock = threading.RLock()

class Foo:
    global lock
    def __init__(self, n):
        self.n = n

    def One(self):
        for i in range(self.n):
            # 得到锁后才执行
            lock.acquire()
            try:
                print('one', end='')
            finally:
                lock.release()

    def Two(self):
        for i in range(self.n):
            lock.acquire()
            try:
                print('two', end='')
            finally:
                lock.release()


class MyThread(threading.Thread):
    global lock

    def __init__(self, no, foo):
        super().__init__()
        self.no = no
        self.foo = foo

    def run(self):
        if self.no == 1:
            lock.acquire()
            print('one', end='')
            lock.release()
        elif self.no == 2:
            self.foo.Two()

def main(n:int):
    foo = Foo(n)
    for i in range(n):
        t1 = MyThread(no=1, foo=foo)
        t1.start()
        t2 = MyThread(no=2,foo=foo)
        t2.start()

if __name__ == '__main__':
    main(5)
