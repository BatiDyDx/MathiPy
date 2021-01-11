import numpy as np
from mathipy import arithmetic 
from mathipy.functions import logarithmic 
from mathipy.functions import trigonometric
from mathipy import _complex 
from mathipy import statistics as stats
from mathipy import datastr

def round_int(n, neg = False):
    ceil_thresh = 0.99
    floor_thresh = 0.001
    if isinstance(n, _complex.Complex):
        return _complex.Complex(round_int(n.a), round_int(n.b))
    elif isinstance(n, complex):
        return complex(round_int(n.real), round_int(n.imag))
    elif isinstance(n, (tuple, list, set, np.ndarray)):
        return [round_int(i) for i in n]
    if n > 0:
        if n % 1 >= ceil_thresh or n % 1 <= floor_thresh:
            return int(round(n)) if not neg else -int(round(n))
    elif n < 0:
        return round_int(abs(n), True)

def is_iter(a, exclude = None) -> bool:
    types = (tuple, list, set, np.ndarray, datastr.Queue, datastr.Stack)
    if exclude:
        if is_iter(a = exclude):
            types = tuple(t for t in types if t not in exclude)
        else:
            types = tuple(t for t in types if t != exclude)
    return isinstance(a, types)

def abs(n):
    if isinstance(n, _complex.Complex):
        return n.r
    elif isinstance(n, complex):
        return np.sqrt((n.real)**2 + (n.imag)**2)
    elif isinstance(n, (list, tuple, set)):
        return [abs(i) for i in n]
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

def log(x, base):
    return Log.log(x, base=base)

def ln(x):
    return Log().ln(x)

def min(iterable):
    return stats.Statistics(iterable).min()

def max(iterable):
    return stats.Statistics(iterable).max()

def mean(iterable):
    return stats.Statistics(iterable).mean()

def probability_of(x, iterable):
    return stats.Statistics(iterable)(x)

def sin(x):
    return np.sin(x)

def cos(x):
    return np.cos(x)

def tan(x):
    return np.tan(x)

# def cosec(x):
#     return Cosec.csc(x)

# def sec(x):
#     return Sec.sec(x)

# def cotan(x):
#     return Cotan.cotan(x)