import threading
from time import sleep

POOL = []
new_POOL = []
LOCK = threading.Lock()

def my_add():
    no = 0
    while True:
        s = [i for i in range(no, no+15)]
        POOL.extend(s)
        sleep(5)
        no += 15


def get(s):
    sleep(10)
    new_POOL.append(s)

def my_push():
    while True:
        if len(POOL) > 0:
            with LOCK:
                s = POOL.pop()
            get(s)



t1 = threading.Thread(target=my_add)
thread_POOL = []
for i in range(25):
    t = threading.Thread(target=my_push)
    thread_POOL.append(t)

t1.start()
for i in thread_POOL:
    i.start()
while True:
    new_POOL.sort()
    print(new_POOL)
    sleep(5)




