import threading


def One():
    print('one', end='')


def Two():
    print('two', end='')


def Three():
    print('three', end='')


class Foo():

    def __init__(self):
        self.cd = threading.Condition()
        self.NUM = 0

    def first(self,PrintFirst:callable):
        # with语法糖
        with self.cd:
            while self.NUM != 0:
                self.cd.wait()
            PrintFirst()
            self.NUM += 1
            self.cd.notify_all()

    def Second(self,PrintSecond:callable):
        self.cd.acquire()
        while self.NUM != 1:
            self.cd.wait()
        PrintSecond()
        self.NUM += 1
        self.cd.notify_all()
        self.cd.release()

    def Third(self,PrintThird:callable):
        self.cd.acquire()
        while self.NUM != 2:
            self.cd.wait()
        PrintThird()
        self.NUM += 1
        self.cd.notify_all()
        self.cd.release()

if __name__ == '__main__':
    foo = Foo()
    callablelist = [foo.first, foo.Second, foo.Third]
    callablelistargs = [One, Two, Three]
    order = [2, 1, 3]
    A = threading.Thread(target=callablelist[order[0]-1], args=(callablelistargs[order[0]-1],))
    B = threading.Thread(target=callablelist[order[1]-1], args=(callablelistargs[order[1]-1],))
    C = threading.Thread(target=callablelist[order[2]-1], args=(callablelistargs[order[2]-1],))
    A.start()
    B.start()
    C.start()

