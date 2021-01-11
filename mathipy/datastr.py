class Stack(object):
    def __init__(self, *args):
        self.__elements = list(args)

    def elements(self):
        return self.__elements

    def get(self):
        return self.__elements.pop()

    def add(self, x):
        self.__elements.append(x)

    def __iter__(self):
        return iter(self.__elements)

    def __repr__(self):
        return f'Stack({self.__elements})'

class Queue(object):
    def __init__(self, *args):
        self.__elements = list(args)

    def elements(self):
        return self.__elements

    def get(self):
        return self.__elements.pop(0)

    def add(self, x):
        self.__elements.append(x)

    def __iter__(self):
        return iter(self.__elements)

    def __str__(self):
        return f'Queue({self.__elements})'

    def __repr__(self):
        return str(self)

class Graph(object):
    pass

class Node(Graph):
    def __init__(self, node_value):
        self.__node_value = node_value
        self.__connections = []

    def add(self, *iterable):
        nodes = []
        new_node_values = []
        for n in iterable:
            if isinstance(n, Node):
                nodes.append(n)
            else:
                new_node_values.append(n)
    
        for node in nodes:
            self.__connections.append(node)
            node.__connections.append(self)
    
        new_nodes = []
        for value in new_node_values:
            new_node = Node(value)
            self.__connections.append(new_node)
            new_node.__connections.append(self)
            new_nodes.append(new_node)

        return new_nodes if True else None

    def get_connection(self, value):
        for connection in self.__connections:
            if connection.__node_value == value:
                return connection

    def get_connections(self):
        return self.__connections

    def is_connected_with(self, node):
        for connection in self.__connections:
            if connection.__node_value == node.__node_value:
                return True
        return False

    def __str__(self, preview_connections = True):
        connections = [c.__node_value for c in self.__connections]
        return f'Graph(Value: {self.__node_value}, Connections: {connections})'

    def __repr__(self):
        return str(self)

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

class BinaryTree(Tree):
    def __init__(self):
        pass