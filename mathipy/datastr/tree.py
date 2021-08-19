from typing import List, Optional, TypeVar, Generic, Union
from mathipy.datastr.graph import Graph

T = TypeVar('T')

class Tree(Graph, Generic[T]):
    value: T
    children: List[T]
    parent: Optional[T]

    def __init__(self, value: T, parent: Optional['Tree'] = None) -> None:
        self.value = value
        self.children = []
        self.parent = parent
        if self.parent:
            parent.add(self)

    def add(self, *children_values: Union[T, 'Tree']) -> List['Tree']:
        children: List['Tree'] = []
        new_children_values: List[T] = []
        for c in children_values:
            if isinstance(c, Tree):
                children.append(c)
            else:
                new_children_values.append(c)
    
        for child in children:
            self.children.append(child)
            child.parent = self
    
        new_children: List['Tree'] = []
        for value in new_children_values:
            new_child = Tree(value, self)
            self.children.append(new_child)
            new_children.append(new_child)

        return new_children

    def get_child(self, child_value: T) -> 'Tree':
        for child in self.children:
            if child.value == child_value:
                return child

    def is_child_of(self, parent: 'Tree') -> bool:
        return self in parent.children

    def is_parent_of(self, child: 'Tree') -> bool:
        return child in self.children

    def __str__(self) -> str:
        children = [c.value for c in self.children] if self.children else None
        return f'Tree(Parent: {self.parent.value if self.parent else None}, Value: {self.value}, Children: {children})'

    def __repr__(self) -> str:
        return str(self)
