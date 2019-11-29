import sympy

x = sympy.Symbol('x')


class NewtonIteration:
    """
    非线性方程——牛顿迭代法
    x|(k + 1) = x|(k) - f(x|(k)) / f'(x|(k))
    """
    def __init__(self, function: str, x0: float, deviation: float, n: int):
        self.x0 = x0
        self.deviation = deviation
        self.N = n
        self.function = eval(function)
        self.derivative = sympy.diff(self.function, x)

    def computer_fx_value(self, value: float) -> float:
        """
        计算f(x)的值
        :param value: 自变量取值
        :return: float
        """
        return self.function.evalf(subs={x: value})

    def computer_fx_der_value(self, value: float) -> float:
        """
        计算f(x) 的一阶导数值
        :param value: 自变量取值
        :return: float
        """
        return self.derivative.evalf(subs={x: value})

    def computer(self):
        index = 0
        while True:
            assert index < self.N
            x1 = self.x0 - self.computer_fx_value(self.x0) / self.computer_fx_der_value(self.x0)
            if abs(x1 - self.x0) < self.deviation:
                return x1
            self.x0 = x1
            index += 1


def run():
    function = input("请输入迭代函数：")
    x0 = float(input("请输入初值x0："))
    deviation = float(input("请输入允许误差: "))
    n = int(input("请输入允许迭代的最大次数："))
    newton = NewtonIteration(function, x0, deviation, n)
    try:
        return newton.computer()
    except AssertionError:
        print("在允许误差范围内超出最大迭代次数!!!!")


if __name__ == '__main__':
    print(run())
