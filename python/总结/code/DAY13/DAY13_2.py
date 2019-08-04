def singleton(cls):
    singleton_dict = {}
    def close(*args, **kwargs):
        return singleton_dict.setdefault('obj',cls(*args, **kwargs))
    return close

@singleton
class MyClass:
    pass

if __name__ == '__main__':
    foo1 = MyClass()
    foo2 = MyClass()
    print(foo1)  # <__main__.MyClass object at 0x000001DF618C8940>
    print(foo2)  # <__main__.MyClass object at 0x000001DF618C8940>