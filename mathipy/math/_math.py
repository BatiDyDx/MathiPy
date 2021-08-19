from functools import cache, lru_cache
from typing import Dict, Generator, Optional, Union, Callable
from dataclasses import dataclass, field
import ctypes
import pathlib
import numpy as np
#import mathipy.config
import mathipy.numeric_operations as ops
from mathipy.config import Scalar, Real

#_C_funcs = mathipy.config.__load_c_utils(__file__)

"""Deprecated file"""

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


from mathipy.math.complex_math import to_polar

@ops.vectorize
def ln(x: Scalar):
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
def log(x, base: Scalar = 10):
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



