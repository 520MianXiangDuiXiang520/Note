from sys import getrefcount


class MyList(list):
    def __del__(self):
        print('该对象被回收')

a = MyList()
b = MyList()
a.append(b)
b.append(a)
print(f'a的引用计数{getrefcount(a)}')
print(f'b的引用计数{getrefcount(b)}')
del a
print(f'del a的引用计数{getrefcount(b[0])}')

c = MyList()
d = MyList()
c.append(d)
d.append(c)
print(f'c的引用计数{getrefcount(c)}')
print(f'd的引用计数{getrefcount(d)}')
del c
del d

print('end')