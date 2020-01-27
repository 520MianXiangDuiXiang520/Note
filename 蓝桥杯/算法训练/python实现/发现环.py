class Node:
    def __init__(self, value=None):
        self.value = value
        self.children = []
        self.fathers = []

    def add_child(self, node):
        self.children.append(node)

    def add_father(self, node):
        self.fathers.append(node)


def creat_tree(roads: list, count: int):
    nodes = [Node(value) for value in range(1, count + 1)]
    for i in roads:
        nodes[i[0] - 1].add_child(nodes[i[1] - 1])
        nodes[i[1] - 1].add_father(nodes[i[0] - 1])
    return nodes


r = []


def get_all_fathers(node):
    r.append(node.value)
    if len(node.fathers) > 0:
        for father in node.fathers:
            get_all_fathers(father)


def result(nodes: list, count: int):
    nodes = creat_tree(nodes, count)
    for node in nodes:
        if len(node.fathers) > 1:
            get_all_fathers(node)


num = int(input())
get_data = []
for i in range(num):
    get = input()
    p = [int(i) for i in get.split(" ") if i != '']
    p.sort()
    get_data.append(p)
result(get_data, num)
r = list(r)
r.sort()
sr = list(set(r))
start = len(r) - len(sr)

r = r[2 * start - 1:]
for i in r:
    print(i, end=" ")
