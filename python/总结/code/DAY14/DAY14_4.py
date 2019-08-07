import threading
import time

NUM = 0
# 互斥锁
lock = threading.Lock()

def Foo1(num: int):
    global NUM
    for i in range(num):
        lock.acquire()
        NUM += 1
        lock.release()
    print(f'Foo1:{NUM}')

def Foo2(num: int):
    global NUM
    for i in range(num):
        lock.acquire()
        NUM += 1
        lock.release()
    print(f'Foo2:{NUM}')

def main():
    t1 = threading.Thread(target=Foo1,args=(1000000,))
    t2 = threading.Thread(target=Foo2,args=(1000000,))
    t1.start()
    time.sleep(0.1)
    t2.start()


if __name__ == '__main__':
    main()
    time.sleep(2)
    print(NUM)
