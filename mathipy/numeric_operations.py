import math
from functools import wraps
from mathipy.config import Scalar
from typing import Any, Callable, Dict, Iterable, Sequence, TypeVar, Union, Tuple, Optional
import numpy as np
import mathipy.math.statistics

Args = TypeVar('Args')
KwArgs = TypeVar('KwArgs')
Return = TypeVar('Return')

func = Callable[..., Return]
ufunc = Callable[..., Union[Return, Iterable[Return]]]

def vectorize(f: func) -> ufunc:
    """
    Vectorize uses the numpy vectorize function
    to create universal functions. However, numpy
    implementation always returns ndarrays, which is
    not the intention.
    For example, let inc be the increment function, 
    and vec_inc the vectorized version of inc, 
    via numpy.vectorize, then
    >>> type(inc(1))
    int
    >>> type(vec_inc([1]))
    numpy.ndarray
    >>> type(vec_inc(1))
    numpy.ndarray
    
    As seen in the example, numpy vectorized functions
    return ndarrays even when the return value should
    be a scalar.

    This way, with mpy.vectorize, the desired output
    type is always acquired
    >>> type(inc(1))
    int
    >>> type(vec_inc([1]))
    np.ndarray
    >>> type(vec_inc(1))
    int
    """
    vfunc = np.vectorize(f)
    def vectorize_wrapper(*args: Args, **kwargs):
        result = vfunc(*args, **kwargs)
        # If the return of the function is a scalar, i.e np.array(2)
        # return it as a scalar.
        return result.item() if (result.size == 1 and result.shape == ()) else result
    return vectorize_wrapper

K = TypeVar('K')
V = TypeVar('V')
def kwargsParser(kwargs: Dict[K, V], params: Tuple[K, ...], default: Optional[V] = None) -> V:
    """
    Receives a dictionary and a sequence of keys and returns the
    value of the first key that is in the dictionary. If none of
    the keys are in the dictionary, returns the default value
    passed as optional parameter.

    The idea is to be able to get the value from a dictionary, when the
    key may have different names. 
    >>> kwargsParser({'color': 'red', 'size': 10}, ('c', 'colour', 'color'), 'blue')
    'red'
    >>> kwargsParser({'color': 'red', 'size': 10}, ('c', 'colour'), 'blue')
    'blue'

    """
    for parameter in params:
        value = kwargs.get(parameter)
        if value is None:
            continue
        return value
    return default

X = TypeVar('X')
def fold(f: Callable[[X, X], X], n: X, x: Sequence[X]) -> X:
    """
    Fold operating recursive pattern. f must be a
    closed operation in x, and n the neutral element
    of the operation
    fold : (X -> X) X List(X) -> X
    >>> fold(lambda x,y: x * y, 1, [2,3,5,1])
    30
    >>> fold(OR, False, [False, True, True, False])
    True
    >>> fold(AND, True, [False, True, True, False])
    False
    """
    if len(x) == 0:
        return n
    else:
        return f(x[0], fold(f, n, x[1:]))

Y = TypeVar('Y')
def mapIf(f: Callable[[X], Y], p: Callable[[X], bool], x: Iterable[X]) -> np.ndarray:
    """
    Applies the function f to every element
    in x that evaluates to True when passed to the
    predicate p. If an element evaluates to False,
    the element is left unchanged
    """
    def if_condition(x):
        return f(x) if p(x) else x
    
    computed_list = map(if_condition, x)
    return np.array(list(computed_list))


@vectorize
def round_if_close(n: Scalar, thresh_exp: int = 3, return_int: bool = False) -> Scalar:
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
        x = round_if_close(n.real, thresh_exp, return_int)
        y = round_if_close(n.imag, thresh_exp, return_int)
        return x + y * 1j

    if n >= 0:
        if n % 1 >= ceil_thresh or n % 1 <= floor_thresh:
            rounded_n = float(round(n))
            return int(rounded_n) if return_int else rounded_n
        else:
            return n

    elif n < 0:
        return -round_if_close(-n, thresh_exp, return_int)


def is_iterable(obj: Any, exclude: Optional[Tuple[type, ...]] = None) -> bool:
    """
    Recieves an object and checks if it is iterable by
    looking for the __iter__ method on the object.
    If exclude is provided, is_iterable will evaluate
    to False is the object is instance of any of the types
    in exclude.
    >>> is_iterable([1,2,3,])
    True
    >>> is_iterable([1,2,3,], exclude=(list,))
    False
    >>> is_iterable(1)
    False
    """
    exclude = exclude if exclude is not None else ()
    if hasattr(obj, '__iter__'):
        return not isinstance(obj, exclude)
    else:
        return False


def is_scalar(n: Any) -> bool:
    """
    is_scalar checks if the input is a scalar magnitude.
    Scalar maagnitudes are defined as adimensional magnitudes,
    this is, they do not possess direction.
    Complex numbers are taken as scalars, although they can
    be thought of having a direction in the complex plane.
    Quaternions and Octonions are not scalars, so is_scalar
    evaluates to False if an instance of them is passed.
    """
    types: tuple[type, ...] = (int, float, complex, np.integer, np.floating, np.complexfloating)
    return isinstance(n, types)


def is_integer(n: Any) -> bool:
    """
    Evaluates to True if the input is instance of int
    or np.integer
    """
    return type(n) is int or isinstance(n, np.integer)


def get_error(
        f: Callable[[X], Y],
        g: Callable[[X], Y],
        /,
        iterations: int = 1000,
        *,
        sample_input: Optional[Sequence[X]] = None,
        print_on_iteration: bool = True,
        squared_error: bool = False,
        fargs: Optional[Dict[K, V]] = None,
        gargs: Optional[Dict[K, V]] = None
) -> None:
    """
    Given two mathematical functions, it evaluates both functions
    on a sample input, and compare their results. 
    :param iterations: if sample_input is not provided,
    generates a random uniform list of inputs of size iterations.
    :param sample_input: if provided, evaluates both functions
    on the elements of sample_input
    :param print_on_iteration: if True, for every x in the list of
    inputs, x, f(x), g(x) and error(f(x), g(x)) is printed. If False,
    these print statements are ommited, and the function only prints
    the mean of the calculated error.
    :param squared_error: if True, the error is calculated obtaining
    the square of the difference. Else, the error is just the absolute
    value of the difference
    :param fargs: keyword arguments for f
    :param gargs: keyword arguments for g
    """

    if sample_input is None:
        sample_input = np.random.uniform(size=iterations)

    fargs = fargs if fargs else {}
    gargs = gargs if gargs else {}

    errors: list[float] = list()
    exp = 2 if squared_error else 1

    for x in sample_input:
        r1 = f(x, **fargs)
        r2 = g(x, **gargs)

        diff = abs(r1 - r2) ** exp
        errors.append(diff)
        if print_on_iteration:
            print('x is:    ', x)
            print('f(x) is: ', r1)
            print('g(x) is: ', r2)
            print('Difference is: ', diff)

    error_type_str: str = 'Mean squared error is: ' if squared_error else 'Mean error is: '
    print(error_type_str, mathipy.math.statistics.mean(errors))


def round_significant_figures(n: float, sigf: int) -> float:
    """
    Rounds a float to the corresponding significant
    figures.
    :param sigf: significant figures to be rounded
    :return: returns n rounded. Return is a float
    """
    if not is_integer(sigf):
        raise TypeError(f'significant figures must be an integer, received {sigf.__class__.__name__}')
    if sigf < 0:
        raise ValueError(f'significant figures must be positive, received {sigf}')
    
    return round(n, sigf - int(math.floor(math.log10(abs(n)))) - 1)


@vectorize
def trunc(n: float, decimals: int = 0) -> float:
    """
    Truncates a number, to the decimals indicated.
    :param n: number to be truncated
    :param decimals: decimals to which n is truncated
    :return: truncated n
    """
    if not is_integer(decimals):
        raise TypeError('decimal places must be an integer')
    elif decimals < 0:
        raise ValueError('decimal places has to greater or equal to 0')

    factor = 10.0 ** decimals
    return math.floor(n * factor) / factor


def handleZeroDivision(f: Callable[[X], Y]) -> Callable[[X], Y]:
    """
    Decorates a function, so if f raises a ZeroDivisionError,
    handleZeroDivision raises an exception and returns mpy.Infinite()
    """
    from mathipy.math import ntheory

    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ZeroDivisionError:
            return ntheory.Infinite()
    return wrapper
