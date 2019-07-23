from my_python_package import code_time

resultList = {0: 1, 1: 1}

def _Fibonacci(n):
    if n <= 1:
        return 1
    else:
        if n-1 in resultList:
            a = resultList[n-1]
        else:
            a = _Fibonacci(n-1)
            resultList[n-1] = a
        if n-2 in resultList:
            b = resultList[n-2]
        else:
            b = _Fibonacci(n-2)
            resultList[n-2] = b
        return a + b

@code_time
def Fibonacci(n):
    return _Fibonacci(n)


if __name__ == '__main__':
    var = Fibonacci(40)
    print(var)