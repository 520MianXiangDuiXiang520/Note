# def func1(func):
#     def func2():
#         print("func2")
#         return func()
#     return func2

def func1(num):
    def func2(func):
        def func3():
            if num >10:
                print("大于10")
            else:
                print("小于10")
            return func()
        return func3
    return func2


@func1(num=12)
def Demo():
    print("Demo")


if __name__ == '__main__':
    Demo()
    # s = func1(Demo)