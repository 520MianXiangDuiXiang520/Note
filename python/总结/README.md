# python 重要知识点总结

## 目录

|DAY|CODE|DAY|CODE|
|---|----|----|----|
|DAY1|[函数的参数传递](#day-1-%e5%87%bd%e6%95%b0%e7%9a%84%e5%8f%82%e6%95%b0%e4%bc%a0%e9%80%92)|DAY2|[元类](#day-2-%e5%85%83%e7%b1%bb)|
|DAY3|[静态方法和类方法](#day-3-%e9%9d%99%e6%80%81%e6%96%b9%e6%b3%95%e5%92%8c%e7%b1%bb%e6%96%b9%e6%b3%95)|DAY4|[类变量和实例变量](#day-4-%e7%b1%bb%e5%8f%98%e9%87%8f%e5%b1%9e%e6%80%a7%e5%92%8c%e5%ae%9e%e4%be%8b%e5%8f%98%e9%87%8f%e5%b1%9e%e6%80%a7)|
|DAY5|[python自省](#day-5-python%e8%87%aa%e7%9c%81)|DAY6|[生成式，迭代器，生成器](#day-6-%e7%94%9f%e6%88%90%e5%bc%8f%e8%bf%ad%e4%bb%a3%e5%99%a8%e7%94%9f%e6%88%90%e5%99%a8)|
|DAY7|[格式化字符串的三种方法](#day-7-%e6%a0%bc%e5%bc%8f%e5%8c%96%e5%ad%97%e7%ac%a6%e4%b8%b2)|DAY8|[*args和**kwargs](#day-8-args%e5%92%8ckwargs)|
|DAY9|[闭包和装饰器](#day-9-%e9%97%ad%e5%8c%85%e5%92%8c%e8%a3%85%e9%a5%b0%e5%99%a8)|总结|[前十天总结](#%e5%89%8d%e5%8d%81%e5%a4%a9%e6%80%bb%e7%bb%93)|
|DAY10|[python鸭子类型](#day-10-%e9%b8%ad%e5%ad%90%e7%b1%bb%e5%9e%8b)|DAY11|[python 重载（single-dispatch generic function）](#day-11-python-%e9%87%8d%e8%bd%bd)|
|DAY12|[python 新式类和旧式类](#day-12-python%e6%96%b0%e5%bc%8f%e7%b1%bb%e5%92%8c%e6%97%a7%e5%bc%8f%e7%b1%bb)|||

## DAY 1. 函数的参数传递

函数参数传递有两种方式，传值和传引用，传值只是把变量的值复制一份给了实参，函数内部的操作不会改变函数外部变量的值，而传引用传递的是外部变量的地址，函数内部直接操作函数外部变量的储存空间，在调用函数之后，函数外部变量的值一般会改变

```python
def Demo(a):
    a = a + 1
    print(id(a))

if __name__ == '__main__':
    a = 3
    print(id(a)) # 140705335465056
    Demo(a) # 140705335465088
    print(id(a)) # 140705335465056
```

看到变量a在函数调用前后地址值没有改变，证明在传递数值时传递的是变量的值，字符等类型也一样，然后尝试列表，元组

```python
def Demo(a):
    a.append(3)
    print(id(a))

if __name__ == '__main__':
    s = [1,2]
    print("value = " + str(s) + "address = " + str(id(s)))  # value = [1, 2]address = 1574898786888
    Demo(s)  # value = [1, 2, 3]address = 1574898786888
    print("value = " + str(s) + "address = " + str(id(s)))  # value = [1, 2, 3]address = 1574898786888
```

函数调用前后地址值一致，证明传递的是引用，并且函数执行以后a的值也发生了改变，说明`a.append()`是在s的内存中操作的

如果传递的是元组，应为元组不可修改，所以三次输出的都是同一块地址，但其实以元组为参数传递时传递的是值。

还有一种情况

```python
def Demo(a):
    a[0].append(3)
    print("value = " + str(a) + "address = " + str(id(a)))

if __name__ == '__main__':
    a = ([1,2], 2)
    print("value = " + str(a) + "address = " + str(id(a)))  # value = ([1, 2], 2)address = 2616967970056
    Demo(a)  # value = ([1, 2, 3], 2)address = 2616967970056
    print("value = " + str(a) + "address = " + str(id(a)))  # value = ([1, 2, 3], 2)address = 2616967970056
```

如果元组中的元素是列表，在调用函数前后，函数外部的a也发生了变化，根据刚开始说的，这感觉是在传引用，但其实不是，对于函数外部的a来说，他的第0个元素始终是`<class 'list'>`,至于列表中元素有没有发生变化，元组并不关心，元组判断元素有没有改变判断的是元素的地址有没有改变，而调用append()函数时，传递的是可变元素列表，地址值不会发生改变，这也就是为什么元组不可变，但如果元组中的数据是可变类型的话该数据就可变的原因

### 1.1 总结

python有两种数据类型，可变和不可变数据，对于可变数据类型，诸如列表，字典，集合在函数传参时**传引用**，对于不可变数据类型，如数值，字符，元组，在函数传参时**传值**，但更准确的来说，python函数传参时使用**传对象引用**的方式，如果函数收到的是一个可变对象（比如字典或者列表）的引用，就能修改对象的原始值－－相当于通过“传引用”来传递对象。如果函数收到的是一个不可变对象（比如数字、字符或者元组）的引用，就不能直接修改原始对象－－相当于通过“传值'来传递对象。

最后还是要注意像元组中数据是可变类型的情况

[参考链接1](https://github.com/taizilongxu/interview_python#1-python%E7%9A%84%E5%87%BD%E6%95%B0%E5%8F%82%E6%95%B0%E4%BC%A0%E9%80%92)
[参考链接2](https://www.cnblogs.com/loleina/p/5276918.html)

## DAY 2. 元类

### 2.1 元类是什么

众所周知，对象由类实例化而来，类是对象的模板，而python一切皆对象，类也是对象，它由元类（type）创建，所以**元类是类的类**，是类的模板

### 2.2 创建类的另一种方法

一般情况下，我们使用class关键字申明一个类，就像

```python
class Demo:
    def __init__(self,name,age):
        self.name = name
        self.age = age
    
    def output(self):
        print("name is " + str(self.name) + " age is " + str(self.age))

if __name__ == '__main__':
    demo = Demo("Bob",18)
    demo.output()
```

python 中所有的类都是通过type创建的，所以当我们使用type()函数查看类的类型时会显式`<class type>`

```python
>>> class Demo:
	pass

>>> type(Demo)
<class 'type'>
>>> demo = Demo()
>>> type(demo)
<class '__main__.Demo'>
```

> 通过类实例化出来的对象的类型是`<class 类名>`，这样也更加验证了所有类都是由元类type实例化而来

#### 通过type创建类

可以看一下type的文档，type可以传入三个参数，object_or_name, bases, dict,当只有一个参数是object时，返回该对象的类型，就是最常使用的这种情况，当传入name, bases, dict参数时，会返回一个类，name是类名，bases是基类元组，dict是类中属性和方法的字典

```python
class type(object):
    """
    type(object_or_name, bases, dict)
    type(object) -> the object's type
    type(name, bases, dict) -> a new type
    """
```

我们使用type重写一下上面的Demo类

```python
# 模拟__init__()
def __init__(self,name,age):
    self.name = name
    self.age = age

def output(self):
    print("name is " + str(self.name) + " age is " + str(self.age))


class_name = 'Demo'
class_bases = (object,)
class_dict = {
    '__init__':__init__,
    'output': output,
}

# type(name, bases, dict) -> a new type
Demo = type(class_name,class_bases,class_dict)
demo = Demo('Bob',18)
demo.output()  # name is Bob age is 18
```

实际上，每次用class定义类时，执行的都是type()方法

### 2.3 MetaClass

既然所有类都是由type创建的，那我们就可以控制类的创建行为，这就需要使用元类metaclass

* 元类用来创建类，实质上也是一个类，继承自type
* `__new__`是真正的构造函数，用来分配内存空间`__new__(cls: type, name: str, bases: Tuple[type, ...], namespace: Dict[str, Any]) -> type`

```python
def add(self, value):
    print('add one value')
    self.append(value)


class ListMetaclass(type):
    def __new__(mcs, name, bases, namespace):
        namespace['add'] = add
        return type.__new__(mcs, name, bases, namespace)


class MyList(list, metaclass=ListMetaclass):
    pass


li = MyList()
li.add(1)
print(li)
```

在用class定义类时，括号中可以指定metaclass，指定后会创建`__metaclass__`,python在创建类的时候，会先检查有没有`__metaclass__`,如果有，就会以此方法创建对象，没有就会逐级向上查找父类中有没有该，如果找到当前package中还没有找到，就会使用默认的type创建(调用`metaclass.__new__()`)

>值得注意的是，如果我们在做类的定义时，在class声明处传入关键字metaclass=ListMetaclass，那么如果传入的这个metaclass有__call__函数，这个__call__函数将会覆盖掉MyList class的__new__函数。这是为什么呢？请大家回想一下，当我们实例化MyList的时候，用的语句是L1=MyList()，而我们知道，__call__函数的作用是能让类实例化后的对象能够像函数一样被调用。也就是说MyList是ListMetaclass实例化后的对象，而MyList()调用的就是ListMetaclass的__call__函数。另外，值得一提的是，如果class声明处，我们是让MyList继承ListMetaclass，那么ListMetaclass的__call__函数将不会覆盖掉MyList的__new__函数。

元类在一般情景下很少用到，但在像ORM中还是会有应用的，ORM（对象关系映射），ORM看这位大佬的文章[谈谈Python中元类Metaclass(二)：ORM实践](https://www.cnblogs.com/ArsenalfanInECNU/p/9100874.html)

### 2.4 总结

* 通过class定义的类其实是通过type()创建的
* type(object_or_name, bases, dict)
* 如果想要控制类的创建行为，需要在创建类时指定metaclass,一旦指定了metaclass，就会在class上添加`__metaclass__`，创建类时会找`__metaclass__`指向的类，并用这个类创建类，如果找不到，就会调用默认的type()

参考文章

[Python中的元类(metaclass)](https://github.com/taizilongxu/interview_python#2-python%E4%B8%AD%E7%9A%84%E5%85%83%E7%B1%BBmetaclass)
[谈谈Python中元类Metaclass(一)：什么是元类](https://www.cnblogs.com/ArsenalfanInECNU/p/9036407.html)
[Python之元类](https://www.cnblogs.com/tootooman/p/9225626.html)

## DAY 3. 静态方法和类方法

有四种方法，实例方法，类方法，静态方法，属性方法

* 实例方法

实例方法的第一个参数是`self`，他会指向类的实例化对象，只能被对象调用，如

```python
class Demo:

    def instanceMethod(self):
        print("this is a instance method")

if __name__ == "__main__":
    demo = Demo()
    demo.instanceMethod()

```

用点调用时不需要传入对象参数，python会把调用实例方法的对象作为实例方法的第一个参数传入，等价于

```python
if __name__ == '__main__':
    demo = Demo()
    Demo.instanceMethod(demo)
```

* 类方法

使用装饰器`@classmethod`。第一个参数必须是当前类对象，该参数名一般约定为“cls”，可以使用类（例如C.f（））或实例（例如C（）。f（））调用类方法。 除了类之外，该实例被忽略。 如果为派生类调用类方法，则派生类对象将作为隐含的第一个参数传递。

```python
class Demo:

    @classmethod
    def classMethod(self):
        print("this is a class method")

if __name__ == "__main__":
    demo = Demo()
    Demo.classMethod()
    demo.classMethod()
```

同样是语法糖，用点调用时会自动把调用类方法的类或对象作为第一个参数传入

* 静态方法

用 @staticmethod 装饰的不带 self 参数的方法叫做静态方法，静态方法不会接收隐式的第一个参数，类似于c++中的静态方法，只是占用了类的命名空间，与类没有联系，了一使用类名或对象名调用

* 属性方法

用来将一个方法变成静态属性，使用修饰器`@property`

```python
class C:
    def __init__(self):
        self._x = None

    @property
    def x(self):
        """I'm the 'x' property."""
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @x.deleter
    def x(self):
        del self._x
```

TODO : 有点难改天专门学

### 3.1 总结

|方法|修饰器|调用|使用场景（个人理解）|
|----|-----|----|------------------|
|实例方法|/|只能被对象调用|大多数场景|
|类方法|@classmethod|能被对象或类调用|只操作类属性|
|静态方法|@staticmethod|能被对象或类调用|不操作类中的属性和方法|
|属性方法|@property|按静态属性的方法调用（不加括号）|TODO|

参考文章
[GitHub 关于python的面试题](https://github.com/taizilongxu/interview_python#3-staticmethod%E5%92%8Cclassmethod)

[Python静态方法、类方法、属性方法](https://baijiahao.baidu.com/s?id=1628397032035477047&wfr=spider&for=pc)

[Python面向对象静态方法，类方法，属性方法](https://www.cnblogs.com/revo/p/7381101.html)

[Python 实例方法、类方法、静态方法的区别与作用](https://www.cnblogs.com/wcwnina/p/8644892.html)

[python 文档 staticmethod](https://docs.python.org/3.7/library/functions.html#staticmethod)

[python 文档 classmethod](https://docs.python.org/3.7/library/functions.html#classmethod)

## DAY 4. 类变量（属性）和实例变量（属性）

* 类变量：在所有类的实例之间都可以共享的变量，类变量在所有对象间只保留一份
  * 在类体中定义
  * 类的所有实例对象都可以访问类变量
  * 类变量只能由类修改，实例对象只有读权限
  * **使用`对象名.类变量名 = new value`不是在使用对象修改类属性，而是给对象添加了一个新属性**

```python
class Demo:
    # 类变量
    classVar = 0
    def __init__(self):
        self.instanceVar = 1

if __name__ == '__main__':
    demo1 = Demo()
    demo2 = Demo()
    # 类的所有实例对象都可以访问类变量
    print(demo1.classVar)  # 0
    print(demo2.classVar)  # 0
    # 由类修改类变量
    Demo.classVar = 2
    print(demo1.classVar)  # 2
    print(demo2.classVar)  # 2
    # 注意，这样不是在修改类变量，而是给实例对象添加了一个属性
    demo1.classVar = 2
    print(demo1.classVar)  # 2
```

* 实例变量：实例化对象时，每个对象都会有自己的实例变量，各实例变量之间不影响
  * 在构造函数中定义
  * 实例变量由实例对象修改，类修改实例变量没意义
  * 每个实例对象有一份实例变量

```python
class Demo:
    # 类变量
    classVar = 0
    def __init__(self):
        # 实例变量
        self.instanceVar = 1

if __name__ == '__main__':
    print(demo1.instanceVar)  # 1
    print(demo2.instanceVar)  # 1
    # 各实例对象间的实例变量互相不影响
    demo1.instanceVar = 2
    print(demo1.instanceVar)  # 2
    print(demo2.instanceVar)  # 1
    # 用类修改实例变量没意义
    Demo.instanceVar = 2
    print(demo1.instanceVar)  # 2
    print(demo2.instanceVar)  # 1

```

### 4.1 总结

|变量（属性）|定义|读取|修改|内存|
|-----------|----|----|---|----|
|类变量|在类体中定义|`className.classVar`和`objectName.classVar`|`className.classVar = new value`|只保留一份|
|实例变量|在构造函数中定义|`objectName.instanceVar`|`objectName.instanceVar = new value`|每个实例对象保存一份，各对象间互不影响|

> **注意：**使用`objectName.classVar = new value`是给对象添加了一个新属性

参考文章：
[GitHub 关于python的面试题](https://github.com/taizilongxu/interview_python#4-%E7%B1%BB%E5%8F%98%E9%87%8F%E5%92%8C%E5%AE%9E%E4%BE%8B%E5%8F%98%E9%87%8F)

[python（类和对象之类属性和类变量）](https://blog.csdn.net/huo_1214/article/details/79233636)

[图解Python 【第五篇】：面向对象-类-初级基础篇](https://www.cnblogs.com/geekmao/p/7562667.html)

## DAY 5. python自省

>In computing, type introspection is the ability of a program to examine the type or properties of an object at runtime. Some programming languages possess this capability.
>在计算机科学中，内省是指计算机程序在运行时（Run time）检查对象（Object）类型的一种能力，通常也可以称作运行时类型检查

这是维基百科对自省（内省）的解释,通俗来说，自省就是在程序运行过程中，能够知道对象的类型的一种能力，大部分语言都有这种能力（都有办法在运行过程中知道对象的类型），如c++，Java等

当然自省不仅仅只针对对象的类型，如python自省还能知道对象的属性，还有一些其他的理解

>在日常生活中，自省（introspection）是一种自我检查行为。
>
>在计算机编程中，自省是指这种能力：检查某些事物以确定它是什么、它知道什么以及它能做什么。自省向程序员提供了极大的灵活性和控制力。
>
>说的更简单直白一点：自省就是面向对象的语言所写的程序在运行时，能够知道对象的类型。简单一句就是，运行时能够获知对象的类型。

例如c++自省(来自维基百科)

C ++通过运行时类型信息（RTTI）typeid和dynamic_cast关键字支持类型内省。 dynamic_cast表达式可用于确定特定对象是否属于特定派生类。 例如：

```cpp
Person* p = dynamic_cast<Person *>(obj);
if (p != nullptr) {
  p->walk();
}
```

typeid运算符检索std :: type_info对象，该对象描述对象的派生类型：

```cpp
if (typeid(Person) == typeid(*obj)) {
  serialize_person( obj );
}

```

php自省(来自维基百科)

在php中，可以使用instanceof运算符判断一个PHP变量是否属于某一类的实例

```php
if ($obj instanceof Person) {
    // Do whatever you want
}
```

Java自省(来自维基百科)

Java中类型自省的最简单示例是instanceof运算符。 instanceof运算符确定特定对象是属于特定类（或该类的子类，还是实现该接口的类）。 例如：

```java
if (obj instanceof Person) {
    Person p = (Person)obj;
    p.walk();
}
```

### 5.1 python实现自省的办法

python实现自省有很多方法，常用的有 help(),dir(),type(),hasattr()，getattr(),setattr(),isinstance(),issubclass(),id(),callable()

#### 5.1.1 help()

help() 函数用于查看函数或模块用途的详细说明。主要在IDE环境下是用，接受任何拥有函数或者方法的对象，打印出对象所有的函数和文档字符串

如可以直接打印出os模块的帮助文档

```python
import os
help(os)
# Help on module os:
#
# NAME
#     os - OS routines for NT or Posix depending on what system we're on.
#
# DESCRIPTION
# 后面的省略了
```

也可以是我们自定义的类，函数，或模块

```python
class Demo:
    """
    this is a Demo
    """
    classVar = 0

    def __init__(self):
        self.var1 = 1

    def output(self):
        print(self.var1)

if __name__ == '__main__':
    help(Demo)
```

运行之后会打印出这个类的完整信息

```txt
Help on class Demo in module __main__:

class Demo(builtins.object)
 |  this is a Demo
 |  
 |  Methods defined here:
 |  
 |  __init__(self)
 |      Initialize self.  See help(type(self)) for accurate signature.
 |  
 |  output(self)
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |  
 |  __dict__
 |      dictionary for instance variables (if defined)
 |  
 |  __weakref__
 |      list of weak references to the object (if defined)
 |  
 |  ----------------------------------------------------------------------
 |  Data and other attributes defined here:
 |  
 |  classVar = 0
```

实例对象会打印出类的信息

函数会打印出帮助文档，没有文档会打印none

```python
 def demoMethods(a):
        """
        这是一个示例函数
        :param a: 示例形参
        :return: None
        """
        print(a)
    help(demoMethods)
# Help on function demoMethods in module __main__:

# demoMethods(a)
#     这是一个示例函数
#     :param a: 示例形参
#     :return: None
```

更详细的请看这篇文章

[Python-自省机制](https://www.cnblogs.com/mitnick/p/8525849.html)

#### 5.1.2 dir()

>dir() 函数不带参数时，返回当前范围内的变量、方法和定义的类型列表；带参数时，返回参数的属性、方法列表。如果参数包含方法__dir__()，该方法将被调用。如果参数不包含__dir__()，该方法将最大限度地收集参数信息。

```python console
dir()
['__builtins__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'sys']
dir([])
['__add__', '__class__', '__contains__', '__delattr__', '__delitem__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__iadd__', '__imul__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__rmul__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', 'append', 'clear', 'copy', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort']

```

#### 5.1.3 hasattr()，getattr(),setattr()

```python
class Demo:
    def __init__(self):
        self.var1 = 0
        self.var2 = 1

if __name__ == '__main__':
    demo = Demo()
    if hasattr(demo,'var1'):
        setattr(demo,'var1',2)
    print(getattr(demo,'var1','not find'))  # 2
    print(getattr(demo,'var11','not find'))  # not find
```

* hasattr()

```python
def hasattr(*args, **kwargs): # real signature unknown
    """
    Return whether the object has an attribute with the given name.
    返回对象是否具有给定名称的属性。

    This is done by calling getattr(obj, name) and catching AttributeError.
    这是通过调用getattr(obj，name)并捕获AttributeError来完成的.
    """
    pass
```

* setattr()

```py
def setattr(x, y, v): # real signature unknown; restored from __doc__
    """
    Sets the named attribute on the given object to the specified value.
    将给定对象的命名属性设置为指定值。

    setattr(x, 'y', v) is equivalent to ``x.y = v''
    setattr(x，‘y’，v)等价于“x.y=v”
    """
    pass
```

* getattr()

```py
def getattr(object, name, default=None): # known special case of getattr
    """
    getattr(object, name[, default]) -> value

    Get a named attribute from an object; getattr(x, 'y') is equivalent to x.y.
    When a default argument is given, it is returned when the attribute doesn't
    exist; without it, an exception is raised in that case.
    从对象中获取指定名称的属性；getattr(x，‘y’)等同于X.Y。
    如果给定了默认参数，则未找到该属性时将返回该参数。
    如果未指定，则会引发异常。
    """
    pass
```

#### 5.1.4 isinstance()，issubclass()

```python console
>>> help(isinstance)
Help on built-in function isinstance in module builtins:

isinstance(obj, class_or_tuple, /)
    Return whether an object is an instance of a class or of a subclass thereof.
    返回对象是类的实例还是其子类的实例。
    A tuple, as in ``isinstance(x, (A, B, ...))``, may be given as the target to
    check against. This is equivalent to ``isinstance(x, A) or isinstance(x, B)
    or ...`` etc.
```

instance类似于type(),只不过type() 不会认为子类是一种父类类型，不考虑继承关系。isinstance() 会认为子类是一种父类类型，考虑继承关系。

```python console
>>> class A:
	pass

>>> a = A()
>>> isinstance(a,type)
False
>>> class B(A):
	pass

>>> b=B()
>>> isinstance(b,A)
True
>>> isinstance(int,type)
True
>>> isinstance(A,type)
True
>>> isinstance(b,type)
False
>>> isinstance(True,int)
True
```

可以看出类是type的子类型，也验证了前天的元类，而布尔是int的子类

而issubclass()则是用来判断一个类是不是另一个类的子类,传入的两个参数都是类名

```console
>>> issubclass(B,A)
True
```

#### 5.1.5 id()和callable()

* id(): 用于获取对象的内存地址
* callable()：判断对象是否可以被调用。

#### 5.1.6 type()

这个函数在元类中写过了，当传入一个参数时会返回对象的类型，这也是python自省中比较常用的方法

### 5.2 总结

* 什么是自省

简单来说就是在程序运行过程中能知道对象类型（还有属性等）的能力

* python实现自省的方法

|方法|作用|
|----|----|
|help()|查看函数或模块用途的详细说明|
|dir()|返回对象所有属性|
|type()|查看对象类型|
|hasattr()|查看对象是否有特定属性|
|getattr()|得到对象的特定属性|
|seetattr()|设置对象的特定属性|
|isinstance()|判断一个对象是否是一个已知的类型|
|issubclass()|判断一个类是不是另一个类的子类|
|id()|返回地址值|
|callable()|判断对象是否可调用|

参考文章

[python面试题](https://github.com/taizilongxu/interview_python#5-python%E8%87%AA%E7%9C%81)

[wikipedia Type introspection](https://en.wikipedia.org/wiki/Type_introspection#Examples)

[Python自省（反射）指南【转】](https://yq.aliyun.com/articles/391304?spm=a2c4e.11155472.0.0.e32e17127BcBOe)

在这篇文章中说
>在笔者，也就是我的概念里，自省和反射是一回事，当然其实我并不十分确定一定以及肯定...

但是我在维基百科看见了这句话
>Introspection should not be confused with reflection, which goes a step further and is the ability for a program to manipulate the values, meta-data, properties and/or functions of an object at runtime.

也就是说自省和反射不是同一回事，自省是获取对象类型的能力，而反射是操纵对象的值，元数据，属性和/或函数的能力

[Python常用的自省函数](https://blog.csdn.net/Lucymiq/article/details/80415951)

[Python-自省机制](https://www.cnblogs.com/mitnick/p/8525849.html)

[Python自省](https://www.jianshu.com/p/5166427002a8)

[菜鸟教程](https://www.runoob.com/python/python-tutorial.html)

## DAY 6. 生成式,迭代器，生成器

### 6.1 生成式

#### 6.1.1 列表生成式

```python
list = [index for index in range(10)]
```

#### 6.1.2 字典生成式

```python
dict = {
    'zhangsan': 10,
    'lisi': 12,
    'wangwu': 18
}
# 实现键值互换
dict = {k:v for v,k in dict.items() if k >= 12}
```

#### 6.1.3 集合生成式

```python
# 100以内的质数
set = {i for i in range(100) if i % 2 != 0}
```

### 6.2 生成器

生成式会创建一个列表（字典或集合），但无论是字典，列表还是集合，都不能保存一个无限长的序列，比如说全体自然数，当然我们一般不会用到这种序列，但哪怕是万位的序列，保存为列表或集合也是很占用空间的，加上一般情况下我们对一个序列的操作是一次性的，根本不需要保存，那有没有一种办法只有我们需要时才给我们数据，我们不需要时程序只保留“算法”呢？这就用到了生成器

创建生成器有两种办法，一种是类似于推导式，把列表推导式的中括号改为小括号就行，会返回一个生成器对象，可以使用next()或for循环遍历

```py
t = (i for i in range(100) if i % 2 == 0)
for i in t:
    print(i)
```

举个栗子，斐波那契数列，每一项是前两项之和

一般情况

```py
feibo = [1, 1]
for i in range(2,10000):
    feibo.append(feibo[i - 1] + feibo[i - 2])
print(feibo)
```

我们要做的只是要打印出来而已，没必要保存这么大的数组，这时我们可以用生成器

```python
def feb(f, s, max):
    i = 0
    while i < max:
        f, s = s, f + s
        i += 1
        yield s

for i in feb(1, 1, 100):
    print(i)
```

生成器长得和函数一样，只不过return 变成了yield ，每当运行到yield后，程序就会阻塞，只有在调用该生成器的next()方法时才会从上次暂停的地方继续

```py
def Demo():
    print(1)
    yield 1
    print(2)
    yield 2
    print(3)
    yield 3

demo = Demo()
next(demo)
next(demo)
next(demo)
next(demo)

# 1
# 2
# 3
# Traceback (most recent call last):
#   File "E:/xxxx/DAY6_1.py", line 45, in <module>
#     next(demo)
# StopIteration
```

当超出生成器范围时会抛出StopIteration异常，我们一般也不会使用next,for就是捕捉StopIteration异常遍历生成器的

```py
for i in Demo():
    i

# 等价于

while(True):
    try:
        next(demo)
    except StopIteration:
        break
```

### 6.3 迭代器

#### 6.3.1 可迭代对象

可以直接作用于for循环的对象统称为可迭代对象：Iterable，主要有两类，列表，元组，字典，集合等数据类型和生成器，可以使用isinstance()判断一个对象是否是Iterable对象。

#### 6.3.2 迭代器

可以被next()函数调用并不断返回下一个值的对象称为迭代器：Iterator。可以使用isinstance()判断一个对象是否是Iterator对象

生成器都是Iterator对象，但list、dict、str虽然是Iterable，却不是Iterator。把list、dict、str等Iterable变成Iterator可以使用iter()函数

>你可能会问，为什么list、dict、str等数据类型不是Iterator？
>
>这是因为Python的Iterator对象表示的是一个数据流，Iterator对象可以被next()函数调用并不断返回下一个数据，直到没有数据时抛出StopIteration错误。可以把这个数据流看做是一个有序序列，但我们却不能提前知道序列的长度，只能不断通过next()函数实现按需计算下一个数据，所以Iterator的计算是惰性的，只有在需要返回下一个数据时它才会计算。
>
>Iterator甚至可以表示一个无限大的数据流，例如全体自然数。而使用list是永远不可能存储全体自然数的。

### 6.4 总结

* 生成式

|生成式|语法|
|---|---|
|列表生成式|`L = [i for i in range(100) if i % 2 ==0]`|
|字典生成式|`k:v for k, v in dict.items() if k < 10`|
|集合生成式|`S = {i for i in range(100) if i % 2 ==0}`|

* 生成器

创建：
生成式方式和生成器函数
读取：
next()或for

* 迭代器

|可迭代对象|能被for直接作用的对象|
|------------|---|
|迭代器|能用next()执行的可迭代对象|

参考文章：

[GitHub python面试题](https://github.com/taizilongxu/interview_python#6-%E5%AD%97%E5%85%B8%E6%8E%A8%E5%AF%BC%E5%BC%8F)

[廖雪峰的官方网站](https://www.liaoxuefeng.com/wiki/1016959663602400/1017323698112640)

[python 生成器和迭代器有这篇就够了](https://www.cnblogs.com/wj-1314/p/8490822.html)

## DAY 7. 格式化字符串

到目前为止，我所知道的，python格式化字符串有三种方法，第一是早期就有的%，其次是2.5之后的format(),还有就是3.6添加的f字符串调试

### 7.1 %格式化字符串

%格式化字符串是python最早的，也是能兼容所有版本的一种字符串格式化方法，在一些python早期的库中，建议使用%格式化方式，他会把字符串中的格式化符按顺序后面参数替换，格式是

```py
"xxxxxx %s xxxxxx" % (value1, value2)
```

* 其中 `%s`就是格式化符，意思是把后面的值格式化为字符类型，类似的格式化符还有`%d`,`%f`等，具体参考文章[Python字符串格式化](https://www.cnblogs.com/vitrox/p/4504899.html)
* 后面的`value1`,`value2`就是要格式化的值，不论是字符还是数值，都会被格式化为格式化符对应的类型
* 当然可以不用以元组的形式传值，你可以直接写这样：`"xxxxx %s" % value`，不过不建议这样写，一是应为这样只能传递一个参数，二是如果value是元组或列表等类型，这样会触发TypeErrer
* 如果只传一个参数，并且很确定参数类型不会触发异常，可以使用上面的写法，否则，我建议你提供一个单元素元组，就像`"xxxx %s " % (value,)`

```py
value1 = (7, 8)
value2 = [9, 0]
print("DAY %s 格式化字符串 %s " % (value1,value2))
value3 = 1
s = "xxxix %s" % value3  # 不推荐
print(s)
s1 = "xxxx %s " % value1
print(s1)  # TypeError: not all arguments converted during string formatting
```

### 7.2 format()

%虽然强大，但用起来难免有些麻烦，代码也不是特别美观，因此，在python 2.5 之后，提供了更加优雅的`str.format()`方法。

```py
    def format(self, *args, **kwargs): # known special case of str.format
        """
        S.format(*args, **kwargs) -> str

        Return a formatted version of S, using substitutions from args and kwargs.
        The substitutions are identified by braces ('{' and '}').
        """
        pass
```

* format()的常用用法

```py
# 使用名称占位符
s2 = "xxxx {age} xxxx {name}".format(age=18, name="hangman")
print(s2)  # xxxx 18 xxxx hangman

# 使用序号占位符，为空默认从左到右01234.。。
s3 = "xxxx {1} xxx{0}".format(value1,value2)
print(s3)  # xxxx [9, 0] xxx(7, 8)

# 也可以混合使用
s4 = "xxxx {} XXX {name} xxx {}".format(value2,value1,name="s4")
print(s4)  # xxxx [9, 0] XXX s4 xxx (7, 8)
```

### 7.3 f-string

f-string是2015年python 3.6 根据PEP 498新添加的一种字符串格式化方法，f-string实际上是在运行时计算的表达式，而不是常量值。在Python源代码中，f-string是一个文字字符串，前缀为'f'，其中包含大括号内的表达式。表达式会将大括号中的内容替换为其值。例如

```py
import datetime
name = "zings"
age = 17
date = datetime.date(2019,7,18)
print(f'my name is {name}, this year is {date:%Y},Next year, I\'m {age+1}')  # my name is zings, this year is 2019,Next year, I'm 18
```

#### 7.3.2 格式规范迷你语言

“格式规范”用于格式字符串中包含的替换字段中，以定义各个值的显示方式

标准格式说明符的一般形式是：

```py
format_spec     ::=  [[fill]align][sign][#][0][width][grouping_option][.precision][type]
fill            ::=  <any character>
align           ::=  "<" | ">" | "=" | "^"
sign            ::=  "+" | "-" | " "
width           ::=  digit+
grouping_option ::=  "_" | ","
precision       ::=  digit+
type            ::=  "b" | "c" | "d" | "e" | "E" | "f" | "F" | "g" | "G" | "n" | "o" | "s" | "x" | "X" | "%"
```

##### (1) 对齐 align

|align（对齐方式）|作用|
|------|---|
|`<`|左对齐（字符串默认对齐方式）|
|`>`|右对齐（数值默认对齐方式）|
|`=`|填充时强制在正负号与数字之间进行填充，只支持对数字的填充|
|`^`|居中|

* 除非定义了最小字段宽度，否则字段宽度将始终与填充它的数据大小相同，因此在这种情况下，对齐选项没有意义。
* 如果指定了align值，则可以在其前面加上可以是任何字符的填充字符，如果省略则默认为空格。 无法使用文字大括号（“{”或“}”）作为格式化字符串文字中的填充字符或使用str.format（）方法。 但是，可以插入带有嵌套替换字段的大括号。

```python
print(f'{name:^18}')  # |      zings     |
```

##### (2) sign

sign只对数字起作用

|sign|作用|
|-----|---|
|`+`|强制对数字使用正负号|
|`-`|仅对负数使用前导负号(默认)|
|`空格`|对正数使用一个' '作前导，负数仍以'-'为前导|

```py
print(f'{money:+}')  # +19999999877
```

##### (3) #选项

>'＃'选项使“替代形式”用于转换。 对于不同类型，替代形式的定义不同。 此选项仅对integer，float，complex和Decimal类型有效。 对于整数，当使用二进制，八进制或十六进制输出时，此选项将前缀“0b”，“0o”或“0x”添加到输出值。 对于浮点数，复数和十进制，替换形式会导致转换结果始终包含小数点字符，即使后面没有数字也是如此。 通常，只有在跟随数字的情况下，这些转换的结果中才会出现小数点字符。 此外，对于“g”和“G”转换，不会从结果中删除尾随零。

##### (4) ,选项

','被用来对数字整数部分进行千分位分隔

|描述符|作用|
|------|----|
|,|使用,作为千位分隔符|
|_|使用_作为千位分隔符|

>
* `,` 仅适用于浮点数、复数与十进制整数：对于浮点数和复数，, 只分隔小数点前的数位。
* `_` 适用于浮点数、复数与二、八、十、十六进制整数：对于浮点数和复数，_ 只分隔小数点前的数位；对于二、八、十六进制整数，固定从低位到高位每隔四位插入一个 _（十进制整数是每隔三位插入一个 _）。

```py
print(f'{money:,}')  # 19,999,999,877
```

##### (5) width

width是定义最小字段宽度的十进制整数。 如果未指定，则字段宽度将由内容确定。

当然，format还有很多彪悍的特性，还可以看这位大佬的文章：[Python字符串格式化](https://www.cnblogs.com/vitrox/p/4504899.html)

##### (6) .precision

.precision对于数字对象，用来指定数字的小数位数，如果有小数；对于非数字对象，用来指定最终返回的格式化字符的最大长度，即格式化完成后，以这个precision参数对结果进行截取

##### (7) type

![python_总结_01.png](../../image/python_总结_01.png)

**注意：**格式规范迷你语言对format一样适用（本来就是format的）

### 7.4 总结

python最先的格式化字符串方法是%，但他的致命缺点是支持的类型有限，只支持int,str,double,其他所有类型只能转换为这几个类型，还有如果传递的是元组，那么必须还要传入一个单值元组，为此，添加了str.format（）以解决％-formatting中的一些问题，特别是，它使用普通函数调用语法（并因此支持多个参数），并且可以通过__format __（）方法在被转换为字符串的对象上进行扩展。但str.format（）又存在代码冗余的问题，例如

```py
v = 6*8
print("the value is {}".format(v))
```

而使用f-string只需要

```py
print(f'the value is{6*8}')
```

F字符串提供了一种简洁易读的方式，可以在字符串中包含Python表达式的值。包括lambda表达式（要放在括号里）

参考文章

[PEP 498](https://www.python.org/dev/peps/pep-0498/)

[python doc](https://docs.python.org/3/library/string.html#string.Formatter)

[Python字符串格式化](https://www.cnblogs.com/vitrox/p/4504899.html)

[Python格式化字符串f-string概览](https://blog.csdn.net/sunxb10/article/details/81036693)

[GitHub python 面试题](https://github.com/taizilongxu/interview_python#8-%E5%AD%97%E7%AC%A6%E4%B8%B2%E6%A0%BC%E5%BC%8F%E5%8C%96%E5%92%8Cformat)

## DAY 8. *args和**kwargs

`*args`：多值元组，`**kwargs`多值字典，他们是python函数传参时两个特殊的参数，args和kwargs并不是强制的，但习惯使用这两个，如果在函数参数列表中声明了`*args`，则允许传递任意多的参数，多余的参数会被以元组的形式赋给args变量，而`**kwargs`允许你使用没有定义的变量名，会把显式传递的参数打包成字典

```py
def output(*args, **kwargs):
    print(args)
    print(kwargs)

output('zhangsan', 'lisi', 5, 6,a=1,b=2,c=3)

# ('zhangsan', 'lisi', 5, 6)
# {'a': 1, 'b': 2, 'c': 3}
```

如果函数还有别的参数，传递参数时会从左到右依次对照赋值，所以请务必把`*args`和`**kwargs`放在函数参数列表的最后，否则会抛出TypeError异常，并且`*args`必须放在`**kwargs`前面，正确的参数顺序应该是

```py
def fun(arg, *args, **kwargs):
    pass
```

在调用函数时也可以使用`*`和`**`

```py
def put(a, b, c):
    print(f'a={a},b={b},c={c}')

put(*mylist)  # a=aardvark,b=baboon,c=cat

s = {'a': 1, 'b': 2, 'c': 3}
put(**s)  # a=1,b=2,c=3
```

之所以能实现这样的功能，原理是序列解包，下面简单介绍序列解包

```py
>>> s = "ABCDE"
>>> a,b,c,d,e = s
>>> a,c
('A', 'C')

>>> t = (1,2,3,4,5)
>>> a1,b1,c1,d1,e1 = t
>>> a1,c1
(1, 3)
```

上面就是用到了序列解包，左右两端的元素个数必须相等，否则会抛出ValueError异常

```py
>>> a2,b2 = s
Traceback (most recent call last):
  File "<pyshell#6>", line 1, in <module>
    a2,b2 = s
ValueError: too many values to unpack (expected 2)
```

但总不能所有序列都一一对应把，如果序列有很多位或不确定有多少位时使用序列解包就显得很不方便了，这时候就可以使用`*`和了

```py
>>> a3,*a4 = s
>>> a3,a4
('A', ['B', 'C', 'D', 'E'])
```

```py
>>> while s:
        f,*s = s
        print(f,s)

A ['B', 'C', 'D', 'E']
B ['C', 'D', 'E']
C ['D', 'E']
D ['E']
E []
```

参考文章：

[详解Python序列解包（4）](https://cloud.tencent.com/developer/article/1098734)

[stack overflow](https://stackoverflow.com/questions/3394835/use-of-args-and-kwargs)

[从一个例子看Python3.x中序列解包](https://blog.csdn.net/Jerry_1126/article/details/78510847)

[GitHub python面试题](https://github.com/taizilongxu/interview_python#10-args-and-kwargs)

## DAY 9. 闭包和装饰器

### 9.1 闭包

> 闭包就是内部函数对外部函数作用域内变量的引用

可以看出

* 闭包是针对函数的，还有两个函数，内部函数和外部函数
* 闭包是为了让内部函数引用外部函数作用域内的变量的

我们先写两个函数

```py
def fun1():
    print("我是fun1")

    def fun2():
        print("我是fun2")
```

这样fun2就作为fun1的内部函数，此时在函数外部是无法调用Fun2的，因为

1. fun2实际上相当于fun1的一个属性(方法)，作用域是fun1的块作用域，全局作用域中无法找到，
2. 函数内属性的生命周期是在函数运行期间，在fun1中只是定义了fun2，并没有调用它

为了让fun2跳出fun1的生命周期，我们需要返回fun2，这样在外部获取到的fun1的返回值就是fun2，这样调用fun1的返回值就是调用了fun2,如：

```py
def fun1():
    print("我是fun1")
    def fun2():
        print("我是fun2")
    return fun2

var = fun1()
var()
# 我是fun1
# 我是fun2
```

当然，这还不是一个闭包，闭包是引用了自由变量的函数，所谓自由变量可以理解为局部变量，如果fun2调用了fun1中的变量，那么fun2就是一个闭包了。如

```py
def fun1(var1):
    def fun2():
        print(f"var1 = {var1}")
    return fun2

var = fun1(1)
var()  # var1 = 1
```

#### 闭包的作用

闭包私有化了变量，实现了数据的封装，类似于面向对象

```py
def fun1(obj):
    def fun2():
        obj[0] += 1
        print(obj)
    return fun2


if __name__ == '__main__':
    mylist = [i for i in range(5)]
    var = fun1(mylist)
    var()
    var()
    var()
    # [1, 1, 2, 3, 4]
    # [2, 1, 2, 3, 4]
    # [3, 1, 2, 3, 4]
```

### 9.2 装饰器

闭包在python中有一个重要的用途就是装饰器，装饰器接受被装饰的函数作为参数并执行一次调用，装饰器的本质还是一个闭包

```py
def func1(func):
    def func2():
        print("func2")
        return func()
    return func2


@func1
def Demo():
    print("Demo")


if __name__ == '__main__':
    Demo()
    # func2
    # Demo
```

* 首先，`@func1`是一颗语法糖，等价于`func1(Demo)()`
* 外部函数必须能接收一个参数，也只能接受一个参数，如果有多个参数，必须再套一个函数，因为在使用`@`语法糖时，会自动把被修饰函数作为参数传递给装饰器
* 内部函数必须返回被装饰函数的调用

运行流程：

1. 把被修饰函数作为参数传递给装饰器,这时函数返回的是闭包函数func2
2. 隐式地调用func2,相当于`func2()`，执行函数体，输出func2,这时函数返回值是`func()`,返回的直接是被修饰函数的调用，相当于直接执行被修饰函数，输出Demo

相当于：

```py
def func1(func):
    def func2():
        print("func2")
        return func()
    return func2


# @func1
def Demo():
    print("Demo")


if __name__ == '__main__':
    # s = Demo()
    # 先把被修饰函数作为参数传递给修饰器，这里的s就是func2
    s = func1(Demo)
    # 调用闭包函数
    s()
    print(s)

    # func2
    # Demo
    # <function func1.<locals>.func2 at 0x00000117F163AD90>

```

#### 9.2.1 装饰器带参数

```py
def func1(num):
    def func2(func):
        def func3():
            if num >10:
                print("大于10")
            else:
                print("小于10")
            return func()
        return func3
    return func2


@func1(num=12)
def Demo():
    print("Demo")


if __name__ == '__main__':
    Demo()b
```

执行流程

1. 将装饰器的参数传递给第一层函数，并返回第二层函数func2
2. 将被修饰函数作为参数传递给第二层函数func2,隐式调用func2，返回闭包函数
3. 执行闭包函数，并返回被修饰函数的调用（执行被修饰函数）

#### 9.2.2 被修饰函数带参数

如果被修饰函数带有参数，需要把参数传递给内层闭包函数,返回被修饰函数的调用时记得加参数

```py
def func1(func):
    def func2(arg):
        arg += 1
        # 记得加参数
        return func(arg)
    return func2

@func1
def Demo(arg):
    print(arg)

if __name__ == '__main__':
    Demo(11)  # 12
```

#### 9.2.3 例

1. 求斐波那契数列任意一项的值

```py
import time

def code_time(func):
    '''
    修饰器，用来打印函数运行时间
    :param func: 被修饰函数
    :return: func
    '''
    start_time = time.time()
    def closer(*args,**kwargs):
        result = func(*args,**kwargs)
        codeTime = time.time() - start_time
        print(f"This code runs at:{codeTime}")
        return result
    return closer

def _Fibonacci(n):
    if n <= 1:
        return 1
    else:
        return _Fibonacci(n-1) + _Fibonacci(n-2)

@code_time
def Fibonacci(n):
    return _Fibonacci(n)


if __name__ == '__main__':
    var = Fibonacci(40)
    print(var)
    # This code runs at:61.738335609436035
    # 165580141
```

发现代码效率非常低，输出第四十个值需要一分多钟，这是应为每计算一个值，需要计算前两个值，这里有很多重复的，如

```txt
            10
            |
    |-----------------|
    9                 8
|--------|       |--------|
8        7       7        6

7，8被重复计算多次
```

所以需要把已经计算过的储存起来，计算之前先判断有没有计算过，没计算过再计算，修改程序为：

```py
import time

def code_time(func):
    '''
    修饰器，用来打印函数运行时间
    :param func:
    :return:
    '''
    start_time = time.time()
    def closer(*args,**kwargs):
        result = func(*args,**kwargs)
        codeTime = time.time() - start_time
        print(f"This code runs at:{codeTime}")
        return result
    return closer
resultList = {0:1,1:1}
def _Fibonacci(n):
    if n <= 1:
        return 1
    else:
        if n-1 in resultList:
            a = resultList[n-1]
        else:
            a = _Fibonacci(n-1)
            resultList[n-1] = a
        if n-2 in resultList:
            b = resultList[n-2]
        else:
            b = _Fibonacci(n-2)
            resultList[n-2] = b
        return a + b

@code_time
def Fibonacci(n):
    return _Fibonacci(n)


if __name__ == '__main__':
    var = Fibonacci(40)
    print(var)

    # This code runs at:0.0
    # 165580141
```

速度快了很多，但重复的代码是不能忍受的，使用修饰器重新一下：

```py
import time


def code_time(func):
    start_time = time.time()

    def closer(*args, **kwargs):
        result = func(*args, **kwargs)
        codeTime = time.time() - start_time
        print(f"This code runs at:{codeTime}")
        return result

    return closer


def modify(func):
    catch = {0: 1, 1: 1}

    def closer(*args):
        if args not in catch:
            catch[args] = func(*args)
        return catch[args]
    return closer


@modify
def _Fibonacci(n):
    if n <= 1:
        return 1
    else:
        return _Fibonacci(n - 1) + _Fibonacci(n - 2)


@code_time
def Fibonacci(n):
    return _Fibonacci(n)


if __name__ == '__main__':
    var = Fibonacci(40)
    print(var)

```

有20节楼梯，一次可以走1，2，3，4级，总共有多少种走法

```py
from my_python_package import code_time


def Modify(c = None):
    if c == None:
        c = {}
    def modify(func):
        catch = c
        def closer(*args):
            if args[0] not in catch:
                catch[args[0]] = func(*args)
            return catch[args[0]]
        return closer
    return modify

@Modify()
def _Stairs(num, steps):
    count = 0
    if num == 0:
        count = 1
    elif num > 0:
        for step in steps:
            count += _Stairs(num-step,steps)
    return count

@code_time
def Stairs(num,steps):
   count = _Stairs(num,steps)
   return count

if __name__ == '__main__':
    num = 20
    steps = [step for step in range(1,5)]
    count = Stairs(num, steps)
    print(count)

    # Stairs runs at: 0.0 s
    # 283953
```

### 9.3 总结

* 闭包：内部函数调用了外部函数作用域内的变量
  * 针对函数
  * 要有自由变量（私有变量）
  * 要点：内部函数要跳出外部函数的生命周期，需要外部函数把他return出来

* 装饰器：
  * 基础：闭包
  * 作用：不修改原来代码的基础上拓展原函数功能
  * 用处：修改API功能，AOP编程
  * 要点：@语法糖，函数执行顺序

* 参考链接

[Python高级编程技巧（进阶）(已完结)](https://www.bilibili.com/video/av56768464/?p=38&t=447)

[Python的闭包与装饰器](https://www.bilibili.com/video/av18586448?t=1917)

## DAY 10. 鸭子类型

这个概念来源于美国印第安纳州的诗人詹姆斯·惠特科姆·莱利（James Whitcomb Riley,1849-1916）的诗句：”When I see a bird that walks like a duck and swims like a duck and quacks like a duck, I call that bird a duck.”

> 当我看到一只像鸭子一样走路，像鸭子一样游泳，像鸭子一样嘎嘎叫的鸟，我就叫它鸭子。

鸭子类型在动态编译语言如python，go中经常使用，意思是程序只关心对象行为而不关心对象类型，如

```py
class Duck:
    def __init__(self, name):
        self._name = name

    def call(self):
        print("gua gua gua")

class Frog:
    def __init__(self, name):
        self._name = name

    def call(self):
        print("gua gua gua")

def quack(duck):
    duck.call()

if __name__ == '__main__':
    duck = Duck('Duck')
    frog = Frog('Frog')
    quack(duck)
    quack(frog)
```

虽然duck和frog不是同一个类型，但他们都有相同的方法call，那就可以把他们“当作同一种类型——鸭子类型”

## 前十天总结

* 函数的参数传递
  * 可变类型传引用，不可变类型传值
* 元类
  * 元类是所有类的类，所有类由元类实例化而来
  * 创建类的两种方法
    * class关键字，底层调用type()函数
    * type函数，接受三个参数，类名，基类元组，属性方法的字典
  * MetaClass
    * 如果在使用class关键字声明类的时候指定metaclass，则会根据指定的类实例化新类，自定义的MetaClass继承自type，需要重写`__new__(mcs,name,base,namespace)`方法，与type的变量和用法一致
    * 用来控制类的创建行为
* 静态方法和类方法
  * 静态方法
    * 使用修饰器`@staticmethod`修饰
    * 不操作类中的属性和方法
    * 不会传递隐式参数
    * 只占用类的命名空间，与类无太大联系
    * 可以被类或对象调用
  * 实例方法
    * 第一个参数默认是self，指向实例对象，只能被实例对象调用
    * `.`语法糖，会把调用方法的对象作为第一个参数self传递
  * 类方法
    * 使用修饰器`@classmethod`修饰
    * 第一个参数为`cls`
    * 多用来操作类属性
    * 可以被类或方法调用
    * 类方法修改示例属性无效
    * `.`语法糖，无论使用类名调用还是使用对象名调用，都会把类作为第一个参数传递
* 类变量和实例变量
  * 类变量
    * 在所有示例之间共享
    * 只保留一份
    * 在类体中定义
    * 只能通过类修改，实例对象修改无效
  * 实例变量
    * 各示例对象保留自己的实例变量，互不影响
    * 为实例对象添加实例变量`对象名.实例变量名 = value`,不要和用对象修改类属性混淆
    * 类修改某个对象的实例属性无效
    * 在构造函数中定义
* python自省
  * 在运行过程中能知道对象类型的能力
  * help():获取对象详细说明
  * dir():获取对象所有属性和方法
  * type(object):只传递一个参数时返回对象的类型
  * hasattr():判断对象有没有特点属性，调用getattr()捕获异常实现
  * getattr(object,name,default):获取对象特定属性，object为对象，name为特定属性,default为找不到时返回值，不指定default找不到抛出AttributeError
  * setattr(x,y,v):给对象添加一个属性，等价于x.y=v
  * isinstance(object,class):判断一个对象是不是某个类的实例，考虑继承
  * issubclass(class1,class2):判断一个类是不是另一个类的子类
  * id()：返回地址值
  * callable():判断是否可调用
* 生成式,迭代器，生成器
  * 列表生成式`mylist = [i for i in range(10) if i % 2 != 0]`
  * 字典生成式`mydict = {K:V for k,v in dict.items() if v > 10}`
  * 集合生成式`myset = {i for i in range(10) if i % 2 == 0}`
  * 生成器：类似函数，可迭代，return变为yield
  * 迭代器：可以被next()函数调用并不断返回下一个值的对象，表示数据流，没有数据时抛出StopIteration异常
  * 可迭代对象：可直接作用于for循环的对象
  * 生成器都是迭代器，list，dir等只是可迭代对象，不是迭代器
* 格式化字符串的三种方法
  * %
  * format()
  * f-string
  * 格式规范迷你语言
* `*args`和`**kwargs`
  * `*args`：多值元组
  * `**kwargs`：多值字典
  * 序列解包
* 闭包和装饰器
  * 闭包：内部函数使用了外部函数作用域内的参数
  * 装饰器
    * 本质：闭包
    * 参数：外层函数必须接受被修饰函数作为参数，也只能接受一个参数
    * 返回值：外层函数返回闭包函数，闭包函数返回被修饰函数的调用
    * 装饰器带参数：在原来装饰器基础上外加一层函数，接受装饰器参数，返回外层函数
    * 被修饰函数带参数：参数传递给闭包函数
    * `@`语法糖：自动传递被修饰函数，隐式函数调用
    * 修饰器函数的执行顺序：注意隐式的调用
* 鸭子类型
  * 只关心对象的行为而不关心对象类型

## DAY 11. python 重载

函数重载是指允许定义参数数量或类型不同的同名函数，程序在运行时会根据所传递的参数类型选择应该调用的函数
，但在默认情况下，python是不支持函数重载的，定义同名函数会发生覆盖

```py
def foo(a:int):
    print(f'int {a}')

def foo(b:list):
    print(f'list{b}')

foo(3)
foo([i for i in range(3)])

# list3
# list[0, 1, 2]
```

至于不支持的原因，我想大概是没必要，首先，只在两种情况下可能发生函数重载，一是参数类型不同，二是参数个数不同，对于第一种情况，鸭子类型的存在使得函数不在乎参数类型而只关心参数的行为，所以你可以传递任何类型的参数，对于第二种情况，缺省参数的使用使得可以传递任意多个参数，因此函数的重载在python中就显得很鸡肋了，但如果非要实现函数重载，可以使用3.4中增加的转发机制即单分派泛型函数（single-dispatch generic function）来实现重载

### 11.2 单分派泛型函数

* 泛型函数 generic function ：由多个函数组成的函数，可以根据不同的参数类型决定调用那个函数
* 单分派，single-dispatch：一种泛型函数分派形式，其中实现是根据单个参数的类型选择的。

所以，单分派泛型函数就是根据函数的第一个参数类型决定使用哪个函数的泛型函数

将一个函数声明为泛型函数可以使用修饰器`@singledispatch`,需要从`functools`模块导入，singledispatch有两个常用方法，register和dispatch

```py
from functools import singledispatch

@singledispatch
def Foo(arg,*args):
    print(arg)
```

这样就实现了一个泛型函数，他的分派发生在第一个参数类型上，如果想要基于此实现重载，需要使用他的register方法，

```py
from functools import singledispatch

@singledispatch
def Foo(arg,*args):
    print(arg)

# 使用了类型注释
@Foo.register
def _1(arg:int,*args):
    print(f'int - {arg}')

# 没有使用类型注释，显式传递给修饰器
@Foo.register(list)
def _2(arg,*args):
    print(f'list - {arg}')

if __name__ == '__main__':
    Foo(3)  # int - 3
    Foo([i for i in range(10)])  # list - [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

对于使用了类型注释的变量，singledispatch会自动推断第一个参数的类型，如上面int的那个，对于没有使用类型注释的变量，可以显式传递类型给singledispatch，如下面list的那个

register属性还可以以函数的形式调用，这可以用在lambdas表达式上，如

```py
>>> def nothing(arg, verbose=False):
...     print("Nothing.")
...
>>> fun.register(type(None), nothing)
```

如果没有实现针对特定类型的注册，那么就会使用被@singledispatch修饰的函数

```py
Foo("string")  # string
```

要检查泛型函数将为给定类型选择哪个实现，请使用dispatch()属性

```py
print(Foo.dispatch(int))  # <function _1 at 0x000001D7C2724B70>
print(Foo.dispatch(list))  # <function _2 at 0x000001D7C2792E18>
print(Foo.dispatch(str))  # <function Foo at 0x000001FB456FC268>
```

要访问所有已注册的实现，请使用只读的registry属性

### 11.3 总结

python默认不支持重载，但可以使用单分派泛型函数实现，声明泛型函数需要使用修饰器@singledispatch，它有三个属性，register用来注册针对特定类型的“重载函数”,这里必须指明针对的是哪一个特定的类型，可以给第一个参数类型注释，也可以给register传入一个显式类型，否则会抛出TypeError异常;dispatch属性用来查看特定的类型将要选择的函数;registry用来访问所有已注册的实现。

参考链接：

[functools.singledispatch](https://docs.python.org/3.7/library/functools.html#functools.singledispatch)

[single dispatch](https://docs.python.org/3.7/glossary.html#term-single-dispatch)

[generic function](https://docs.python.org/3.7/glossary.html#term-generic-function)

[python中的重载](https://blog.csdn.net/qq_37049781/article/details/83959365)

[为什么 Python 不支持函数重载？其他函数大部分都支持的？](https://www.zhihu.com/question/20053359)

## DAY 12. python新式类和旧式类

继承自object基类的类叫做新式类，否则叫做旧式类，python3中的类默认是新式类，之前版本默认是旧式类

```python
root@kail:~# python
python 2.7.15 (default,Jul 28 2018,11:29:29)
[GCC 8.1.0] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> class A():
...     pass
...
>>> a=A()
>>> dir(a)
['__doc__','__module__']
```

如上，在python2中定义一个类，不继承任何基类，内建属性只有两个，这就是旧式类，如果想要创建一个新式类，需要显式的继承object基类，如：

```python
root@kail:~# python
python 2.7.15 (default,Jul 28 2018,11:29:29)
[GCC 8.1.0] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> class A(object):
...     pass
...
>>> dir(A)
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__']
```

新式类默认有很多属性，都是从object基类中继承过来的，而在python3中所有类默认继承object基类

```py
Python 3.7.0 (v3.7.0:1bf9cc5093, Jun 27 2018, 04:59:51) [MSC v.1914 64 bit (AMD64)] on win32
Type "copyright", "credits" or "license()" for more information.
>>> class A:
        pass
>>> dir(A)
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__']
>>>
```

每个属性的具体用法参见[Python——特殊属性与方法](https://www.cnblogs.com/Security-Darren/p/4604942.html)

### C3算法
