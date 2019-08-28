# 迭代器，可迭代对象
from collections.abc import Iterator
from collections.abc import Iterable


class ClassMate:
    def __init__(self):
        self.names = []
        self._order = 0

    def __iter__(self):
        return self

    def __next__(self) -> object:
        if self._order < len(self.names):
            result: object = self.names[self._order]
            self._order += 1
            return result
        else:
            raise StopIteration

    def add_student(self, name):
        self.names.append(name)


if __name__ == '__main__':
    cm = ClassMate()
    cm.add_student('a')
    cm.add_student('b')
    print(isinstance(cm, Iterable))
    for i in cm:
        print(i)
