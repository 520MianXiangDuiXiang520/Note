from threading import Condition, Thread, RLock

def printNumber(n):
    print(n, end=' ')


class ZeroEvenOdd:
    def __init__(self, n):
        self.n = n
        self.con = Condition()
        self.order = 0
    # zero 唤醒even，even唤醒zero，zero唤醒odd，odd唤醒zero
    # 0 1 0 2 0 3 0 4 0 5  0  6  0  7
    # 0 1 2 3 5 6 7 8 9 10 11 12 13 14
    # printNumber(x) outputs "x", where x is an integer.
    def zero(self, printNumber) -> None:
        # 控制输出n个0
        for i in range(self.n):
            with self.con:
                # 当序号未偶数时，输出0，其余情况该线程阻塞
                while self.order % 2 != 0:
                    self.con.wait()
                printNumber(0)
                self.order += 1
                self.con.notify_all()

    def even(self, printNumber) -> None:
        # 控制输出n/2个偶数
        for i in range(self.n//2):
            with self.con:
                while self.order % 4 != 3:
                    self.con.wait()
                printNumber(self.order//2 + 1)
                self.order += 1
                self.con.notify_all()

    def odd(self, printNumber) -> None:
        for i in range(self.n - self.n // 2):
            with self.con:
                while self.order % 2 != 1:
                    self.con.wait()
                printNumber(self.order//2 + 1)
                self.order += 1
                self.con.notify_all()


if __name__ == '__main__':
    zeo = ZeroEvenOdd(14)
    t1 = Thread(target=zeo.zero, args=(printNumber,))
    t2 = Thread(target=zeo.even, args=(printNumber,))
    t3 = Thread(target=zeo.odd, args=(printNumber,))
    t1.start()
    t2.start()
    t3.start()