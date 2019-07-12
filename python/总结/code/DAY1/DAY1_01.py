def Demo(a):
    a[0].append(3)
    print("value = " + str(a) + "address = " + str(id(a)))

if __name__ == '__main__':
    a = ([1,2], 2)
    print("value = " + str(a) + "address = " + str(id(a)))  # value = ([1, 2], 2)address = 2616967970056
    Demo(a)  # value = ([1, 2, 3], 2)address = 2616967970056
    print("value = " + str(a) + "address = " + str(id(a)))  # value = ([1, 2, 3], 2)address = 2616967970056
