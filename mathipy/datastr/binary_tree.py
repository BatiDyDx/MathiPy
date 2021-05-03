from mathipy.datastr import Tree


class BinaryTree(Tree):
    def __init__(self, data):
        self.data = data
        self.left, self.right = (None, None)

    def insert(self, *values):
        for value in values:
            if value <= self.data:
                if self.left:
                    self.left.insert(value)
                else:
                    self.left = BinaryTree(value)
            else:
                if self.right:
                    self.right.insert(value)
                else:
                    self.right = BinaryTree(value)

    def contains(self, value) -> bool:
        if value == self.data: return True
        elif value <= self.data:
            if self.left:
                return self.left.contains(value)
            else: return False
        else:
            if self.right:
                return self.right.contains(value)
            else: return False

    def printInOrder(self):
        if self.left:
            self.left.printInOrder()
        print(self.data)
        if self.right:
            self.right.printInOrder()

    def printPreOrder(self):
        print(self.data)
        if self.left:
            self.left.printPreOrder()
        if self.right:
            self.right.printPreOrder()

    def printPostOrder(self):
        if self.left:
            self.left.printPostOrder()
        if self.right:
            self.right.printPostOrder()
        print(self.data)

    def __str__(self):
        try:
            left = self.left.data
        except AttributeError:
            left = None
        try:
            right = self.right.data
        except AttributeError:
            right = None
        finally:
            s =  'Binary Tree('
            s += f'\n  Data:  {self.data}' 
            s += f'\n  Left:  {left}'
            s += f'\n  Right: {right}'
            s += '\n)'
            return s

    def __repr__(self):
        return str(self)