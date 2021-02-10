from mathipy.functions import logarithmic 
e     = 2.718281828459045
pi    = 3.141592653589793
tau   = 2 * pi
sqrt2 = 2 ** (1/2)
phi   = 1.618033988749894
gamma = 0.577215664901532860

class AlgebraicExpression:
    consts = {
        'e'     : e,
        'pi'    : pi,
        'tau'   : tau,
        'sqrt2' : sqrt2,
        'phi'   : phi,
        'gamma' : gamma
    }

class Sum(AlgebraicExpression):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return f'({self.a} + {self.b})'

    def evaluate(self, vars):
        return self.a.evaluate(vars) + self.b.evaluate(vars)

class Minus(AlgebraicExpression):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return f'({self.a} - {self.b})'

    def evaluate(self, vars):
        return self.a.evaluate(vars) - self.b.evaluate(vars)

class Product(AlgebraicExpression):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return f'({self.a} * {self.b})'

    def evaluate(self, vars):
        return self.a.evaluate(vars) * self.b.evaluate(vars)

class Division(AlgebraicExpression):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return f'([{self.a}] / [{self.b}])'

    def evaluate(self, vars):
        return self.a.evaluate(vars) / self.b.evaluate(vars)

class Power(AlgebraicExpression):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return f'{self.a}^({self.b})'

    def evaluate(self, vars):
        return self.a.evaluate(vars) ** self.b.evaluate(vars)

class Root(AlgebraicExpression):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return f'{self.b}-Root({self.a})'

    def evaluate(self, vars):
        return self.a.evaluate(vars) ** (1 / self.b.evaluate(vars))

class Logarithm(AlgebraicExpression):
    def __init__(self, a, base):
        self.a = a
        self.base = base

    def __repr__(self):
        return f'Log_{self.base}({self.a})'

    def evaluate(self, vars):
        return logarithmic.Log.log(self.a.evaluate(vars), self.base.evaluate(vars))

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
        return '(' + str(self.value) + ')'

    def evaluate(self, vars):
        if isinstance(self.value, str):
            return Constant.consts[self.value]
        else:
            return self.value

class Infinite():
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

class Undefined():
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