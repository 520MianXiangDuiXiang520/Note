def func1(func):
    def func2(arg):
        arg += 1
        return func(arg)
    return func2

@func1
def Demo(arg):
    print(arg)

if __name__ == '__main__':
    Demo(11)  # 12