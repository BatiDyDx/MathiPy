from functools import cache, lru_cache
from typing import Generator, Optional, Union, Callable
from dataclasses import dataclass, field
import ctypes
import pathlib
import numpy as np
#import mathipy.config
import mathipy.numeric_operations as ops

#_C_funcs = mathipy.config.__load_c_utils(__file__)

e:     float = 2.718281828459045
pi:    float = 3.141592653589793
pi_2:  float = 1.5707963267948966
tau:   float = 6.283185307179586
sqrt2: float = 1.4142135623730951
phi:   float = 1.618033988749894
gamma: float = 0.5772156649015328


@dataclass(init=True, repr=True, eq=True, frozen=True)
class Infinite(float):
    sign: bool = field(default=True, hash=True, compare=True, repr=False)

    def __add__(self, n):
        return self

    def __radd__(self, n):
        return self

    def __sub__(self, n):
        return self

    def __rsub__(self, n):
        return -self

    def __neg__(self):
        return Infinite(sign=(not self.sign))

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
            return '+inf'
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


def productory(f: Callable, up_bound: int, low_bound: int = 0, **kwargs) -> float:
    if up_bound < low_bound:
        return 0
    elif up_bound == low_bound:
        return f(low_bound, **kwargs)
    else:
        return f(low_bound, **kwargs) * productory(f, up_bound, low_bound + 1, **kwargs)


@ops.vectorize
def gcd(a: int, b: int) -> int:
    if a % b == 0:
        return b
    else:
        c: int = a % b
        return gcd(b, c)


@ops.vectorize
def lcm(a: int, b: int) -> int:
    d: int = gcd(a, b)
    return (a * b) // d


import math # temporary
def sci_notation(x: float) -> tuple[float, int]:
    """
    Given a number, it returns two numbers that
    correspond to its scientific notation, the mantissa
    and the order of magnitude
    i.e. 150 = 1.5 * 10 ^ 2, where the mantissa is 1.5
    and the order of magnitude is 2.
    """
    # Take the order of magnitude of x, 
    # then convert it to an int
    order = math.log10(abs(x))
    order = int(ops.floor(order))
    
    # Divide x by its order of magnitude
    mant = x / (10 ** order)

    return (mant, order)


@cache
def fibonacci(n: int) -> int:
    """
    Fibonacci numbers generator
    :param n: generate fibonacci numbers starting by the nth one
    :return: nth fibonacci number
    """
    if not ops.is_integer(n):
        raise TypeError(f'n must be an integer, received {n =}')
    
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


@ops.vectorize
def abs(x):
    """
    Returns the distance from the origin of a number
    For real numbers, calculating absolute values is equal to 
    returning the positive of a number.
    For example: abs(1) = 1, abs(-2) = 2
    With complex numbers, absolute values are calculated with
    Pythagoras' Theorem, where the legs of the triangle are the real
    and imaginary parts of the number, and the hypotenuse is the absolute
    value of it
    >>> abs(1j)
    1
    >>> abs(3 + 4j)
    5
    """
    return sqrt(x.real ** 2 + x.imag ** 2)


@ops.vectorize
@cache
def factorial(n: int) -> int:
    """
    The factorial of a natural number is
    defined recursively as n! = n(n-1)!,
    where 1! = 1 = 0! are the base cases.
    Its definition is used for combinatorics,
    where the factorial of n is the number of possible
    arranges for n elements.
    >>> factorial(5)
    120
    >>> factorial(0)
    1
    """
    
    if not ops.is_integer(n):
        raise TypeError(f'n must be an integer, received an {n.__class__.__name__}')
    elif n < 0:
        raise ValueError('Cannot calculate factorial of negative numbers')
    
    return factorial(n - 1) * n if n > 1 else 1
    # _C_funcs.factorial.argtypes = (ctypes.c_int,)
    # _C_funcs.factorial.restype = ctypes.c_int
    # return _C_funcs.factorial(n)    


@ops.vectorize
@cache
def subfactorial(n: int) -> int:
    """
    The subfactorial is recursively defined for natural numbers (including 0) as: 
    
    - !n = !(n-1)n + (-1)^n, n >= 1, where !0 = 1 is the base case for 
    the recursion, or;
    
    - !n = (n-1)(!(n-1)+!(n-2)), n >= 2, where !0 = 1, !1 = 0 are the 
    base cases for the recursion.
    """
    if not ops.is_integer(n):
        raise TypeError(f'n must be an integer, received an {n.__class__.__name__}')
    elif n < 0:
        raise ValueError('Cannot calculate factorial of negative numbers')
    
    if n == 1:
        return 0
    elif n == 0:
        return 1
        
    return (n - 1) * (subfactorial(n - 1) + subfactorial(n - 2))


from mathipy.math.complex_math import to_polar


@ops.vectorize
def ln(x):
    """
    The natural logarithm, or log base e, is
    defined as the inverse of e^x, so as:
    ln(x) = y <==> e^y = x
    
    >>> ln(1)
    0
    >>> ln(e^2)
    2
    >>> ln(-1)
    np.nan
    >>> ln(0)
    -inf
    """
    if x == 0:
        return -Infinite()
    
    if isinstance(x, complex):
        r, theta = to_polar(x)
        return ln(r) + theta * 1j
    elif x < 0:
        return np.nan
    else:
        return 2 * np.arctanh((x - 1)/(x + 1))


@ops.vectorize
def log(x, base: Union[int, complex] = 10):
    """
    The logarithm operation is defined as:
    log_b(x) = y <==> b^y = x
    Bases can be any real number greater or equal to 1,
    or a complex number
    
    >>> log(64, base = 2)
    6
    >>> log(0.00001)
    -5
    >>> log(0)
    -inf
    >>> log(-4)
    np.nan
    >>> log(10, base = 2 + 1j)
    (2.1482252561393507-1.2377234261839685j)
    """
    if base.real <= 1 and base.imag == 0:
        raise ValueError('Base must be greater than 1')
    return ln(x) / ln(base)


@ops.vectorize
def root_n(x, index: int, return_complex: bool = True):
    """
    Root of n index for real or complex numbers.
    When the index is even, there are no real roots for
    negative numbers, so if return_complex is True, it
    returns the complex root, else returns np.nan. This
    does not happen when the index is odd, so the function 
    behaves the same, no matter what the return_complex parameter is
    
    >>> root_n(16, 4)
    2
    >>> root_n(-27, 3, True)
    -3
    >>> root_n(-27, 3, False)
    -3
    >>> root_n(-4, 2, True)
    2j
    >>> root_n(-4, 2, False)
    np.nan
    """
    
    if x.real >= 0 or x.imag != 0:
        return x ** (1 / index)
    else:
        if index % 2 == 0:
            return (0 + root_n(-x, index) * 1j) if return_complex else np.nan
        else:
            return -root_n(-x, index)


@ops.vectorize
def sqrt(x, return_complex: bool = True):
    """
    Square root function for real or complex numbers.
    If return_complex is True, then returns complex
    values for square roots of negative numbers. Else,
    returns np.nan.
    sqrt(x) is equivalent to calling root_n(x, 2)
    
    >>> sqrt(9)
    3
    >>> sqrt(-16, True)
    4j
    >>> sqrt(-16, False)
    np.nan
    """
    return root_n(x, 2, return_complex)


@ops.vectorize
def trunc(n: float, decimals: int = 0) -> float:
    """
    Truncates a number, to the decimals indicated.
    :param n: number to be truncated
    :param decimals: decimals to which n is truncated
    :return: truncated n
    """
    if not ops.is_integer(decimals):
        raise TypeError('decimal places must be an integer')
    elif decimals < 0:
        raise ValueError('decimal places has to greater or equal to 0')
    elif decimals == 0:
        return n - mantissa(n)

    factor = 10.0 ** decimals
    return floor(n * factor) / factor


@ops.vectorize
def floor(x: Union[int, float]) -> Union[int, float]:
    """
    Floor function. Rounds to the nearest lower integer
    >>> floor(1.5)
    1.0
    >>> floor(-3.0)
    -3.0
    """
    return x - mantissa(x)


@ops.vectorize
def ceil(x: Union[int, float]) -> Union[int, float]:
    """
    Ceil function. Rounds to the nearest greater integer
    >>> ceil(10.3)
    11.0
    >>> floor(0)
    0
    """
    return -floor(-x)


@ops.vectorize
def mantissa(x: Union[int, float]) -> float:
    """
    Mantissa function. Returns the floating value
    of a number
    >>> mantissa(1.432523)
    0.432523
    >>> mantissa(0.3)
    0.3
    """
    return x % 1


@ops.vectorize
def variation(n: int, k: int, repetitions: bool = False) -> int:
    if repetitions:
       return n ** k
    else:
       return factorial(n) // factorial(n - k)
    # if k > n: raise ValueError('k must be less than n')
    
    # _C_funcs.variation.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.c_bool)
    # _C_funcs.variation.restype = ctypes.c_int
    
    # return _C_funcs.variation(n, k, repetitions)


@ops.vectorize
def permutation(n: int, k: Optional[int] = None, circular: bool = False) -> int:
    if not k:
        if circular: return factorial(n - 1)
        else: return factorial(n)
    else:
        denominator = 1
        for el in range(k):
            denominator *= factorial(el)
        return factorial(n) // denominator


@ops.vectorize
def combinatorial(n: int, k: int, repetitions: bool = False) -> int:
    if not repetitions:
        if k >= n: raise ValueError('n must be greater than p')
        num = factorial(n)
        den = factorial(k) * factorial(n - k)
        return num // den
    else:
        return combinatorial(n + k - 1, k, repetitions=False)


@ops.vectorize
def maximum(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Returns the maximum between two elements.
    Behaves like a universal function.
    """
    return (a >= b) * a + b * (a < b)


@ops.vectorize
def minimum(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Returns the minimum between two elements.
    Behaves like a universal function.
    """
    return (a <= b) * a + b * (a > b)
