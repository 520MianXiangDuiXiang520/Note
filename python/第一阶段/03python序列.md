# python序列

## 列表

python变量不存放值，之存放值的引用，所以列表中元素可以是不同类型

## 1.常用方法

### 1.1 增加元素

* append,在末尾插入元素
* extend，将一个列表整体插入到尾部
* insert，将某个元素插入到特定位
* +/*，拼合或拼合多个元素，该操作不是原地操作，会创建新地址

* 上三个都是原地操作，在源地址上增删查改，最后两个会新开辟一个地址

### 1.2 删除元素

* del，删除对象，用在所有对象上
* remove，从列表里移除某个元素
* pop，从列表里移除某个元素，并返回该元素
* clear，清空列表中所有元素，但保留列表自身对象

### 1.3 排序

* sort
* reverse
* sorted
* reversed

### 1.4 查找

* count
* index

## 2. 列表推导式

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

## 3. 切片

由两个冒号，三个数字组成，三个数字分别是起始，终止，步长，切片可以用在列表，元组，字符串等上

使用切片可以实现浅复制，修改值等操作。

## 元组

元组不能修改，比较安全，访问速度比列表快

### 1.生成器推导式

```python
(表达式 for 变量 in 迭代器)
```

生成器推导式形式与列表推导式类似，但生成器推导式返回一个生成器对象，生成器


## 字典


## 集合