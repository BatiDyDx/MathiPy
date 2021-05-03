from mathipy.datastr import Node


class Tree(Node):
    def __init__(self, value, parent = None):
        self.value = value
        self.children = []
        self.parent = parent
        if self.parent:
            parent.add(self)

    def add(self, *children_values):
        children = []
        new_children_values = []
        for c in children_values:
            if isinstance(c, Tree):
                children.append(c)
            else:
                new_children_values.append(c)
    
        for child in children:
            self.children.append(child)
            child.parent = self
    
        new_children = []
        for value in new_children_values:
            new_child = Tree(value)
            self.children.append(new_child)
            new_child.parent = self
            new_children.append(new_child)

        return new_children if True else None

    def get_child(self, child_value):
        for child in self.children:
            if child.value == child_value:
                return child

    def get_children(self):
        return self.children

    def is_child_of(self, parent):
        if self in parent.children:
            return True
        else:
            return False

    def is_parent_of(self, child):
        if child in self.children:
            return True
        else:
            return False

    def __str__(self):
        children = [c.value for c in self.children] if self.children else None
        return f'Tree(Parent: {self.parent.value if self.parent else None}, Value: {self.value}, Children: {children})'

    def __repr__(self):
        return str(self)
