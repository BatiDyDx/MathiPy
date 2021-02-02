import numpy as np
from mathipy import arithmetic 
from mathipy.functions import logarithmic
from mathipy.functions import nroot
from mathipy.functions import trigonometric
from mathipy import _complex 
from mathipy import statistics as stats
from mathipy import datastr

def binomial(a, b, exp):
    if isinstance(b, _complex.Complex):
        pass

def pascal_triangle(n):
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

def round_int(n, thresh_exp = 3):
    floor_thresh = 1 * (10 ** -thresh_exp)
    ceil_thresh = 1 - floor_thresh
    if isinstance(n, _complex.Complex):
        return _complex.Complex(round_int(n.a), round_int(n.b))
    elif isinstance(n, complex):
        return complex(round_int(n.real), round_int(n.imag))
    elif is_iter(n):
        return list(map(round_int, n))
    if n >= 0:
        if n % 1 >= ceil_thresh or n % 1 <= floor_thresh:
            return int(round(n))
        else: return n
    elif n < 0:
        return -round_int(-n)

def is_iter(a, exclude = None) -> bool:
    types = (tuple, list, set, np.ndarray, datastr.Queue, datastr.Stack)
    if exclude:
        if is_iter(a = exclude):
            types = tuple(t for t in types if t not in exclude)
        else:
            types = tuple(t for t in types if t != exclude)
    return isinstance(a, types)

def is_scalar(a):
    return isinstance(a, (int, float, complex, _complex.Complex))

def abs(n):
    if isinstance(n, _complex.Complex):
        return n.r
    elif isinstance(n, complex):
        return np.sqrt((n.real)**2 + (n.imag)**2)
    elif is_iter(n):
        return list(map(abs, n))
    else:
        if n < 0:
            return - n
        else:
            return n

def fibonacci(n):
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

def summation(arg, upper_bound, lower_bound = 0, **kwargs):
    var = kwargs.get('var_name', 'x')
    if isinstance(arg, (int, float, complex, _complex.Complex)):
        arg = arithmetic.Constant(arg)

    if upper_bound < lower_bound:
        return 0

    if upper_bound == lower_bound:
        if hasattr(arg, '__call__'):
            return arg(lower_bound)
        else:
            return arg.evaluate({var: lower_bound})
    else:
        if hasattr(arg, '__call__'):
            return arg(upper_bound) + summation(arg, upper_bound - 1, lower_bound)
        else:
            return arg.evaluate({var: upper_bound}) + summation(arg, upper_bound - 1, lower_bound, var_name = var)

def product(arg, upper_bound, lower_bound = 1, **kwargs):
    var = kwargs.get('var_name', 'x')
    if isinstance(arg, (int, float, complex, _complex.Complex)):
        arg = arithmetic.Constant(arg)

    if upper_bound < lower_bound:
        return 0

    if upper_bound == lower_bound:
        if hasattr(arg, '__call__'):
            return arg(lower_bound)
        else:
            return arg.evaluate({var: lower_bound})
    else:
        if hasattr(arg, '__call__'):
            return arg(upper_bound) * product(arg, upper_bound - 1, lower_bound)
        else:
            return arg.evaluate({var: upper_bound}) * product(arg, upper_bound - 1, lower_bound, var_name = var)

def gcd(a, b):
    if a % b == 0:
        return b
    else:
        c = a % b
        return gcd(b, c)

def mcm(a, b):
    d = gcd(a,b)
    return (a * b) // d

def sqrt(x, return_complex = True):
    return nroot.NRoot.root(x, return_complex= return_complex)

def root_n(x, n, return_complex):
    return nroot.NRoot.root(x, index= n, return_complex= return_complex)

def log(x, base):
    return logarithmic.Log.log(x, base=base)

def ln(x):
    return logarithmic.Log.ln(x)

def min(iterable):
    return stats.Statistics(iterable).min()

def max(iterable):
    return stats.Statistics(iterable).max()

def mean(iterable):
    return stats.Statistics(iterable).mean()

def probability_of(x, iterable):
    return stats.Statistics(iterable)(x)

def sin(x):
    y = (arithmetic.e ** (1j * x) - arithmetic.e ** (-1j * x))
    y /=  2j
    y = round_int(y)
    if y.imag != 0:
        return y
    else:
        return y.real

def cos(x):
    y = ((arithmetic.e ** (1j * x) + arithmetic.e ** (-1j * x))) / 2
    y = round_int(y)
    if y.imag != 0:
        return y
    else:
        return y.real

def tan(x):
    return (sin(x) / cos(x))

# def cosec(x):
#     return Cosec.csc(x)

# def sec(x):
#     return Sec.sec(x)

# def cotan(x):
#     return Cotan.cotan(x)