import multiprocessing
import time


def Demo1():
    while True:
        print('0', end='')
        time.sleep(0.5)

def Demo2():
    while True:
        print('1', end='')
        time.sleep(0.5)


if __name__ == '__main__':
    p1 = multiprocessing.Process(target=Demo1)
    p2 = multiprocessing.Process(target=Demo2)

    p1.start()
    p2.start()