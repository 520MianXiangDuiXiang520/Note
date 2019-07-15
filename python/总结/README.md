# python 重要知识点总结

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
