class Duck:
    def __init__(self, name):
        self._name = name

    def call(self):
        print("gua gua gua")

class Frog:
    def __init__(self, name):
        self._name = name

    def call(self):
        print("gua gua gua")

def quack(duck):
    duck.call()

if __name__ == '__main__':
    duck = Duck('Duck')
    frog = Frog('Frog')
    quack(duck)
    quack(frog)