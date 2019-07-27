class Type(type):
    __bases__ = ()
    __base__ = None
    __mro__ = (None,)



Foo1 = Type('Foo1',() ,{})
Foo2 = Type('Foo2', (), {})
Foo3 = Type('Foo3', (), {})
Foo4 = Type('Foo4', (Foo1, Foo2), {})
Foo5 = Type('Foo5', (Foo1, Foo3), {})
Foo6 = Type('Foo6', (Foo4, Foo5), {})

if __name__ == '__main__':

    # base 为空时会多出两个属性，第一个与类描述有关，第二个与弱拷贝有关
    print(dir(Foo1))  # ['__dict__', '__doc__', '__module__', '__weakref__']
    print(dir(Foo2))  # ['__dict__', '__doc__', '__module__', '__weakref__']
    print(dir(Foo3))  # ['__dict__', '__doc__', '__module__', '__weakref__']

    # base 不为空时，默认属性表现的和经典类一样
    print(dir(Foo4))  # ['__doc__', '__module__']
    print(dir(Foo5))  # ['__doc__', '__module__']
    print(dir(Foo6))  # ['__doc__', '__module__']

    # 假如定义的是经典类，这里应该不能调用mro方法，但这里调用了，说明本身就不对，并且mro列表最后是object，进一步说明这还是一个新式类
    print(Foo1.mro())  # [<class '__main__.Foo1'>, <class 'object'>]
    print(Foo2.mro())  # [<class '__main__.Foo1'>, <class 'object'>]
    print(Foo3.mro())  # [<class '__main__.Foo1'>, <class 'object'>]
    print(Foo4.mro())  # [<class '__main__.Foo4'>, <class '__main__.Foo1'>, <class '__main__.Foo2'>, <class 'object'>]
    print(Foo5.mro())  # [<class '__main__.Foo5'>, <class '__main__.Foo1'>, <class '__main__.Foo3'>, <class 'object'>]

    # 清楚的看到MRO使用的是C3算法
    print(Foo6.mro())  # [<class '__main__.Foo6'>, <class '__main__.Foo4'>, <class '__main__.Foo5'>, <class '__main__.Foo1'>, <class '__main__.Foo2'>, <class '__main__.Foo3'>, <class 'object'>]

    # TODO: 如何在python3中定义经典类，还是根本不能定义，抛砖引玉，请赐教
