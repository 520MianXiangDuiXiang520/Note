def GetTwoInts():
    x = input()
    x, y = x.split(" ")
    return int(x), int(y)
x, y = GetTwoInts()
print(x + y)
