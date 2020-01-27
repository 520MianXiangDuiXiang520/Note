def swap(x, y):
    return y, x

x = input()
x, y = x.split(" ")
x, y = swap(x, y)
print(f"{x} {y}")
