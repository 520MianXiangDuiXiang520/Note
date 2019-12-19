from copy import copy
from SystemOfLinearEquations.GaussianElimination import GaussianElimination


class GaussianPrincipalElimination(GaussianElimination):
    def __init__(self):
        super().__init__()

    def swap(self, a: int, b: int):
        m = copy(self.augmented_matrix[a])
        r = copy(self.augmented_matrix[b])
        for index, i in enumerate(r):
            self.augmented_matrix[a][index] = i
        for index, j in enumerate(m):
            self.augmented_matrix[b][index] = j

    def first_determine_pivot(self):
        for i in range(1, 3):
            maxa = abs(self.augmented_matrix[0][0])
            if abs(self.augmented_matrix[i][0]) > maxa:
                self.swap(i, 0)

    def second_determine_pivot(self):
        for i in range(2, 3):
            maxa = abs(self.augmented_matrix[1][1])
            if abs(self.augmented_matrix[i][1]) > maxa:
                self.swap(i, 1)

    def first(self):
        print("第一次选取列主元：")
        self.first_determine_pivot()
        for i in self.augmented_matrix:
            print(i)
        print("*"*70)
        super().first()

    def second(self):
        print("第二次选取列主元：")
        for i in self.augmented_matrix:
            print(i)
        print("*" * 70)
        self.second_determine_pivot()
        super().second()


if __name__ == '__main__':
    ge = GaussianPrincipalElimination()
    ge.first()
    ge.second()
    ge.result()

