class MyIterator:
    def __init__(self, start: int, end: int, step: int = 1):
        self.start = start
        self.end = end
        self.step = step

    def __next__(self):
        if self.start < self.end:
            now = self.start
            self.start += self.step
            return now
        else:
            raise StopIteration

    def __iter__(self):
        return self


if __name__ == '__main__':
    for i in MyIterator(0, 9):
        print(i)
