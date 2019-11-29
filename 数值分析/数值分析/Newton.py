import sympy
from abc import abstractmethod

x = sympy.Symbol('x')


class Newton:
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

    @abstractmethod
    def computer(self):
        pass
