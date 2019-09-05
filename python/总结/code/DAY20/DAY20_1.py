import copy

a = ['a', [i for i in range(5)]]

# 引用
quote_a = a
print(id(a))  # 51195656
print(id(quote_a))  # 51195656

print(id(a[0]), id(a[1]))  # 49298528 51195616
print(id(quote_a[0]), id(quote_a[1]))  # 49298528 51195616

quote_a[1].append(6)
print(a)  # ['a', [0, 1, 2, 3, 4, 6]]


# 浅拷贝
copy_a = copy.copy(a)
print(id(a))  # 51195656
print(id(copy_a))  # 51237352

print(id(a[0]), id(a[1]))  # 49298528 51195616
print(id(copy_a[0]), id(copy_a[1]))  # 49298528 51195616

copy_a[1].append(7)
print(a)  # ['a', [0, 1, 2, 3, 4, 6, 7]]


# 深拷贝
deepcopy_a = copy.deepcopy(a)
print(id(a))  # 51195656
print(id(deepcopy_a))  # 51261648

print(id(a[0]), id(a[1]))  # 49298528 51195616
print(id(deepcopy_a[0]), id(deepcopy_a[1]))  # 49298528 51237992

deepcopy_a.append(7)
print(a)  # ['a', [0, 1, 2, 3, 4, 6, 7]]

# 元组中全部是原子对象
t = tuple(i for i in range(10))
deepcopy_p = copy.deepcopy(t)
print(id(t))  # 62247752
print(id(deepcopy_p))  # 62247752


# 为了节约内存，对于完全相同的原子对象，python会把他们指向同一块内存空间
s = "ss"
s2 = "ss"
print(id(s))  # 58542144
print(id(s2))  # 58542144

l = [i for i in range(10)]
l2 = [i for i in range(10)]
print(id(l))  # 57389904
print(id(l2))  # 59167328

# 元组中只包含原子对象，元组会被当作原子对象
p1 = [(1, 2), (3, 4)]
p2 = [(3, 4), (1, 2)]
print(id(p1[0]), id(p2[1]))  # 8499968 8499968
print(id(p1[1]), id(p2[0]))  # 47696312 47696312

# 集合只包含原子对象的情况: 同列表

s = {i for i in range(10)}
s2 = {i for i in range(10)}
print(id(s), id(s2))  # 55475776 55475656
