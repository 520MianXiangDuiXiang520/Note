import sympy

from interpolation.Interpolation import Interpolation


class LagrangeInterpolation(Interpolation):
    def __init__(self, x: list, y: list):
        super().__init__(x, y)
        self.n = len(x) - 1

    def calculate_interpolation_polynomial(self):
        """
        计算插值表达式
        :return:
        """
        for k in range(self.n):
            lx = "1"
            for i in range(self.n):
                if i != k:
                    lx += f"*"
        result = 0
        k = sympy.Symbol('k')
        sympy.summation(2 * k, (k, 0, self.n))

    def calculate_interpolation(self, value: float):
       pass
