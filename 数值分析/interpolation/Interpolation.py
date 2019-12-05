from abc import abstractmethod


class Interpolation:
    def __init__(self, x: list, y: list):
        self.Xi = x
        self.Yi = y

    @abstractmethod
    def calculate_interpolation_polynomial(self):
        """
        计算插值表达式
        :return:
        """
        pass

    @abstractmethod
    def calculate_interpolation(self, value: float):
        """
        根据插值表达式预测/求值
        :param value:
        :return:
        """
        pass
