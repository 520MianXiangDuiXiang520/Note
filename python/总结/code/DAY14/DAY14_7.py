from time import sleep
import threading

def Demo():
    print('start')
    sleep(3)
    print('end')

def Demo2():
    print('start2')
    sleep(1)
    print('end2')

if __name__ == '__main__':
    t1 = threading.Thread(target=Demo, name='t1')
    t2 = threading.Thread(target=Demo2, name='t2')
    t1.setDaemon(True)
    # t2.setDaemon(True)
    t1.start()
    t2.start()
    # t1.join(1)
    t2.join(1)
    # t1是守护线程，join(1)会使主线程在1s后结束，t2是非守护线程，


