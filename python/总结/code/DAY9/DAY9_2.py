def func1(func):
    def func2():
        print("func2")
        return func()
    return func2


# @func1
def Demo():
    print("Demo")


if __name__ == '__main__':
    # s = Demo()
    s = func1(Demo)
    s()
    print(s)
