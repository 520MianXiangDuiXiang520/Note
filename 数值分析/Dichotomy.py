import math
from sys import exit


class Dichotomy:

    def __init__(self, start: float, end: float, allowable_error: float, function: str):
        """
        :param start: float 区间起点
        :param end: float 区间终点
        :param allowable_error: float 允许误差
        :param function: str 函数表达式，必须是python可以直接执行的
        """
        self.start = start
        self.end = end
        self.allowable_error = allowable_error
        self.function = function

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

    def calculate_the_value_of_midpoint(self) -> float:
        """
        计算f(x)在区间[a,b]中点的值f((a+b)/2)
        :return: float
        """
        midpoint = (self.start + self.end) / 2
        value = self.calculation_function_value(midpoint)
        return value

    def judge(self):
        """
        判断： 若f((a+b)/2) * f(a) > 0,则根位于区间 [(a+b)/2, b]中
        以 （a+b）/2 代替a, 否则，以(a+b)/2 代替b
        :return: None
        """
        # 判断
        value_midpoint = self.calculate_the_value_of_midpoint()
        fa = self.calculation_function_value(self.start)
        if fa * value_midpoint > 0:
            self.start = (self.start + self.end) / 2
        else:
            self.end = (self.start + self.end) / 2


def run():
    function = str(input("请输入函数表达式（python math支持,未知量用x表示，如【1-x-math.sin(x)】）："))
    start = float(input("请输入区间起点："))
    end = float(input("请输入区间终点："))
    error = float(input("请输入允许误差："))
    calcu = Dichotomy(start, end, error, function)
    while True:
        calcu.judge()
        cha = calcu.end - calcu.start
        if cha < calcu.allowable_error:
            result = (calcu.start + calcu.end) / 2
            print(result)
            return 0


if __name__ == '__main__':
    run()
