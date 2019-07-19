# l = [i for i in range(10) if i > 5]
# print(l)
# dict = {
#     'zhangsan': 10,
#     'lisi': 12,
#     'wangwu': 18
# }
# dict = {k:v for v,k in dict.items() if k >= 12}
# print(dict)
# s = {i for i in range(100) if i % 2 != 0}
# print(s)
# t = (i for i in range(10) if i % 2 == 0)
# print(t)  # <generator object <genexpr> at 0x000001F17ED14C00>
# print(list(t))
# print(set(t))  # {0, 2, 4, 6, 8}
import time
starttime = time.time()
# feibo = [1, 1]
# for i in range(2,10000):
#     feibo.append(feibo[i - 1] + feibo[i - 2])
# print(feibo)
# def feb(f, s, max):
#     i = 0
#     while i < max:
#         f, s = s, f + s
#         i += 1
#         yield s
#
# for i in feb(1, 1, 100):
#     print(i)
# print("用时："+str(time.time() - starttime))  # 用时：0.52858567237854

# def Demo():
# #     print(1)
# #     yield 1
# #     print(2)
# #     yield 2
# #     print(3)
# #     yield 3
# #
# # for i in Demo():
# #     i

t = (i for i in range(100) if i % 2 == 0)
# for i in t:
#     print(i)
# 或
while(True):
    try:
        next(t)
    except StopIteration:
        break