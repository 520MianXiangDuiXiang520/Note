import sympy
from sys import exit
from 数值分析.Newton import Newton

x = sympy.Symbol('x')


class NewtonDownHill(Newton):
    """
    非线性方程的解法————牛顿下山法
    牛顿迭代法当初值x0在单根x*领域时， 具有平方收敛速度
    但如果初值x0距离x*较远，收敛速度较慢，牛顿下山法要求迭代过程中所选的初值能够使函数值单调下降
    下山条件：|f(X(k+1)| < |f(x(k))|
    迭代公式：x|(k + 1) = x|(k) - r * f(x|(k)) / f'(x|(k))
    """

    def __init__(self, function: str, x0: float, deviation: float, n: int, downhill_lower: float):
        super().__init__(function, x0, deviation, n)
        self.downhill_factor = 1
        self.downhill_factor_lower_limit = downhill_lower

    def computer_downhill_factor(self):
        """
        计算下山因子
        :return:
        """
        fx0 = self.computer_fx_value(self.x0)
        while True:
            assert self.downhill_factor > self.downhill_factor_lower_limit
            fx1 = self.x0 - self.downhill_factor * (self.computer_fx_value(self.x0) /
                                                    self.computer_fx_der_value(self.x0))
            if abs(fx1) < abs(fx0):
                print(f"下山因子：{self.downhill_factor}")
                return fx1
            self.downhill_factor /= 2

    def computer(self):
        try:
            self.x0 = self.computer_downhill_factor()
        except AssertionError:
            print("不能下山")

        index = 0
        while True:
            assert index < self.N
            x1 = self.x0 - (self.computer_fx_value(self.x0) /
                                                   self.computer_fx_der_value(self.x0))
            if abs(x1 - self.x0) < self.deviation:
                return x1, index
            self.x0 = x1
            index += 1


def run():
    function = input("请输入迭代函数：")
    x0 = float(input("请输入初值x0："))
    deviation = float(input("请输入允许误差: "))
    n = int(input("请输入允许迭代的最大次数："))
    downhill_lower = float(input("请输入下山因子取值下限"))
    newton = NewtonDownHill(function, x0, deviation, n, downhill_lower)
    # newton = NewtonDownHill('x*x*x -x -1', 0.6, 0.001, 100000, 0.0001)
    try:
        return newton.computer()
    except AssertionError:
        print("在允许误差范围内超出最大迭代次数!!!!")
        raise


if __name__ == '__main__':
    result = run()
    print(result[0])
    print(f"迭代{result[1]}次")
