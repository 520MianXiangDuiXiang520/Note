class Demo:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def output(self):
        print("name is " + str(self.name) + " age is " + str(self.age))


if __name__ == '__main__':
    demo = Demo("Bob", 18)
    demo.output()
    type(demo)