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

### 总结

python有两种数据类型，可变和不可变数据，对于可变数据类型，诸如列表，字典，集合在函数传参时**传引用**，对于不可变数据类型，如数值，字符，元组，在函数传参时**传值**，但更准确的来说，python函数传参时使用**传对象引用**的方式，如果函数收到的是一个可变对象（比如字典或者列表）的引用，就能修改对象的原始值－－相当于通过“传引用”来传递对象。如果函数收到的是一个不可变对象（比如数字、字符或者元组）的引用，就不能直接修改原始对象－－相当于通过“传值'来传递对象。

最后还是要注意像元组中数据是可变类型的情况

[参考链接1](https://github.com/taizilongxu/interview_python#1-python%E7%9A%84%E5%87%BD%E6%95%B0%E5%8F%82%E6%95%B0%E4%BC%A0%E9%80%92)
[参考链接2](https://www.cnblogs.com/loleina/p/5276918.html)

## DAY 2 元类

### 1. 元类是什么

众所周知，对象由类实例化而来，类是对象的模板，而python一切皆对象，类也是对象，它由元类（type）创建，所以**元类是类的类**，是类的模板

### 2. 创建类的另一种方法

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

### 3. MetaClass

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

### 4. 总结

* 通过class定义的类其实是通过type()创建的
* type(object_or_name, bases, dict)
* 如果想要控制类的创建行为，需要在创建类时指定metaclass,一旦指定了metaclass，就会在class上添加`__metaclass__`，创建类时会找`__metaclass__`指向的类，并用这个类创建类，如果找不到，就会调用默认的type()

参考文章

[Python中的元类(metaclass)](https://github.com/taizilongxu/interview_python#2-python%E4%B8%AD%E7%9A%84%E5%85%83%E7%B1%BBmetaclass)
[谈谈Python中元类Metaclass(一)：什么是元类](https://www.cnblogs.com/ArsenalfanInECNU/p/9036407.html)
[Python之元类](https://www.cnblogs.com/tootooman/p/9225626.html)
