class C:
    def __init__(self):
        self._x = 11
        self.value = ''

    @property
    def x(self):
        """I'm the 'x' property."""
        return self._x

    @x.setter
    def x(self, value):
        value = 1111
        self._x = value

    @x.deleter
    def x(self):
        del self._x

if __name__ == '__main__':
    c = C()

    print(type(c.x))