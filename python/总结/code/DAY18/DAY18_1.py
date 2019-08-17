from sys import getrefcount

foo: int = 1
print(getrefcount(foo))  # 91 应为包含临时引用，所以会比预期的高很多

bar: int = foo
print(getrefcount(foo))  # 92 增加了一个foo的引用，所以计数加一

List = []
List.append(foo)
print(getrefcount(foo))  # 93 作为成员存储在容器中,计数加一

def Foo(*agrs):
    print(getrefcount(foo))  # 95 作为参数传递给了函数计数加一，实参与形参的赋值使计数加一
Foo(foo)
print(getrefcount(foo))  # 93 函数生命周期结束，离开函数作用域 计数减2

del bar
print(getrefcount(foo))  # 92 对象的别名被显式销毁

List.pop()
print(getrefcount(foo))  # 91 从容器中删除

foo2: int = foo
foo2 = 2
print(getrefcount(foo))  # 91 别名被赋予新值
