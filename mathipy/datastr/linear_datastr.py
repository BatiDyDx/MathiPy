from typing import Iterator, List, Sequence, TypeVar, Generic
from abc import ABC, abstractmethod

T = TypeVar('T') # Type Variable

class LinearDataStruct(Generic[T], ABC):
    name: str
    _elements: List[T]

    def __init__(self, elements: Sequence[T]) -> None:
        self._elements: List[T] = list(elements)

    @property
    def elements(self) -> List[T]:
        return self._elements

    def add(self, value: T) -> None:
        """
        Add elements to the data structure
        """
        self._elements.append(value)

    @abstractmethod
    def get(self) -> T:
        """
        Get the corresponding element according to the data structure
        """
        pass

    def empty(self) -> bool:
        return len(self.elements) == 0

    def __iter__(self) -> Iterator:
        return iter(self.elements)

    def __str__(self) -> str:
        return f'{self.name}({self.elements})'

    def __repr__(self) -> str:
        return f'mathipy.{self.name}'


class Stack(LinearDataStruct[T]):
    name: str = 'Stack'
    _elements: List[T]

    def get(self) -> T:
        return self._elements.pop()


class Queue(LinearDataStruct[T]):
    name: str = 'Queue'
    _elements: List[T]

    def get(self) -> T:
        return self._elements.pop(0)
