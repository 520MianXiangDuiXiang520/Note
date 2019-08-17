class MyList(list):
    def __del__(self):
        print('该对象被回收')


if __name__ == '__main__':
    a = MyList()
    b = MyList()
    # 循环引用
    a.append(b)
    b.append(a)
    del a
    del b
    # 直到程序结束，内存才会被释放
    print('程序结束')