from mathipy import _math
from mathipy import arithmetic

class AlgebraicExpression:
    '''
    Mathematical algebraic expressions
    for operating with multiple variables
    '''
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

class Variable(AlgebraicExpression):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def evaluate(self, vars):
        return vars[self.name]

class Constant(AlgebraicExpression):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

    def evaluate(self, vars):
        if isinstance(self.value, str):
            return Constant.consts[self.value]
        else:
            return self.value

class Infinite:
    def __init__(self, neg = False):
        self.neg_inf = neg

    def __add__(self, n):
        return self

    def __radd__(self, n):
        return self

    def __sub__(self, n):
        return self

    def __rsub__(self, n):
        return -self

    def __neg__(self):
        if self.neg_inf == False:
            return Infinite(neg = True)
        else:
            return Infinite()

    def __mul__(self, n):
        return self

    def __rmul__(self, n):
        return self

    def __truediv__(self, n):
        return self

    def __rtruediv__(self, n):
        return 0

    def __float__(self):
        if not self.neg_inf:
            return float('inf')
        else:
            return float('-inf')

    def __repr__(self):
        if not self.neg_inf:
            return 'Infinite'
        else:
            return '-Infinite'

class Undefined:
    def __add__(self, n):
        return self
    
    def __radd__(self, n):
        return self
    
    def __sub__(self, n):
        return self
    
    def __rsub__(self, n):
        return self
    
    def __mul__(self, n):
        return self
    
    def __rmul__(self, n):
        return self
    
    def __truediv__(self, n):
        return self
    
    def __rtruediv__(self, n):
        return self
    
    def __floordiv__(self, n):
        return self
    
    def __rfloordiv__(self, n):
        return self
    
    def __pow__(self, n):
        return self
    
    def __rpow__(self, n):
        return self
    
    def __neg__(self):
        return self
    
    def __bool__(self):
        return False
    
    def __str__(self):
        return 'undefined'
    
    def __repr__(self):
        return 'undefined'