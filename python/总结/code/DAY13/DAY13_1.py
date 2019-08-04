class Foo:
    def __new__(cls,*args, **kwargs):
        # 如果是第一次实例化，返回一个新对象
        if not hasattr(cls, '_object'):
            cls._object = super().__new__(cls)
        return cls._object

    def __init__(self, name):
            self.name = name

    def Print(self):
        print(f'The name of this object is: {self.name}')

if __name__ == '__main__':
    foo1 = Foo('foo1')
    foo2 = Foo('foo2')
    foo3 = Foo('foo3')
    print(foo1)  # <__main__.Foo object at 0x000001FE0B0B22B0>
    print(foo2)  # <__main__.Foo object at 0x000001FE0B0B22B0>
    foo1.Print()  # The name of this object is: foo3
    foo2.Print()  # The name of this object is: foo3
    foo3.Print()  # The name of this object is: foo3
