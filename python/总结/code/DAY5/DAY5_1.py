# import os
# help(os)
# # Help on module os:
# #
# # NAME
# #     os - OS routines for NT or Posix depending on what system we're on.
# #
# # DESCRIPTION

class Demo:
    """
    this is a Demo
    """
    classVar = 0

    def __init__(self):
        self.var1 = 1

    def output(self):
        print(self.var1)

if __name__ == '__main__':
    # help(Demo)
    # def demoMethods(a):
    #     """
    #     这是一个示例函数
    #     :param a: 示例形参
    #     :return: None
    #     """
    #     print(a)
    # help(demoMethods)
    demo = Demo()
    # help(3)
    dir(Demo)