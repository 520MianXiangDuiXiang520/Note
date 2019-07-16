class Demo:
    # 类变量
    classVar = 0
    def __init__(self):
        self.instanceVar = 1

if __name__ == '__main__':
    demo1 = Demo()
    demo2 = Demo()
    print(demo1.classVar)  # 0
    print(demo2.classVar)  # 0
    Demo.classVar = 2
    print(demo1.classVar)  # 2
    print(demo2.classVar)  # 2

    print(demo1.instanceVar)  # 1
    print(demo2.instanceVar)  # 1
    demo1.instanceVar = 2
    print(demo1.instanceVar)  # 2
    print(demo2.instanceVar)  # 1
    Demo.instanceVar = 2
    print(demo1.instanceVar)  # 2
    print(demo2.instanceVar)  # 1
