import sympy
from SolvingNonlinearEquations.Newton import Newton

x = sympy.Symbol('x')


class NewtonIteration(Newton):
    """
    非线性方程——牛顿迭代法
    x|(k + 1) = x|(k) - f(x|(k)) / f'(x|(k))
    """
    def __init__(self, function: str, x0: float, deviation: float, n: int):
        super(NewtonIteration, self).__init__(function, x0, deviation, n)

    def computer(self):
        index = 0
        while True:
            assert index < self.N
            x1 = self.x0 - self.computer_fx_value(self.x0) / self.computer_fx_der_value(self.x0)
            if abs(x1 - self.x0) < self.deviation:
                return x1, index
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
    print("牛顿迭代法")
    print("班级：17070144 "
          "姓名：张君保 "
          "学号：1707004650")
    result = run()
    print(result[0])
    print(f"迭代{result[1]}次")

# 请输入迭代函数：1-x-sympy.sin(x)
# 请输入初值x0：0
# 请输入允许误差: 0.00005
# 请输入允许迭代的最大次数：100
# 0.510973429357289
# 迭代2次
