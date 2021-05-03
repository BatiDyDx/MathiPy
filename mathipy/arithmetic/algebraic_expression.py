from mathipy import _math
from mathipy import arithmetic
from dataclasses import dataclass


class AlgebraicExpression:
    """
    Mathematical algebraic expressions
    for operating with multiple variables
    """
    consts = {
        'e'     : _math.e,
        'pi'    : _math.pi,
        'tau'   : _math.tau,
        'sqrt2' : _math.sqrt2,
        'phi'   : _math.phi,
        'gamma' : _math.gamma
    }

    def __config__(self):
        if not isinstance(self.a, AlgebraicExpression):
            self.a = Constant(self.a)

        if not isinstance(self.b, AlgebraicExpression):
            self.b = Constant(self.b)

    def __add__(a, b):
        return arithmetic.addition.Sum(a, b)

    def __radd__(a, b):
        return a + b

    def __sub__(a, b):
        return arithmetic.addition.Minus(a, b)

    def __rsub__(a, b):
        return -a + b

    def __mul__(a, b):
        return arithmetic.multiplication.Product(a, b)

    def __rmul__(a, b):
        return a * b
    
    def __neg__(a):
        return a * -1

    def __truediv__(a, b):
        return arithmetic.multiplication.Division(a, b)

    def __rtruediv__(a, b):
        return b * (1 / a)
    
    def __pow__(a, b):
        return arithmetic.power.Power(a, b)

    def __rpow__(a, b):
        return arithmetic.power.Power(b, a)

    def __call__(self, v):
        return self.evaluate(v)


@dataclass(init=True, eq=True)
class Variable(AlgebraicExpression):
    name: str

    def __repr__(self):
        return self.name

    def evaluate(self, vars):
        return vars[self.name]


@dataclass(init=True, eq=True)
class Constant(AlgebraicExpression):
    value: float

    def __repr__(self):
        return str(self.value)

    def evaluate(self, vars):
        if isinstance(self.value, str):
            return Constant.consts[self.value]
        else:
            return self.value
