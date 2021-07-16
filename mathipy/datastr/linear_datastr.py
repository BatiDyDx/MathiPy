from typing import Iterator, List, TypeVar, Generic

T = TypeVar('T') # Type Variable

class Stack(Generic[T]):
    elements: List[T]
    
    def __init__(self, *args):
        self.elements = list(args)

    def get(self) -> T:
        return self.elements.pop()

    def add(self, value: T) -> None:
        self.elements.append(value)

    def __iter__(self) -> Iterator:
        return iter(self.elements)

    def __str__(self) -> str:
        return f'Stack({self.elements})'

    def __repr__(self) -> str:
        return 'Stack datastr'


class Queue(Generic[T]):
    elements: List[T]
    
    def __init__(self, *args):
        self.elements = list(args)

    def get(self) -> T:
        return self.elements.pop(0)

    def add(self, value: T) -> None:
        self.elements.append(value)

    def __iter__(self) -> Iterator:
        return iter(self.elements)

    def __str__(self) -> str:
        return f'Queue({self.elements})'

    def __repr__(self) -> str:
        return 'Queue datastr'
