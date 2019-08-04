import threading
import time

def Foo1():
    for i in range(5):
        print('********* 01 *********')
        time.sleep(1)


def Foo2():
    for i in range(5):
        print('******** 02 **********')
        time.sleep(1)


def main():
    t1 = threading.Thread(target=Foo1)
    t2 = threading.Thread(target=Foo2)

    t1.start()
    t2.start()

if __name__ == '__main__':
    main()