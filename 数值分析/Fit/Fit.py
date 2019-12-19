import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq




class Fit:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def linear_equation_expression(params, x):
        a, b = params
        return a * x + b

    def error(self, params, x, y):
        return self.linear_equation_expression(params, x) - y

    def slovePara(self):
        p0 = [10, 10]
        Para = leastsq(self.error, p0, args=(self.x, self.y))
        return Para

    def solution(self):
        Para = self.slovePara()
        a, b = Para[0]
        print("拟合出的直线方程为:")
        print("y=" + str(round(a, 2)) + "x+" + str(round(b, 2)))
        print(f"预测2017年利润为{a * 2017 + b}")
        print(f"预测2018年利润为{a * 2018 + b}")
        plt.figure(figsize=(8, 6))
        plt.scatter(self.x, self.y, color="green", label="standardPoint", linewidth=2)
        x = np.linspace(2009, 2019, 100)
        y = a * x + b
        plt.plot(x, y, color="red", label="interpolationLine", linewidth=2)
        plt.legend()
        plt.show()


if __name__ == '__main__':
    X = np.array([2010, 2011, 2012, 2013, 2014, 2015, 2016])
    Y = np.array([70, 122, 144, 156, 174, 196, 202])
    fix = Fit(X, Y)
    fix.solution()