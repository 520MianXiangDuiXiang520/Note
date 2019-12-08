from time import sleep


class TLB:
    _data = []

    def __new__(cls):
        if not hasattr(cls, '_object'):
            cls._object = super().__new__(cls)
        return cls._object

    def __init__(self):
        self._max_length = 10

    def __iter__(self):
        self._index = 0

        return self

    def __next__(self):
        if self._index >= len(self._data):
            raise StopIteration
        data = self._data[self._index]
        self._index += 1
        # 模拟快表速度高于页表
        sleep(0.1)
        return data

    def fifo(self):
        """
        如果快表满了，就按先进先出的原则删除一个快表项
        :return:
        """
        if len(self._data) > self._max_length:
            print("快表满了，执行置换")
            self._data.pop(0)

    def append(self, data: tuple):
        self.fifo()
        self._data.append(data)

    @property
    def data(self):
        return self._data


if __name__ == '__main__':
    for i in TLB():
        print(i)

