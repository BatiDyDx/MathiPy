import numpy as np
import mathipy.numeric_operations as ops

e     = 2.718281828459045
pi    = 3.141592653589793
tau   = 6.2831853071796
sqrt2 = 1.4142135623731
phi   = 1.618033988749894
gamma = 0.577215664901532860

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
    elif ops.is_iter(x):
        return np.array(list(map(abs, x)))

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

def factorial(n):
    if n < 0:
        raise ValueError('Cannot calculate factorial of negative numbers')
    if n == 1 or n == 0:
        return 1
    return n * factorial(n - 1)

def sin(x):
    if ops.is_iter(x):
        return np.array(list(map(sin, x)))
    y = (e ** (1j * x) - e ** (-1j * x)) / 2j
    y = ops.round_int(y)
    if y.imag == 0:
        return y.real
    else:
        return y

def cos(x):
    return sin(x + pi / 2)

def tan(x):
    try:
        return sin(x) / cos(x)
    except ZeroDivisionError:
        return None

def sinh(x):
    if ops.is_iter(x):
        return np.array(list(map(sin, x)))
    y = ((e ** x) - (e ** -x)) / 2
    y = ops.round_int(y)
    if y.imag == 0:
        return y.real
    else:
        return y

def cosh(x):
    return cos(x * 1j)

def tanh(x):
    return sinh(x) / cosh(x)

def cosec(x):
    try:
        return 1 / sin(x)
    except ZeroDivisionError:
        return None

def sec(x):
    try:
        return 1 / cos(x)
    except ZeroDivisionError:
        return None

def cotan(x):
    try:
        return cos(x) / sin(x)
    except ZeroDivisionError:
        return None

import mathipy._complex as C
def ln(x):
    if ops.is_iter(x):
        return np.array(list(map(ln, x)))
    elif isinstance(x, complex):
        x = C.to_Complex(x)
        return C.Complex(ln(x.r), x.theta)
    if x <= 0:
        raise ValueError('Argument must be positive')
    else:
        return 2 * np.arctanh((x - 1)/(x + 1))

def log(x, base= 10):
    if ops.is_iter(x):
        return np.array(list(map(lambda x: log(x, base), x)))
    elif isinstance(x, complex):
        x = C.to_Complex(x)
        return C.Complex(ln(x.r), x.theta) / ln(base)

    if x <= 0:
        raise ValueError('Argument must be positive')
    elif base <= 1:
        raise ValueError('Base must be greater than 1')
    if base == e:
        return ln(x)
    else:
        log_n = ln(x) / ln(base)
        return ops.round_int(log_n)

def root_n(x, index, return_complex: bool= True):
    if ops.is_iter(x):
        return np.array(list(map(lambda x: root_n(x, index, return_complex), x)))
    if isinstance(x, complex):
        return x ** (1 / index)
    else:
        if x >= 0:
            return x ** (1 / index)
        else:
            if index % 2 == 0:
                return C.Complex(0, root_n(-x)) if return_complex else None
            else:
                return -root_n(-x, index)

def sqrt(x, return_complex: bool= True):
    return root_n(x, 2, return_complex)