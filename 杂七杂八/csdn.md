# CSDN 面试题

* 执行以下代码的结果是：

```py
list = [1, 2, 3]
list.append(4) + list('abc')
```

答案：**报错**  

首先会执行append()函数，返回值是None，相当于`None + list("abc")`,会报一个TypeError  
其次list已经是一个列表了，使用list()不会把字符串转换为列表，会报 `TypeError: 'list' object is not callable`

* 执行以下代码的结果是

```py
url = 'julyedu.ai'
url[-3:-1] = '.com'
```

答案：**报错**

string是一种不可变数据类型，会报`TypeError: 'str' object does not support item assignment`,可以用`url = url[:-3] + ".com" + url[-1]`
