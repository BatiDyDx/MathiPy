import math
from dataclasses import dataclass, field
from typing import Callable, Dict, Iterable, Optional, Generator, Tuple
from functools import cache, lru_cache
from mathipy import numeric_operations as ops

##### Mathematical constants ###############
math_constants: Dict[str, float] = {
    'e'        :  2.718281828459045,
    'pi'       :  3.141592653589793,
    'pi/2'     :  1.5707963267948966,
    'pi/4'     :  0.785398163397448,
    'pi/6'     :  0.523598775598299,
    '3pi/2'    :  4.71238898038469,
    'tau'      :  6.283185307179586,
    'sqrt2'    :  1.4142135623730951,
    'sqrt3'    :  1.732050807568877,
    'sqrt5'    :  2.23606797749979,
    'phi'      :  1.618033988749894,
    'gamma'    :  0.5772156649015328,
    '.5!'      :  0.886226925452758,
    '2^e'      :  6.58088599101792097085,
    'sqrt(pi)' :  1.77245385090551602729,
    'log2(3)'  :  1.58496250072115618145,
    'e^e'      :  2.66514414269022518865,
    'pi^pi'    :  36.46215960720791177099,
    'e^gamma'  :  1.78107241799019798523,
    'sqrt(e)'  :  1.64872127070012814684,
    'e^(pi/2)' :  4.81047738096535165547,
    'pi^e'     :  22.45915771836104547342,
    'e^pi'     :  2.66514414269022518865,
    '1/pi'     :  0.31830988618379067153,
    '2/pi'     :  0.63661977236758134307,
    '4/pi'     :  1.27323954473516268615,
    'pi^2'     :  9.86960440108935861883,
    '1/e'      :  0.36787944117144232159,
    'i^i'      :  0.20787957635076190854,
}

e:  float = math_constants['e']
pi: float = math_constants['pi']
tau: float = math_constants['tau']

############################################

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


def sum_n_naturals(n: int) -> int:
    return n * (n + 1) // 2


def sum_n_squared_naturals(n: int) -> int:
    return (n * (n + 1) * (2 * n + 1)) // 6


def sum_n_cubed_naturals(n: int) -> int:
    return ((n ** 2) * ((n + 1) ** 2)) // 4


def arithmetic_prog(n: int, a, r):
    return (2 * a + (n - 1) * r) * (n / 2)


def geometric_prog(n: int, a, r):
    return a * (r ** (n + 1) - 1) / (r - 1)


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


def summation_over_set(f: Callable, s: Iterable, **kwargs):
    result = 0
    for i in s:
        result += f(i, **kwargs)
    return result


def productory_over_set(f: Callable, s: Iterable, **kwargs):
    result = 1
    for i in s:
        result *= f(i, **kwargs)
    return result

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


def is_multiple(a: int, b: int) -> bool:
    """Checks if a is multiple of b"""
    return lcm(a, b) == a


def is_divisor(a: int, b: int) -> bool:
    """Checks if b is divisible by a"""
    return gcd(a, b) == b


def coprimes(a: int, b: int) -> bool:
    """
    Returns if two numbers are coprimes.
    Two numbers are said to be coprimes if they
    do not share any prime factor.
    i.e. 20 and 21 are coprimes, since
    20 = 2 x 2 x 5 and 21 = 3 x 7
    >>> coprimes(20, 21)
    True
    >>> coprimes(10, 15)
    False
    """
    return gcd(a, b) == 1


def sci_notation(x: float) -> Tuple[float, int]:
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


def index_of_fib(n: int) -> Optional[int]:
    """
    Returns the index of n in the fibonacci sequence.
    If n is not a fibonacci number, returns None
    :param n:
    :return:
    """
    # TODO
    # Redo the function
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