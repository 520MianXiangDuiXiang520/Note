class BinaryTree:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
    
    def __str__(self):
        return str(self.value)

    def add_left(self, value):
        new_tree = BinaryTree(value)
        if self.left is None:
            self.left = new_tree
        else:
            new_tree.left = self.left
            self.left = new_tree
        return new_tree
    
    def add_right(self, value):
        new_tree = BinaryTree(value)
        if self.right is None:
            self.right = new_tree
        else:
            new_tree.right = self.right
            self.right = new_tree
        return new_tree
    
    def add_many_node(self, values: list):
        nodes = [self, ]
        index = 0
        while index < len(values):
            node = nodes.pop(0)
            left_node = node.add_left(values[index])
            nodes.append(left_node)
            index += 1
            if index < len(values):
                right_node = node.add_right(values[index])
                nodes.append(right_node)
                index += 1

    def _pre_visiting(self, root):
        print(root, end=" ")
        if root.left is not None:
            self._pre_visiting(root.left)
        if root.right is not None:
            self._pre_visiting(root.right)

    def pre_visiting(self):
        self._pre_visiting(self)
        print()

    def _mid_visiting(self, root):
        if root.left is not None:
            self._mid_visiting(root.left)
        print(root, end=" ")
        if root.right is not None:
            self._mid_visiting(root.right)
    
    def mid_visiting(self):
        self._mid_visiting(self)
        print()

    def _pos_visiting(self, root):
        if root.left is not None:
            self._pos_visiting(root.left)
        if root.right is not None:
            self._pos_visiting(root.right)
        print(root, end=" ")
    
    def pos_visiting(self):
        self._pos_visiting(self)
        print()
    
    def _level_visiting(self, root):
        queue = [root]
        for node in queue:
            print(node, end=" ")
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)



    def level_visiting(self):
        self._level_visiting(self)
        print()



def create_new_tree_by_list(values: list):
    pass


if __name__ == '__main__':
    tree = BinaryTree("0")
    tree.add_many_node([1, 2, 3, 4, 5])
    tree.pre_visiting()
    tree.mid_visiting()
    tree.pos_visiting()
    tree.level_visiting()
