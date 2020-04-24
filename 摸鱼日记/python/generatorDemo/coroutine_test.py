def builder_demo():
    news = yield 0
    print(f'news:  {news}')
    news1 = yield 1
    print(f'new1: {news1}')
    yield 4
    yield 5
    return 3


if __name__ == '__main__':
    bd = builder_demo()
    # print(next(bd))
    print(bd.send(None))
    # result1 = bd.send("hello")
    # print(result1)
    # result2 = bd.send("hello2")
    # print(result2)
    bd.throw(Exception, TypeError("throw new error"))
    # bd.close()
    print(next(bd))

    # while True:
    #     try:
    #         print(next(bd))
    #     except StopIteration as e:
    #         print(f'result is {e.value}')
    #         break


    # gen = (i for i in range(10))
    # print(type(gen))
    # for i in gen:
    #     print(i, end=" ")
