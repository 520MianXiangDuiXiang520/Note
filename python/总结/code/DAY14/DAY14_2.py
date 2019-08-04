import threading

class Foo:
    def __init__(self):
        pass

    def One(self):
       pass

    def Two(self):
        pass

class MyThread(threading.Thread):
    def __init__(self,foo:object):
        super().__init__()
        self.foo = foo

    def run(self):
        self.foo.One()
        self.foo.Two()

def main(obj:object):
    t = MyThread(obj)
    t.start()

if __name__ == '__main__':
    foo = Foo()
    main(foo)
