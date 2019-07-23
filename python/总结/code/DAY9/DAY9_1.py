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