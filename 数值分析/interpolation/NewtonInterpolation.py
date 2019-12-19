# from configparser import Interpolation

from tabulate import tabulate
import sympy
import matplotlib.pyplot as plt

from interpolation.Interpolation import Interpolation

"""
牛顿插值法
"""


class NewtonInterpolation(Interpolation):
    def __init__(self, x: list, y: list):
        super().__init__(x, y)
        self.difference_quotient_table = [[] for _ in range(len(x) + 1)]

    def _get_difference_quotient_table(self):
        """
        获得差商表
        :return:
        """
        self.difference_quotient_table[0].append("xi")
        for j in range(1, len(self.Xi) + 1):
            self.difference_quotient_table[0].append(f"{j - 1}阶")
        for i in range(1, len(self.Xi) + 1):
            self.difference_quotient_table[i].append(self.Xi[i - 1])
        for i in range(1, len(self.Xi) + 1):
            self.difference_quotient_table[i].append(self.Yi[i - 1])
        for i in range(1, len(self.Xi) + 1):
            for j in range(2, len(self.Xi) + 1):
                if i < j:
                    self.difference_quotient_table[i].append(" ")
                else:
                    self.difference_quotient_table[i].append((self.difference_quotient_table[i][j - 1] -
                                                              self.difference_quotient_table[i - 1][j - 1]) / (
                                                                     self.difference_quotient_table[i][0] -
                                                                     self.difference_quotient_table[i - j + 1][0]))
        self.difference_quotient_table[0].append("因子")
        self.difference_quotient_table[1].append(1)
        factor = "1"
        for i in range(2, len(self.Xi) + 1):
            factor = factor + f"*(x - {self.difference_quotient_table[i - 1][0]})"
            self.difference_quotient_table[i].append(factor)

    def print_difference_quotient_table(self):
        """
        输出差商表
        :return:
        """
        self._get_difference_quotient_table()
        print(tabulate(self.difference_quotient_table[1:],
                       headers=self.difference_quotient_table[0],
                       tablefmt="simple"))

    def calculate_interpolation_polynomial(self):
        """
        计算牛顿插值表达式
        :return:
        """
        polynomial = f"{self.difference_quotient_table[1][1]} * " \
                                   f"{self.difference_quotient_table[1][len(self.Xi) + 1]}"
        for i in range(2, len(self.Xi) + 1):
            polynomial = polynomial + f" + ({self.difference_quotient_table[i][i]}) * " \
                                      f"({self.difference_quotient_table[i][len(self.Xi) + 1]})"
        x = sympy.Symbol('x')
        return eval(polynomial)

    def calculate_interpolation(self, value: float):
        """
        根据插值表达式预测
        :param value:
        :return:
        """
        x = sympy.Symbol('x')
        polynomial = self.calculate_interpolation_polynomial()
        return polynomial.evalf(subs={x: value})


if __name__ == '__main__':
    # x = [2010, 2011, 2012, 2013, 2014, 2015, 2016]
    # y = [70, 122, 144, 156, 174, 196, 202]
    x = [0, 3, 5, 7, 9, 11, 12, 13, 14]
    y = [0, 1.2, 1.7, 2, 2.1, 2, 1.8, 1.2, 1]
    n = NewtonInterpolation(x, y)
    n.print_difference_quotient_table()
    print("插值得到的牛顿插值表达式为：")
    print(n.calculate_interpolation_polynomial())
    x1 = []
    y1 = []
    for i in range(0, 140):
        x1.append(i/10)
        y1.append(n.calculate_interpolation(i/10))
    fig, ax = plt.subplots()
    ax.scatter(x, y)
    ax.plot(x1, y1)
    plt.show()
    print(f"f0=={n.calculate_interpolation(0)}")
