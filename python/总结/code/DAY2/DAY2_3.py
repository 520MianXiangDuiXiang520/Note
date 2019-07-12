def add(self, value):
    print('add one value')
    self.append(value)


class ListMetaclass(type):
    def __new__(mcs, name, bases, namespace):
        namespace['add'] = add
        return type.__new__(mcs, name, bases, namespace)


class MyList(list, metaclass=ListMetaclass):
    pass


li = MyList()
li.add(1)
print(li)
