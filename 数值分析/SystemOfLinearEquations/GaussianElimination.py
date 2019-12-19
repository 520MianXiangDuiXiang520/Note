"""
高斯消去法
1. 输入增广矩阵
2. 选取主元
3. 第0行不变，确定m10, m20 ; m10 = a10/a00; m20 = a20/a00
4. 第0， 1行不变，确定 m21; m21 = a21/a11

m[i][j] =  a[i][j] / a[i][i]
"""


class GaussianElimination:
    def __init__(self):
        self.augmented_matrix = [
            [0.3475, 1.8423, 0.4759, 1.7321],
            [0.9428, 0.3475, -0.8468, 0.4127],
            [-0.8468, 0.4759, 1.2147, -0.8621]
        ]
        self.row_num = len(self.augmented_matrix)

    def first(self):
        m1 = self.augmented_matrix[1][0] / self.augmented_matrix[0][0]
        m2 = self.augmented_matrix[2][0] / self.augmented_matrix[0][0]
        for i in range(len(self.augmented_matrix[1])):
            self.augmented_matrix[1][i] = self.augmented_matrix[1][i] - m1 * self.augmented_matrix[0][i]
        for i in range(len(self.augmented_matrix[2])):
            self.augmented_matrix[2][i] = self.augmented_matrix[2][i] - m2 * self.augmented_matrix[0][i]
        for i in self.augmented_matrix:
            print(i)

    def second(self):
        m3 = self.augmented_matrix[2][1] / self.augmented_matrix[1][1]
        for i in range(len(self.augmented_matrix[2])):
            self.augmented_matrix[2][i] = self.augmented_matrix[2][i] - m3 * self.augmented_matrix[1][i]
        print("-"*70)
        for i in self.augmented_matrix:
            print(i)

    def result(self):
        z = self.augmented_matrix[2][3] / self.augmented_matrix[2][2]
        y = (self.augmented_matrix[1][3] - self.augmented_matrix[1][2] * z) / self.augmented_matrix[1][1]
        x = (self.augmented_matrix[0][3] - self.augmented_matrix[0][1] * y - self.augmented_matrix[0][2] * z) /\
            self.augmented_matrix[0][0]
        print("-"*70)
        print(f"x = {x}")
        print(f"y = {y}")
        print(f"z = {z}")


if __name__ == '__main__':
    ge = GaussianElimination()
    ge.first()
    ge.second()
    ge.result()
