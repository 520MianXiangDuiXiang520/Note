class Foo(object):
    """
    test demo
    """
    def __delattr__(self, item):
        print('删除了一个属性')
        return super().__delattr__(item)

if __name__ == '__main__':
    foo = Foo()
    foo.a = "pp"
    del foo.a
    print(Foo.__doc__)