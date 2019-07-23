from my_python_package import code_time
def Modify(c = None):
    if c == None:
        c = {}
    def modify(func):
        catch = c
        def closer(*args):
            if args[0] not in catch:
                catch[args[0]] = func(*args)
            return catch[args[0]]
        return closer
    return modify


@Modify({0: 1, 1: 1})
def _Fibonacci(n):
    if n <= 1:
        return 1
    else:
        return _Fibonacci(n - 1) + _Fibonacci(n - 2)


@code_time
def Fibonacci(n):
    return _Fibonacci(n)


if __name__ == '__main__':
    var = Fibonacci(40)
    print(var)
