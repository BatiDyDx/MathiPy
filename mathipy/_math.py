import numpy as np
import mathipy.functions as F
from mathipy import _complex as C
from mathipy import arithmetic
from mathipy.functions import logarithmic, nroot, trigonometric
from mathipy import statistics as stats
from mathipy import datastr, linalg


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
    if isinstance(n, C.Complex):
        return C.Complex(round_int(n.a), round_int(n.b))
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
    types = (tuple, list, set, np.ndarray, datastr.Queue, datastr.Stack, linalg.Tensor)
    if exclude:
        if is_iter(a = exclude):
            types = tuple(t for t in types if t not in exclude)
        else:
            types = tuple(t for t in types if t != exclude)
    return isinstance(a, types)

def is_scalar(a):
    return isinstance(a, (int, float, complex, C.Complex))

def abs(n):
    if isinstance(n, C.Complex):
        return n.r
    elif isinstance(n, complex):
        return _math.sqrt((n.real)**2 + (n.imag)**2)
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

def summation(f, up_bound, low_bound = 0):
    if up_bound < low_bound:
        return 0
    elif up_bound == low_bound:
        return f(low_bound)    
    else:
        return f(low_bound) + summation(f, up_bound, low_bound + 1)

def product(f, up_bound, low_bound = 1):
    if up_bound < low_bound:
        return 0
    elif up_bound == low_bound:
        return f(low_bound)
    else:
        return f(low_bound) * product(f, up_bound, low_bound + 1)

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
    return F.nroot.NRoot.root(x, return_complex= return_complex)

def root_n(x, n, return_complex):
    return F.nroot.NRoot.root(x, index= n, return_complex= return_complex)

def log(x, base):
    return F.logarithmic.Log.log(x, base=base)

def ln(x):
    return F.logarithmic.Log.ln(x)

def min(iterable):
    return stats.Statistics(iterable).min()

def max(iterable):
    return stats.Statistics(iterable).max()

def mean(iterable):
    return stats.Statistics(iterable).mean()

def probability_of(x, iterable):
    return stats.Statistics(iterable)(x)

def sin(x):
    y = (_math.e ** (1j * x) - _math.e ** (-1j * x)) / 2j
    y = round_int(y)
    if y.imag == 0:
        return y.real
    else:
        return y

def cos(x):
    return sin(x - _math.pi / 2)

def tan(x):
    try:
        return sin(x) / cos(x)
    except ZeroDivisionError:
        return None

def sinh(x):
    return sin(C.Complex(0,1) * x)

def cosh(x):
    return cos(C.Complex(0,1) * x)

def tanh(x):
    return sinh(x) / cosh(x)

# def cosec(x):
#     return Cosec.csc(x)

# def sec(x):
#     return Sec.sec(x)

# def cotan(x):
#     return Cotan.cotan(x)