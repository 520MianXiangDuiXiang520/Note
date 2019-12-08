from time import sleep


class RAM:
    blocks = [(0, None), (1, None), (2, None), (3, None), (4, None), (5, None),
             (6, None), (7, None), (8, None), (9, None), (10, None), (11, None)]
    blocks = [list(i) for i in blocks]

    def __str__(self):
        return str([i for i in self.blocks])


class PageTable:

    def __init__(self, data: list = None):
        if data:
            self._data = data
        else:
            self._data = []

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index >= len(self._data):
            raise StopIteration
        data = self._data[self._index]
        self._index += 1
        sleep(1)
        return data

    @property
    def page_table(self):
        return self._data

    def append(self, data: tuple):
        self._data.append(data)


if __name__ == '__main__':
    P = PageTable()
    print(P.page_table[0])
