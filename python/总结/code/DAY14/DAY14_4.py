import threading

NUM = 0

def Foo1(num: int):
    global NUM
    for i in range(num):
        NUM += 1

def Foo2(num: int):
    global NUM
    for i in range(num):
        NUM += 1

def main():
    t1 = threading.Thread(target=Foo1,args=(1000,))
    t2 = threading.Thread(target=Foo2,args=(1000,))
    t1.start()
    t2.start()


if __name__ == '__main__':
    main()
    
