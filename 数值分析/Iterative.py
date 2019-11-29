import math
"""
迭代法
"""


class ComputerException(Exception):
    pass


class Iterative:
    def __init__(self, function: str, x0: float, deviation: float, n: int):
        self.function = function
        self.x0 = x0
        self.deviation = deviation
        self.N = n

    def calculation_function_value(self, x: float) -> float:
        """
        计算函数表达式，开始输入的表达式中必须含有x
        :param x: 函数自变量，输入的表达式通过eval转换为可执行语句
        :return: float
        """
        try:
            result = eval(self.function)
            return result
        except NameError:
            print("函数表达式有误")
            exit()

    def judge(self):
        index = 0
        while True:
            assert index < self.N
            x1 = self.calculation_function_value(self.x0)
            if abs(x1 - self.x0) < self.deviation:
                return x1
            self.x0 = x1
            index += 1


def run():
    function = input("请输入迭代函数：")
    x0 = float(input("请输入初值x0："))
    deviation = float(input("请输入允许误差: "))
    n = int(input("请输入允许迭代的最大次数："))
    iterative = Iterative(function, x0, deviation, n)
    try:
        print(iterative.judge())
    except AssertionError:
        print('在允许误差范围内超出最大迭代次数！！！')


if __name__ == '__main__':
    run()

