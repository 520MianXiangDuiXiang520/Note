def Febo(n):
    n0 = 0
    n1 = 1
    for i in range(n):
        n0, n1 = n1, n0 + n1
        sum = yield n1
        print("------------", sum)
    return sum

if __name__ == '__main__':
    f = Febo(100)
    print(next(f))
    print(f.send(12))
    print(f.send(12))
    print(f.send(12))
    print(f.send(12))
