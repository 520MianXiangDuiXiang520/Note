# 循环引用

a = []
b = []

a.append(b)
b.append(a)