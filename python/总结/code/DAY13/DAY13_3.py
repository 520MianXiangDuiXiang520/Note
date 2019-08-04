class Foo:
    _mydict = {}
    def __new__(cls, *args, **kwargs):
        ob = super().__new__(cls)
        ob.__dict__ = cls._mydict
        return ob

if __name__ == '__main__':
    foo1 = Foo()
    foo2 = Foo()
    foo1.name = 'foo1'
    print(foo2.name)  # foo1
    # foo1 和 foo2 并不是同一个对象，只不过他们的方法和属性公用同一块内存
    print(foo1)  # <__main__.Foo object at 0x0000023ADA4A8A90>
    print(foo2)  # <__main__.Foo object at 0x0000023ADA4A8AC8>