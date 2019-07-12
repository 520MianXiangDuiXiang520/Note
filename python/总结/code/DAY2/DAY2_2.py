# 模拟__init__()
def __init__(self,name,age):
    self.name = name
    self.age = age

def output(self):
    print("name is " + str(self.name) + " age is " + str(self.age))


class_name = 'Demo'
class_bases = (object,)
class_dict = {
    '__init__':__init__,
    'output': output,
}

# type(name, bases, dict) -> a new type
Demo = type(class_name,class_bases,class_dict)
demo = Demo('Bob',18)
demo.output()  # name is Bob age is 18