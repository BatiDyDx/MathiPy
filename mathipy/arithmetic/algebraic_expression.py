from mathipy.math import ntheory
from abc import ABC, abstractmethod
from typing import Dict, Union
from mathipy import arithmetic
from dataclasses import dataclass, field

class AlgebraicExpression(ABC):
    """
    Mathematical algebraic expressions
    for operating with multiple variables
    equations and functions
    """

    def __config__(self) -> None:
        if not isinstance(self.a, AlgebraicExpression):
            self.a = Constant(self.a)

        if not isinstance(self.b, AlgebraicExpression):
            self.b = Constant(self.b)

    @abstractmethod
    def evaluate(self, v) -> Union[int, float, complex]:
        pass

    def __add__(a, b) -> 'arithmetic.addition.Sum':
        return arithmetic.addition.Sum(a, b)

    def __radd__(a, b) -> 'arithmetic.addition.Sum':
        return arithmetic.addition.Sum(a, b)

    def __sub__(a, b) -> 'arithmetic.addition.Minus':
        return arithmetic.addition.Minus(a, b)

    def __rsub__(a, b) -> 'arithmetic.addition.Minus':
        return arithmetic.addition.Minus(b, a)

    def __mul__(a, b) -> 'arithmetic.multiplication.Product':
        return arithmetic.multiplication.Product(a, b)

    def __rmul__(a, b) -> 'arithmetic.multiplication.Product':
        return arithmetic.multiplication.Product(a, b)

    def __neg__(a) -> 'arithmetic.multiplication.Product':
        return arithmetic.multiplication.Product(a, -1)

    def __truediv__(a, b) -> 'arithmetic.multiplication.Division':
        return arithmetic.multiplication.Division(a, b)

    def __rtruediv__(a, b) -> 'arithmetic.multiplication.Division':
        return arithmetic.multiplication.Division(b, a)

    def __pow__(a, b) -> 'arithmetic.power.Power':
        return arithmetic.power.Power(a, b)

    def __rpow__(a, b) -> 'arithmetic.power.Power':
        return arithmetic.power.Power(b, a)

    def __call__(self, v) -> Union[int, float, complex]:
        return self.evaluate(v)



@dataclass(init=True, eq=True)
class Variable(AlgebraicExpression):
    name: str = field(default='x', init=True)

    def __repr__(self) -> str:
        return self.name

    def evaluate(self, vars: Dict[str, Union[int, float, complex]]) -> Union[int, float, complex]:
        return vars[self.name]


@dataclass(init=True, eq=True)
class Constant(AlgebraicExpression):
    value: Union[int, float, complex]

    def __repr__(self) -> str:
        return str(self.value)

    def evaluate(self, vars: Dict[str, Union[int, float, complex]]) -> Union[int, float, complex]:
        if isinstance(self.value, str):
            return ntheory.math_constants[self.value]
        else:
            return self.value
