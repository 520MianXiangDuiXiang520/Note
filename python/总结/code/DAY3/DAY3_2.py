class Foo:

    classvar1 = 0

    def __init__(self):
        self.var1 = 1

    @classmethod
    def func1(cla):
        cla.var1 = 2
        cla.classvar1 = 2

    def output(self):
        print(f'classvar={Foo.classvar1},var1={self.var1}')

if __name__ == '__main__':
    foo1 = Foo()
    foo1.output()
    foo1.func1()
    foo1.output()
    Foo.func1()
    foo1.output()
    foo2 = Foo()
    foo2.output()

    # classvar = 0, var1 = 1
    # classvar = 2, var1 = 1
    # classvar = 2, var1 = 1
    # classvar = 2, var1 = 1