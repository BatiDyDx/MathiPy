from functools import wraps
from typing import Any, Callable, Iterable, Union, Tuple, Optional
import ctypes
import pathlib
import numpy as np
#import mathipy.config

#_C_funcs = mathipy.config.__load_c_utils(__file__)

def kwargsParser(kwargs: dict[str, Any], params: Tuple[str, ...], default: Optional[Any] = None):
    for parameter in params:
        value = kwargs.get(parameter)
        if value is not None:
            return value
        continue
    return default


@np.vectorize
def round_if_close(n: Union[float, complex], thresh_exp: int = 3, return_int: bool = False) -> Union[float, complex]:
    """
    If n is close to a whole number, it rounds it
    :param n: number to be rounded if close enough to an integer
    :param thresh_exp: exponent of the threshold for deciding if n is rounded or not
    :param return_int: if True (default is False), the return is converted to an int. Else, returns a float
    :return: returns a rounded float when the number passes the condition. If n is a complex number, it rounds its
    real and imaginary part. round_if_close behaves likes a universal function:
    >>> round_if_close([1.99999, 3.11, 0.999 + 6j])
    [2, 3.11, 1 + 6j]
    """
    floor_thresh: float = 10.0 ** -thresh_exp
    ceil_thresh: float = 1 - floor_thresh
    if isinstance(n, complex):
        from mathipy import Complex
        x = Complex(round_if_close(n.real, thresh_exp, return_int), round_if_close(n.imag, thresh_exp, return_int))
        return x
    if n >= 0:
        if n % 1 >= ceil_thresh or n % 1 <= floor_thresh:
            rounded_n = float(round(n))
            return int(rounded_n) if return_int else rounded_n
        else:
            return n
    elif n < 0:
        return -round_if_close(-n, thresh_exp, return_int)


def is_iterable(obj: Any, exclude: tuple[type, ...] = None) -> bool:
    if hasattr(obj, '__iter__'):
        if exclude:
            if isinstance(obj, exclude):
                return False
            else:
                return True
        else:
            return True
    else:
        return False


def is_scalar(n: Any) -> bool:
    types: tuple[type] = (int, float, complex, np.integer, np.floating, np.complexfloating)
    return isinstance(n, types)

def is_integer(n: Any) -> bool:
    return type(n) is int or isinstance(n, np.integer)

def get_error(
        f: callable,
        g: callable,
        /,
        iterations: int = 1000,
        *,
        sample_test: Optional[Iterable] = None,
        print_on_iteration=True,
        squared_error=False,
        fargs: dict = None,
        gargs: dict = None
):
    if sample_test is None:
        sample_test = np.random.uniform(size=iterations)

    fargs = fargs if fargs else {}
    gargs = gargs if gargs else {}

    error: list[float] = list()
    exp = 2 if squared_error else 1

    for i in range(iterations):
        x = sample_test[i]
        r1 = f(x, **fargs)
        r2 = g(x, **gargs)

        diff = abs(r1 - r2) ** exp
        error.append(diff)
        if print_on_iteration:
            print('x is:    ', x)
            print('f(x) is: ', r1)
            print('g(x) is: ', r2)
            print('Difference is: ', diff)

    error_type_str = 'Mean squared error is: ' if squared_error else 'Mean error is: '
    print(error_type_str, mean(error))

from mathipy import _math
import math

def round_significant_figures(n: float, sigf: int):
    if not is_integer(sigf):
        raise TypeError(f'significant figures must be an integer, received {sigf.__class__.__name__}')
    if sigf < 0:
        raise ValueError(f'significant figures must be positive, received {sigf}')
    
    return round(n,  sigf - int(math.floor(math.log10(abs(n)))) - 1)


def handleZeroDivision(f: Callable) -> Callable:
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ZeroDivisionError:
            return _math.Infinite()
    return wrapper


@np.vectorize
def trunc(n, decimals=0):
    if not is_integer(decimals):
        raise TypeError('decimal places must be an integer')
    elif decimals < 0:
        raise ValueError('decimal places has to greater or equal to 0')
    elif decimals == 0:
        return n - mantissa(n)

    factor = 10.0 ** decimals
    return floor(n * factor) / factor


@np.vectorize
def floor(x):
    return x - mantissa(x)


@np.vectorize
def ceil(x):
    return -floor(-x)


@np.vectorize
def mantissa(x):
    return x % 1


@np.vectorize
def variation(n: int, k: int, repetitions: bool = False) -> int:
    if repetitions:
       return n ** k
    else:
       return _math.factorial(n) // _math.factorial(n - k)
    # if k > n: raise ValueError('k must be less than n')
    
    # _C_funcs.variation.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.c_bool)
    # _C_funcs.variation.restype = ctypes.c_int
    
    # return _C_funcs.variation(n, k, repetitions)


@np.vectorize
def permutation(n: int, k: Optional[int] = None, circular: bool = False) -> int:
    if not k:
        if circular: return _math.factorial(n - 1)
        else: return _math.factorial(n)
    else:
        denominator = 1
        for el in range(k):
            denominator *= _math.factorial(el)
        return _math.factorial(n) // denominator


@np.vectorize
def combinatorial(n: int, k: int, repetitions: bool = False) -> int:
    if not repetitions:
        if k >= n: raise ValueError('n must be greater than p')
        num = _math.factorial(n)
        den = _math.factorial(k) * _math.factorial(n - k)
        return num // den
    else:
        return combinatorial(n + k - 1, k, repetitions=False)


def configIter(f: Callable[[Iterable], Any]) -> Callable[[Iterable], Any]:
    @wraps(f)
    def iterWrapper(*args, **kwargs):
        args = [list(arg) for arg in args]
        iterable = list(sum(args, []))
        return f(iterable, **kwargs)
    return iterWrapper


@configIter
def min(args: Iterable[Union[int, float]]):
    """
    Return the minimum value of a series of iterable objects
    """
    min_n = float('inf')
    for i in args:
        if i is None:
            continue
        elif i < min_n:
            min_n = i
    return min_n

@configIter
def max(args: Iterable[Union[int, float]]):
    max_n = float('-inf')
    for i in args:
        if i is None:
            pass
        elif i > max_n:
            max_n = i
    return max_n

@configIter
def mean(args: Iterable[Union[int, float]]) -> float:
    """
    Return the mean of a series of iterable objects
    """
    return sum(args) / len(args)

@configIter
def median(args: Iterable[Union[int, float]]):
    args.sort()
    n: int = len(args)
    if n % 2 == 1:
        return args[n // 2]
    else:
        x_1, x_2 = args[(n // 2) - 1], args[n // 2]
        return (x_1 + x_2) / 2 

@configIter
def mode(args: Iterable[Union[int, float]]) -> list:
    items: dict[Union[int, float], int] = {item: args.count(item) for item in set(args)}
    mx_repetitions = max(items.values())
    modes: list[Union[int, float]] = [k for k in items.keys() if items[k] == mx_repetitions]
    return modes

@configIter
def frequency(args: Iterable[Union[int, float]], x: Union[int, float], f_type: str = 'absolute'):
    count = args.count(x)
    if f_type == 'absolute':
        return count
    elif f_type == 'relative':
        return count / len(args)

@configIter
def std(args: Iterable[Union[int, float]]) -> float:
    n: int = len(args)
    m: float = mean(args)
    x_1: float = 1 / n
    f: Callable[[int], float] = (lambda x: (args[x] - m) ** 2)
    x_2: float = _math.summation(f, up_bound = n - 1, low_bound = 0)
    return _math.sqrt(x_1 * x_2)
