class Demo:
    def __init__(self):
        self.var1 = 0
        self.var2 = 1

if __name__ == '__main__':
    demo = Demo()
    if hasattr(demo,'var1'):
        setattr(demo,'var1',2)
    print(getattr(demo,'var1','not find'))