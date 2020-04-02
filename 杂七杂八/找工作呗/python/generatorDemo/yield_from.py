# yield from 可以在子生成器与调用者之间架设双向通信的桥梁
def child():
    # 子生成器
    result = yield 0
    print(result)
    result = yield 1
    print(result)
    while True:
        result = yield 2
        print(result)
    # return 3


def delegator(gen):
    # 委托生成器
    while True:
        result = yield from gen
        print(f"委托：{result}")


def transfer():
    # 调用方
    d = delegator(child())
    result = d.send(None)
    print(result)
    for i in range(5):
        print(d.send("hello"))


def my_chain(*args, **kwargs):
    for i in args:
        yield from i


if __name__ == '__main__':
    transfer()
    for i in my_chain([1, 2, "11"], {"a": 2, "b": 3}, range(10)):
        print(i, end=" ")
