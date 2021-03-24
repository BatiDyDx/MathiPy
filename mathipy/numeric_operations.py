from functools import wraps
import numpy as np

def kwargsParser(kwargs: dict, p: tuple, r=None):
    dft = None
    for parameter in p:
        value = kwargs.get(parameter, dft)
        if value is not dft:
            return value
        continue
    return r

@np.vectorize
def round_if_close(n: any, thresh_exp: int= 3) -> any:
    """Round int doc"""
    floor_thresh = 10.0 ** -thresh_exp
    ceil_thresh = 1 - floor_thresh
    if isinstance(n, complex):
        from mathipy import Complex
        #x = Complex(round_if_close(n.real, thresh_exp), round_if_close(n.imag, thresh_exp))
        x = Complex(round_if_close(n.real, thresh_exp), round_if_close(n.imag, thresh_exp))
        return x
    if n >= 0:
        if n % 1 >= ceil_thresh or n % 1 <= floor_thresh:
            return float(round(n))
        else: return n
    elif n < 0:
        return -round_if_close(-n, thresh_exp)

def is_iterable(it: any, exclude= None) -> bool:
    if hasattr(it, '__iter__'):
        if exclude:
            if isinstance(it, exclude):
                return False
            else: return True
        else: return True
    else: return False

def is_scalar(a: any) -> bool:
    types = (int, float, complex, np.integer, np.floating, np.complexfloating)
    return isinstance(a, types)

from mathipy import _math
def handleZeroDivision(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ZeroDivisionError:
            return _math.Infinite()
    return wrapper

@np.vectorize
def variation(n: int, k: int, repetitions: bool= False) -> int:
    if not k <= n: raise ValueError('k must be less than n')
    if repetitions:
        return n ** k
    else:
        return _math.factorial(n) // _math.factorial(n - k)

@np.vectorize
def permutation(n: int, k: (int, None)= None, circular: bool= False) -> int:
    if not k:
        if not circular: return _math.factorial(n) 
        else: return _math.factorial(n - 1)
    else:
        denominator = 1
        for el in range(k):
            denominator *= _math.factorial(el)
        return _math.factorial(n) // denominator

@np.vectorize
def combinatorial(n: int, k: int, repetitions: bool= False) -> int:
    if not repetitions:
        if k >= n: raise ValueError('n must be greater than p')
        num = _math.factorial(n)
        den = _math.factorial(k) * _math.factorial(n - k)
        return num // den
    else:
        return combinatorial(n + k - 1, k, repetitions= False)

def configIter(f: callable) -> callable:
    @wraps(f)
    def iterWrapper(*args, **kwargs) -> any:
        args = [list(arg) for arg in args]
        iterable = list(sum(args, []))
        return f(iterable, **kwargs)
    return iterWrapper

@configIter
def min(args):
    """
    Return the minimum value of a series of iterable objects
    """
    min_n = float('inf')
    for i in args:
        if i == None: pass
        elif i < min_n: min_n = i
    return min_n

@configIter
def max(args):
    max_n = float('-inf')
    for i in args:
        if i == None: pass
        elif i > max_n: max_n = i
    return max_n

@configIter
def mean(args):
    """
    Return the mean of a series of iterable objects
    """
    return sum(args) / len(args)

@configIter
def median(args):
    args.sort()
    n = len(args)
    if n % 2 == 1:
        return args[n // 2]
    else:
        x_1, x_2 = args[(n // 2) - 1], args[n // 2]
        return (x_1 + x_2) / 2 

@configIter
def mode(args) -> list:
    items = {item: args.count(item) for item in set(args)}
    mx_repetitions = max(items.values())
    modes = [k for k in items.keys() if items[k] == mx_repetitions]
    return modes

@configIter
def frequency(args, x, f_type='absolute'):
    count = args.count(x)
    if f_type == 'absolute':
        return count
    elif f_type == 'relative':
        return count / len(args)

@configIter
def std(args) -> float:
    n = len(iterable)
    m = mean(iterable)
    x_1 = 1 / n
    f = (lambda x: (iterable[x] - m) ** 2)
    x_2 = _math.summation(f, up_bound = n - 1, low_bound = 0)
    std = _math.sqrt(x_1 * x_2)
    return std