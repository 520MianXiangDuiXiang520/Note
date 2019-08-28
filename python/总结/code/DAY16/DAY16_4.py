def Foo():
    while True:
        print('foo', end='')
        yield

def Bar():
    while True:
        print('bar', end='')
        yield

if __name__ == '__main__':
    foo = Foo()
    bar = Bar()
    for i in range(10):
        next(foo)
        next(bar)

# foobarfoobarfoobarfoobarfoobarfoobarfoobarfoobarfoobarfoobar