from multiprocessing import Pool
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
    p = Pool(4)
    p.apply_async(Demo1)
    p.apply_async(Demo2)
    p.close()
    p.join()

