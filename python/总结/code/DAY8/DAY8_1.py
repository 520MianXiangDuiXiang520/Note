def output(*args, **kwargs):
    print(args)
    print(kwargs)

output('zhangsan', 'lisi', 5, 6,a=1,b=2,c=3)

# ('zhangsan', 'lisi', 5, 6)
# {'a': 1, 'b': 2, 'c': 3}

mylist = ['aardvark', 'baboon', 'cat']

def put(a, b, c):
    print(f'a={a},b={b},c={c}')

put(*mylist)  # a=aardvark,b=baboon,c=cat

s = {'a': 1, 'b': 2, 'c': 3}
put(**s)