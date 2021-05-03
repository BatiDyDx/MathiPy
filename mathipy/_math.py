from functools import cache, lru_cache
from typing import Generator, Union, Callable
from dataclasses import dataclass, field
import ctypes
import pathlib
import numpy as np
#import mathipy.config
import mathipy.numeric_operations as ops
from mathipy.polynomial import Polynomial
from mathipy.cfuncs.bin import trigonometry as trig

#_C_funcs = mathipy.config.__load_c_utils(__file__)

e:     float = 2.718281828459045
pi:    float = 3.141592653589793
pi_2:  float = 1.5707963267948966
tau:   float = 6.283185307179586
sqrt2: float = 1.4142135623730951
phi:   float = 1.618033988749894
gamma: float = 0.5772156649015328


@dataclass(init=True, repr=False, eq=True, frozen=True)
class Infinite(float):
    sign: bool = field(default=True, hash=True, compare=True, repr=True)

    def __add__(self, n):
        return self

    def __radd__(self, n):
        return self

    def __sub__(self, n):
        return self

    def __rsub__(self, n):
        return -self

    def __neg__(self):
        return Infinite(neg=(not self.neg))

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
        if self.sign:
            return float('inf')
        else:
            return float('-inf')

    def __str__(self):
        if self.sign:
            return 'inf'
        else:
            return '-inf'


@lru_cache(maxsize=5)
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


def summation(f: Callable, up_bound: int, low_bound: int = 0, **kwargs) -> float:
    if up_bound < low_bound:
        return 0
    elif up_bound == low_bound:
        return f(low_bound, **kwargs)
    else:
        return f(low_bound, **kwargs) + summation(f, up_bound, low_bound + 1, **kwargs)


def product(f: Callable, up_bound: int, low_bound: int = 0, **kwargs) -> float:
    if up_bound < low_bound:
        return 0
    elif up_bound == low_bound:
        return f(low_bound, **kwargs)
    else:
        return f(low_bound, **kwargs) * product(f, up_bound, low_bound + 1, **kwargs)


@np.vectorize
def gcd(a: int, b: int) -> int:
    if a % b == 0:
        return b
    else:
        c: int = a % b
        return gcd(b, c)


@np.vectorize
def lcm(a: int, b: int) -> int:
    d: int = gcd(a, b)
    return (a * b) // d


import math # temporary
def sci_notation(x: float) -> list[float, int]:
    # Take the order of magnitude of x, 
    # then convert it to an int
    order = math.log10(abs(x))
    order = int(ops.floor(order))
    
    # Divide x by its order of magnitude
    mant = x / (10 ** order)

    return [mant, order]


@cache
def fibonacci(n: int) -> int:
    """
    Fibonacci numbers generator
    :param n: generate fibonacci numbers starting by the nth one
    :return: nth fibonacci number
    """
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


def fibonacci_seq(n: int) -> Generator:
    """
    Generator of fibonacci sequence of length n
    :param n: int
    :return: Generator object
    """
    for i in range(n):
        yield fibonacci(i)


def index_of_fib(n: int) -> Union[int, None]:
    """
    Returns the index of n in the fibonacci sequence.
    If n is not a fibonacci number, returns None
    :param n:
    :return:
    """
    seq_len: int = 50
    fibs: list[int] = list(fibonacci_seq(seq_len))
    if fibs[-1] > n:
        return None
    elif n in fibs:
        return fibs.index(n)
    else:
        last_fib: int = fibs[-1]
        while last_fib < n:
            new_fib = fibonacci(seq_len)
            if new_fib == n:
                return seq_len
            last_fib = new_fib
            seq_len += 1


@np.vectorize
def abs(x):
    if ops.is_scalar(x):
        if isinstance(x, complex):
            # Since native python complex numbers do not have the module
            # attribute, it is calculated either if it's complex or mpy.Complex
            return sqrt(x.real ** 2 + x.imag ** 2)
        if x < 0:
            return -x
        else:
            return x


@np.vectorize
@cache
def factorial(n: int) -> int:
    if not ops.is_integer(n):
        raise TypeError(f'n must be int, received {n.__class__.__name__}')
    elif n < 0:
        raise ValueError('Cannot calculate factorial of negative numbers')
    return factorial(n - 1) * n if n > 1 else 1
    # _C_funcs.factorial.argtypes = (ctypes.c_int,)
    # _C_funcs.factorial.restype = ctypes.c_int
    # return _C_funcs.factorial(n)    


@np.vectorize
def differential(x, magnitude: int = 10):
    h: float = 10 ** -magnitude
    delta_x = x + x * h
    return delta_x


@np.vectorize
def sin(x, return_complex: bool = False):
    def complex_sin(z):
        return (e ** (1j * z) - e ** (-1j * z)) / 2j

    if return_complex or x.imag != 0:
        return complex_sin(x)
    else:
        return trig.sin(x)


@np.vectorize
def cos(x, return_complex: bool = False):
    def complex_cos(z):
        return (e ** (1j * z) + e ** (-1j * z)) / 2

    if return_complex or x.imag != 0:
        return complex_cos(x)
    else:
        return trig.cos(x)


@np.vectorize
@ops.handleZeroDivision
def tan(x, return_complex: bool = False):
    def complex_tan(z):
        y = (e ** (1j * z) - e ** (-1j * z)) * -1j
        y /= (e ** (1j * z) + e ** (-1j * z))
        return y

    if return_complex or x.imag != 0:
        return complex_tan(x)
    else:
        return trig.tan(x)


@np.vectorize
def arcsin(x, return_complex: bool = False):
    def complex_arcsin(z):
        y = z * 1j + (1 - z ** 2) ** .5
        y = ln(y) / 1j
        return y
    if return_complex or x.imag != 0:
        return complex_arcsin(x)
    else:
        return trig.arcsin(x)


@np.vectorize
def arccos(x, return_complex: bool = False):
    def complex_arccos(z):
        y = z + (z ** 2 - 1) ** .5
        y = ln(y) / 1j
        return y

    if return_complex or x.imag != 0:
        return complex_arccos(x)
    else:
        if x == 0:
            return pi_2
        return trig.arcsin(x)

@np.vectorize
def arctan(x):
    return trig.arctan(x)


@np.vectorize
def cosh(x):
    return cos(x * 1j)


@np.vectorize
def sinh(x):
    y = ((e ** x) - (e ** -x)) / 2
    y = ops.round_if_close(y)
    if isinstance(x, complex):
        return y
    return y.real


@np.vectorize
def tanh(x):
    return sinh(x) / cosh(x)


@np.vectorize
@ops.handleZeroDivision
def cosec(x):
    return 1 / sin(x)


@np.vectorize
@ops.handleZeroDivision
def sec(x):
    return 1 / cos(x)


@np.vectorize
@ops.handleZeroDivision
def cotan(x):
    return cos(x) / sin(x)


@np.vectorize
@ops.handleZeroDivision
def cosech(x):
    return 1 / sinh(x)


@np.vectorize
def sech(x):
    return 1 / cosh(x)


@np.vectorize
@ops.handleZeroDivision
def cotanh(x):
    return cosh(x) / sinh(x)


from mathipy import _complex


@np.vectorize
def ln(x):
    if x == 0:
        return -Infinite()
    
    if isinstance(x, complex):
        x = _complex.to_Complex(x)
        return _complex.Complex(ln(x.r), x.theta)
    elif x < 0:
        return np.nan
    else:
        return 2 * np.arctanh((x - 1)/(x + 1))


@np.vectorize
def log(x, base: Union[int, complex] = 10):
    if base.real <= 1 and base.imag == 0:
        raise ValueError('Base must be greater than 1')
    return ln(x) / ln(base)


@np.vectorize
def root_n(x, index: int, return_complex: bool = True):
    if isinstance(x, complex):
        return x ** (1 / index)
    else:
        if x >= 0:
            return x ** (1 / index)
        else:
            if index % 2 == 0:
                return _complex.Complex(0, root_n(-x, index)) if return_complex else np.nan
            else:
                return -root_n(-x, index)


@np.vectorize
def sqrt(x, return_complex: bool = True):
    return root_n(x, 2, return_complex)
