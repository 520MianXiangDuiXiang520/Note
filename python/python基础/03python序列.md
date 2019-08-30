<!--961032830987546d0e6d54829fc886f6-->

目录(Catalo)

* [python序列](#python%E5%BA%8F%E5%88%97)
  * [列表](#%E5%88%97%E8%A1%A8)
    * [1.常用方法](#1.%E5%B8%B8%E7%94%A8%E6%96%B9%E6%B3%95)
      * [1.1 增加元素](#1.1%20%E5%A2%9E%E5%8A%A0%E5%85%83%E7%B4%A0)
      * [1.2 删除元素](#1.2%20%E5%88%A0%E9%99%A4%E5%85%83%E7%B4%A0)
      * [1.3 排序](#1.3%20%E6%8E%92%E5%BA%8F)
      * [1.4 查找](#1.4%20%E6%9F%A5%E6%89%BE)
      * [1.5其他](#1.5%E5%85%B6%E4%BB%96)
    * [2. 列表推导式](#2.%20%E5%88%97%E8%A1%A8%E6%8E%A8%E5%AF%BC%E5%BC%8F)
    * [3. 切片](#3.%20%E5%88%87%E7%89%87)
  * [元组](#%E5%85%83%E7%BB%84)
    * [1.生成器推导式](#1.%E7%94%9F%E6%88%90%E5%99%A8%E6%8E%A8%E5%AF%BC%E5%BC%8F)
  * [字典](#%E5%AD%97%E5%85%B8)
    * [1.常用方法](#1.%E5%B8%B8%E7%94%A8%E6%96%B9%E6%B3%95)
  * [集合](#%E9%9B%86%E5%90%88)
    * [1.集合操作](#1.%E9%9B%86%E5%90%88%E6%93%8D%E4%BD%9C)
    * [2.集合运算](#2.%E9%9B%86%E5%90%88%E8%BF%90%E7%AE%97)
    * [3. 集合推导式](#3.%20%E9%9B%86%E5%90%88%E6%8E%A8%E5%AF%BC%E5%BC%8F)
  * [序列解包](#%E5%BA%8F%E5%88%97%E8%A7%A3%E5%8C%85)

<!--a46263f7a69f33f39fc26f907cdb773a-->
# python序列

## 列表

python变量不存放值，之存放值的引用，所以列表中元素可以是不同类型

### 1.常用方法

#### 1.1 增加元素

* append,在末尾插入元素
* extend，将一个列表整体插入到尾部
* insert，将某个元素插入到特定位
* +/*，拼合或拼合多个元素，该操作不是原地操作，会创建新地址

* 上三个都是原地操作，在源地址上增删查改，最后两个会新开辟一个地址

#### 1.2 删除元素

* del，删除对象，用在所有对象上，删除的元素会在合适时间被回收，可以`gc.collect()`立即回收
* remove，从列表里移除某个值与特定值相等的元素
* pop，从列表里移除某个特定位置的元素，并返回该元素
* clear，清空列表中所有元素，但保留列表自身对象

#### 1.3 排序

* sort：按指定规则对元素排序，默认规则是比较元素大小
* reverse：按制定规则逆序排序
* sorted：sort异地排序
* reversed：reverse异地排序

* 前两个在原来基础上排，后两个返回新对象

#### 1.4 查找

* count
* index:返回元素在列表中首次出现的位置

#### 1.5其他

* zip：将多个列表中的元素重新组合为元组，并返回包含这些元组的zip对象
* enumerate：返回包含下标和值的迭代对象，可用来判断一个对象是否是迭代对象
* map():将一个函数依次作用到序列或迭代器对象的每个元素上，并返回map对象
* reduce():接受两个函数的参数，并从左到右把这两个函数依次作用在迭代对象的每个元素上，在functools标准库中

```python
>>> a=[1,2,3,4]
>>> b=[5,6,7]
>>> ab=zip(a,b)
>>> ab
<zip object at 0x0000028A50A61608>
>>> list(ab)
[(1, 5), (2, 6), (3, 7)]
>>> en=enumerate(a)
>>> en
<enumerate object at 0x0000028A50A6BC60>
>>> list(en)
[(0, 1), (1, 2), (2, 3), (3, 4)]
>>>
```

zip两个列表的元素个数不同时以短的为准，里面的参数是可迭代对象

map：

```python
>>> def fun(a):
	return a+5

>>> a=map(fun,range(5))
>>> a
<map object at 0x0000019F517923C8>
>>> list(a)
[5, 6, 7, 8, 9]
>>>
```

也可以是多参数函数，返回的map对象中的所有元素都是经过函数处理过后的，但map不会对迭代对象做修改

```python
>>> z=zip(a,range(10))
>>> z
<zip object at 0x0000028A50A08748>
>>> list(z)
[(1, 0), (2, 1), (3, 2), (4, 3)]
>>> z=zip(a,"1"*11)
>>> list(z)
[(1, '1'), (2, '1'), (3, '1'), (4, '1')]
```

### 2. 列表推导式

```python
[表达式 for 变量 in 序列或迭代对象]
```

可以嵌套多重循环，也可以使用判断

例：

```python
j=[1,3,2]
ss=[s*2 for s in j]
print(ss)

# 输出：[2, 6, 4]
```

* 使用推导式平铺嵌套列表

```python
a=[[a for a in range(3)]]*3
print(a)
s=[j for i in a for j in i]
print(s)

# 输出
# [[0, 1, 2], [0, 1, 2], [0, 1, 2]]
# [0, 1, 2, 0, 1, 2, 0, 1, 2]
```

* 写一个列表生成式，产生一个公差为11的等差数列

```python
    def 等差数列(self,begin,num):
        l=[begin+11*a for a in range(num) ]
        print(l)
```

* 在一个字典中找出最大值

```python
    def 成绩最好(self):
        dir={'zhangsan':95,'lisi':59,'wangwu':78,'zhaoliu':87,'xiaohua':100}
        max_score=max(dir.values())
        max_name=[max_name for max_name in dir if dir[max_name]==max_score]
        print(max_name)
```

* 矩阵转置

```python
 def 矩阵转置(self):
        l=[[1,2,3],[4,5,6],[7,8,9]]
        s=[[r[i] for r in l] for i in range(3)]
        print(s)
```

### 3. 切片

由两个冒号，三个数字组成，三个数字分别是起始，终止，步长，切片可以用在列表，元组，字符串等上

使用切片可以实现浅复制，修改值等操作。

## 元组

元组不能修改，比较安全，访问速度比列表快(tuple)

### 1.生成器推导式

```python
(表达式 for 变量 in 迭代器)
```

生成器推导式形式与列表推导式类似，但生成器推导式返回一个生成器对象，生成器对象用完即销毁,生成器对象需要转换成列表或元组等数据类型才能使用，也可以通过生成器对象的`__next__`属性访问，生成器对象具有惰性求值的特点，只在需要的时候才返回元素，因此比列表推导式效率高，适合大量数据的遍历。

```python
>>> s=(a for a in range(5))
>>> s
<generator object <genexpr> at 0x00000135FDE62C00>
>>> list(s)
[0, 1, 2, 3, 4]
>>> list(s)
[]
>>> s=(a for a in range(5))
>>> tuple(s)
(0, 1, 2, 3, 4)
>>>
```

## 字典

字典是一种无序可变序列，键是不可变类型，值是可变类型，字典访问速度也比列表快

### 1.常用方法

* dict :创建字典
* update： 将一个字典添加到另一个字典中
* pop：删除，并返回给定键对应的值
* popitem：随机弹出一个元素，返回元素
* del
* clear
* copy
* setdefault：查询字典中的元素，不存在就添加一个
* get：查询，不存在允许输出特定值
* items：返回字典中的元素
* key：返回键的列表
* value：返回值的列表

```python
>>> key=['name','id']
>>> value=['zhangsan',11]
>>> s=dict(zip(key,value))
>>> s
{'name': 'zhangsan', 'id': 11}
>>> s2={'sex':'boy'}
>>> s.update(s2)
>>> s
{'name': 'zhangsan', 'id': 11, 'sex': 'boy'}
>>> s.pop
<built-in method pop of dict object at 0x00000135FDE0F288>
>>> s.pop('name')
'zhangsan'
>>> s
{'id': 11, 'sex': 'boy'}
>>> s.popitem()
('sex', 'boy')
>>> s
{'id': 11}
>>> s.get('name','No This Key')
'No This Key'
>>> s.setdefault('name','No This Key')
'No This Key'
>>> s
{'id': 11, 'name': 'No This Key'}
```

## 集合

集合只支持元组等**可哈希数据**，列表，字典等可变类型不能成为集合中的元素，可以使用函数`hash()`判断是否是可哈希数据，字典和集合使用哈希表存储数据，所以操作速度高于列表等。(set)

### 1.集合操作

* add()
* update()
* pop():随即删除并返回一个元素，不存在抛出异常
* remove()：删除一个特点元素，元素不存在抛出异常
* discard()：删除一个特定元素，不存在就忽视该操作
* clear()：删除几何中所有元素

```python
>>> s={1,2,3,4,5}
>>> s.pop()
1
>>> s
{2, 3, 4, 5}
>>> s.remove(0)
Traceback (most recent call last):
  File "<pyshell#53>", line 1, in <module>
    s.remove(0)
KeyError: 0
>>> s.remove(2)
>>> s
{3, 4, 5}
>>> s.discard(0)
>>> s
{3, 4, 5}
>>>
```

### 2.集合运算

* 交：&
* 并：|
* 差：-
* 对称差：^
* 比较:> < <= >= 用来判断并包关系，不是比较大小

### 3. 集合推导式

```python
{表达式 for 变量 in 迭代器}
```

如：

```python
>>> import random
>>> s={random.randint(1,500) for i in range(20)}
>>> s
{1, 387, 268, 411, 293, 167, 48, 53, 441, 187, 191, 195, 324, 465, 473, 474, 481, 362, 114, 123}
>>> len(s)
20
>>> s={random.randint(1,5) for i in range(20)}
>>> s
{1, 2, 3, 4, 5}
>>>
```

集合不允许元素重复，所以可以利用这一特性实现去重。

## 序列解包

```python
>>> x,y,z=1,2,3
>>> p=(2,3,4)
>>> (x,y,z)=p
>>> p
(2, 3, 4)
>>> p=map(str,range(3))
>>> p
<map object at 0x000001BB8B842320>
>>> list(p)
['0', '1', '2']
```