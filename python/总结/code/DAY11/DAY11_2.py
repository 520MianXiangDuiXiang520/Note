from functools import singledispatch

@singledispatch
def Foo(arg,*args):
    print(arg)

@Foo.register
def _1(arg:int,*args):
    print(f'int - {arg}')

@Foo.register(list)
def _2(arg,*args):
    print(f'list - {arg}')

if __name__ == '__main__':
    Foo(3)  # int - 3
    Foo([i for i in range(10)])  # list - [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    Foo("string")
    print(Foo.dispatch(int))  # <function _1 at 0x000001D7C2724B70>
    print(Foo.dispatch(list))  # <function _2 at 0x000001D7C2792E18>
    print(Foo.dispatch(str))  # <function Foo at 0x000001FB456FC268>