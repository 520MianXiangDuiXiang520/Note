from multiprocessing import Pool, Queue, Process
import time

def Demo1(n):
   while True:
       if n.empty():
           num = 0
       else:
           num = n.get()
           print(num, end=' ')
           num += 1
       n.put(num)
       time.sleep(0.000001)

def Demo2(n):
    while True:
        if n.empty():
            num = 0
        else:
            num = n.get()
            print(num, end=' ')
            num += 1
        n.put(num)
        time.sleep(0.000001)

if __name__ == '__main__':
    n = Queue(2)
    p1 = Process(target=Demo1, args=(n,))
    p2 = Process(target=Demo2, args=(n,))

    p1.start()
    p2.start()
