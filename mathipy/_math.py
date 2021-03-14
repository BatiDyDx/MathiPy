import numpy as np
import mathipy.numeric_operations as ops

e     = 2.718281828459045
pi    = 3.141592653589793
tau   = 6.2831853071796
sqrt2 = 1.4142135623731
phi   = 1.618033988749894
gamma = 0.577215664901532860

class Infinite(float):
    def __init__(self, neg = False):
        self.neg = neg

    def __add__(self, n):
        return self

    def __radd__(self, n):
        return self

    def __sub__(self, n):
        return self

    def __rsub__(self, n):
        return -self

    def __neg__(self):
        if self.neg == False:
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

    def __pow__(self, n):
        return self

    def __rpow__(self, n):
        return self

    def __float__(self):
        if not self.neg:
            return float('inf')
        else:
            return float('-inf')

    def __str__(self):
        if not self.neg:
            return 'inf'
        else:
            return '-inf'

    def __repr__(self):
        return str(self)

def pascal_triangle(n: int) -> list:
    if n == 0:
        return []
    elif n == 1:
        return [[1]]
    else:
        new_row = [1]
        result = pascal_triangle(n-1)
        last_row = result[-1]
        for i in range(len(last_row)-1):
            new_row.append(last_row[i] + last_row[i+1])
        new_row.extend([1])
        result.append(new_row)
    return result

def summation(f: callable, up_bound: int, low_bound: int= 0) -> float:
    if up_bound < low_bound:
        return 0
    elif up_bound == low_bound:
        return f(low_bound)    
    else:
        return f(low_bound) + summation(f, up_bound, low_bound + 1)

def product(f: callable, up_bound: int, low_bound: int= 0) -> float:
    if up_bound < low_bound:
        return 0
    elif up_bound == low_bound:
        return f(low_bound)
    else:
        return f(low_bound) * product(f, up_bound, low_bound + 1)

def gcd(a: int, b: int) -> int:
    if a % b == 0:
        return b
    else:
        c = a % b
        return gcd(b, c)

def mcm(a: int, b: int) -> int:
    d = gcd(a,b)
    return (a * b) // d

def fibonacci(n: int) -> 'generator object':
    a, b = 0, 1
    i = 0
    while i < n:
        a, b = b, b + a
        i += 1
    yield a
    yield from fibonacci(n + 1)

@ops.uFunc
def abs(x):
    if ops.is_scalar(x):
        if isinstance(x, complex):
            #Since native python complex numbers do not have the module
            #attribute, it is calculated either if it's complex or mpy.Complex
            return sqrt((x.real)**2 + (x.imag)**2)
        if x < 0:
            return -x
        else:
            return x

@ops.uFunc
def factorial(n: int) -> int:
    if n < 0:
        raise ValueError('Cannot calculate factorial of negative numbers')
    if n == 1 or n == 0:
        return 1
    return n * factorial(n - 1)

@ops.uFunc
def differential(x, magnitude = 10):
    h = 10 ** -magnitude
    delta_x = x + x * h
    return delta_x

@ops.uFunc
def sin(x):
    y = (e ** (1j * x) - e ** (-1j * x)) / 2j
    y = ops.round_if_close(y)
    if isinstance(x, complex):
        return y
    return y.real

@ops.uFunc
def cos(x):
    return sin(x + pi / 2)

@ops.uFunc
@ops.handleZeroDivision
def tan(x):
    return sin(x) / cos(x)

@ops.uFunc
def cosh(x):
    return cos(x * 1j)

@ops.uFunc
def sinh(x):
    y = ((e ** x) - (e ** -x)) / 2
    y = ops.round_if_close(y)
    if isinstance(x, complex):
        return y
    return y.real

@ops.uFunc
def tanh(x):
    return sinh(x) / cosh(x)

@ops.uFunc
@ops.handleZeroDivision
def cosec(x):
    return 1 / sin(x)

@ops.uFunc
@ops.handleZeroDivision
def sec(x):
    return 1 / cos(x)

@ops.uFunc
@ops.handleZeroDivision
def cotan(x):
    return cos(x) / sin(x)

@ops.uFunc
@ops.handleZeroDivision
def cosech(x):
    return 1 / sinh(x)

@ops.uFunc
def sech(x):
    return 1 / cosh(x)

@ops.uFunc
@ops.handleZeroDivision
def cotanh(x):
    return cosh(x) / sinh(x)

import mathipy._complex as C
@ops.uFunc
def ln(x):
    if x == 0:
        return -Infinite()
    
    if isinstance(x, complex):
        x = C.to_Complex(x)
        return C.Complex(ln(x.r), x.theta)
    elif x < 0:
        return np.nan
    else:
        return 2 * np.arctanh((x - 1)/(x + 1))

@ops.uFunc
def log(x, base= 10):
    if base.real <= 1 and base.imag == 0:
        raise ValueError('Base must be greater than 1')
    return ln(x) / ln(base)

@ops.uFunc
def root_n(x, index, return_complex: bool= True):
    if isinstance(x, complex):
        return x ** (1 / index)
    else:
        if x >= 0:
            return x ** (1 / index)
        else:
            if index % 2 == 0:
                return C.Complex(0, root_n(-x, index)) if return_complex else np.nan
            else:
                return -root_n(-x, index)

@ops.uFunc
def sqrt(x, return_complex: bool= True):
    return root_n(x, 2, return_complex)