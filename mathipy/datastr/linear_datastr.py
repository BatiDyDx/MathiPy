class Stack:
    def __init__(self, *args):
        self.elements = list(args)

    def get(self):
        return self.elements.pop()

    def add(self, x):
        self.elements.append(x)

    def __iter__(self):
        return iter(self.elements)

    def __str__(self):
        return f'Stack({self.elements})'

    def __repr__(self):
        return str(self)

class Queue:
    def __init__(self, *args):
        self.elements = list(args)

    def get(self):
        return self.elements.pop(0)

    def add(self, x):
        self.elements.append(x)

    def __iter__(self):
        return iter(self.elements)

    def __str__(self):
        return f'Queue({self.elements})'

    def __repr__(self):
        return str(self)
