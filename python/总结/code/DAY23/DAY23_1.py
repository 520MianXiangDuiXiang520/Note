class Demo:
    def __init__(self):
        print("init")

    def __enter__(self):
        print("enter")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(exc_type, exc_val, exc_tb)
        print("exit")
        return True


if __name__ == '__main__':
    demo = Demo()
    with demo as d:
        print(d)
        raise IOError("主动抛出异常")
        print("with")
