class BinarySortTree:
    def __init__(self, value: int):
        self.left = None
        self.right = None
        self.value = value

    def __str__(self):
        return str(self.value)

    def _add_new_node(self, node, value: int):
        if value < node.value:
            # 存到左子树
            if node.left is not None:
                self._add_new_node(node.left, value)
            else:
                node.left = BinarySortTree(value)
        elif value > node.value:
            if node.right is not None:
                self._add_new_node(node.right, value)
            else:
                node.right = BinarySortTree(value)
        else:
            pass

    def add_node(self, value):
        self._add_new_node(self, value)

    def add_many_node(self, values: list):
        for value in values:
            self.add_node(value)

    def _mid_visiting(self, root):
        if root.left:
            self._mid_visiting(root.left)
        print(root, end=" ")
        if root.right:
            self._mid_visiting(root.right)

    def mid_visiting(self):
        self._mid_visiting(self)
        print()

    def _find(self, root, value):
        if root.value == value:
            return root
        elif root.value < value:
            if root.right:
                return self._find(root.right, value)
        else:
            if root.left:
                return self._find(root.left, value)

    def find(self, value: int):
        return self._find(self, value)

    @staticmethod
    def _delete(root):
        if not root.left and not root.right:
            return None
        elif root.left and not root.right:
            return root.left
        elif root.right and not root.left:
            return root.right
        else:
            this = root.right
            while this.left:
                this = this.left
            this.left = root.left
            return this
            

    def _delete_node(self, root, value):
        if root.left and root.left.value == value:
            root.left = self._delete(root.left)
        elif root.right and root.right.value == value:
            root.right = self._delete(root.right)
        elif root.value < value:
            self._delete_node(root.right, value)
        elif root.value > value:
            self._delete_node(root.left, value)
        return root

    def delete_node(self, value):
        if self.value == value:
            return self._delete(self)
        else:
            try:
                return self._delete_node(self, value)
            except AttributeError:
                print("没有此元素")


if __name__ == '__main__':
    bst = BinarySortTree(7)
    bst.add_many_node([3, 8, 2, 0, 5, 1])
    bst.add_node(99)
    bst.add_node(-1)
    bst.add_node(6)
    bst.mid_visiting()
    bst = bst.delete_node(7)
    bst.mid_visiting()
