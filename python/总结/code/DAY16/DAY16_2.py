# 生成器
from greenlet import greenlet

def Foo(n):
    for i in range(n):
        print('foo', end='')
        g2.switch(n)

def Bar(n):
    for i in range(n):
        print('bar', end='')
        g1.switch(n)


if __name__ == "__main__":
    n = 5
    g1 = greenlet(Foo)
    g2 = greenlet(Bar)
    g1.switch(n)
    g1 = g2 = None