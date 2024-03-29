import math
from typing import Callable, Dict, Tuple, TypeVar
import numpy as np
import matplotlib.pyplot as plt
from mathipy import numeric_operations as ops
import mathipy.math
from mathipy.config import Real

class Function:
    function_type: str = 'Undefined Type'
    function_part: Dict[str, str] = {
        'roots'       : 'green',
        'y-intercept' :  'blue',
        'vertex'      :   'red',
        'asymptote'   :'purple',
        'axis'        : 'black',
        'area'        :'orange'
    }

    def __init__(self, f: callable, **kwargs):
        self.f = ops.vectorize(f)
        self.kwargs = kwargs

    def calculate_values(self, x):
        return self.f(x, **self.kwargs)

    def __call__(self, x) -> Real:
        return self.calculate_values(x)

    def get_yint(self):
        try:
            return self(0)
        except (ValueError, ZeroDivisionError):
            return np.nan

    def plot(self, pos: int = 0, range: int = 5, **kwargs):
        x_min, x_max = pos - range, pos + range
        x = np.linspace(x_min, x_max, 1000)
        y = self.calculate_values(x)

        fig, ax = plt.subplots()
        plt.grid()

        height = ops.kwargsParser(kwargs, ('height', 'h'), 1)
        v_scale = kwargs.get('vertical_scale', 'relative')
        if v_scale == 'relative':
            y_min, y_max = mathipy.math.statistics.min(y) - height, mathipy.math.statistics.max(y) + height
        elif v_scale == 'absolute':
            y_min, y_max = - height / 2, height / 2

        plt.xlim(x_min, x_max)
        try:
            plt.ylim(y_min, y_max)
        except ValueError:
            plt.ylim(-3,3)
    
        self.plot_func(ax)

        integrate_range = kwargs.get('integrate', None)
        if integrate_range:
            x1 = np.linspace(integrate_range[0], integrate_range[1])
            y1 = self.calculate_values(x1)
            ax.fill_between(x1, y1, color= Function.function_part['area'], alpha=0.5)

        ax.hlines(0, x_min, x_max, color= Function.function_part['axis'], alpha= 0.5)
        ax.vlines(0, y_min, y_max, color= Function.function_part['axis'], alpha= 0.5)
        plt.xlabel('$x$')
        plt.ylabel('$y$')
        ax.plot(x, y)
        plt.show()

    def plot_func(self, ax):
        ax.scatter(0, self.get_yint(), color= Function.function_part['y-intercept'])

    def __repr__(self):
        return f'{self.function_type} Function'

X = TypeVar('X')
Y = TypeVar('Y')

# TODO / DELETE
def lim(f: Callable[[X], Y], a: X, epsilon: float = 10e-10, approach: int = 0) -> Y:
    """
    :param epsilon: precision 
    :param approach: 1, 0, or -1. If 0, the limit by both sides are calculated.
    If different, returns np.nan. If approach is 1, the right limit towards a is
    calculated. If approach is -1, the left limit towards a is calculated.
    """
    if approach == 1:
        pass

    elif approach == -1:
        pass


    left_lim = lim(f, a, epsilon, approach = -1)
    right_lim = lim(f, a, epsilon, approach =  1)
    return np.allclose(left_lim, right_lim, epsilon)


def differential(f: callable, x: float, magnitude: int = 13):
    """
    The differential of a function, dy/dx is:
    dy / dx = lim of Δx -> 0 of Δy / Δx, where Δy = f(x + Δx) - f(x), 
    Since computers can't represent infintely small numbers
    the differential is computed relative to the magnitude parameter.
    """
    delta_x: float = 10 ** -magnitude
    dy = f(x + delta_x) - f(x)
    return dy / delta_x


@ops.vectorize
def to_radian(x: float) -> float:
    return x / 360 * mathipy.math.ntheory.tau


@ops.vectorize
def to_degree(x: float) -> float:
    return x / mathipy.math.ntheory.tau * 360


@ops.vectorize
def sign(x: Real) -> int:
    if x == 0:
        return 0
    return 1 if x > 0 else -1


@ops.vectorize
def floor(x: Real) -> Real:
    """
    Floor function. Rounds to the nearest lower integer
    >>> floor(1.5)
    1.0
    >>> floor(-3.0)
    -3.0
    """
    return x - mantissa(x)


@ops.vectorize
def ceil(x: Real) -> Real:
    """
    Ceil function. Rounds to the nearest greater integer
    >>> ceil(10.3)
    11.0
    >>> floor(0)
    0
    """
    return -floor(-x)


@ops.vectorize
def mantissa(x: Real) -> float:
    """
    Mantissa function. Returns the floating value
    of a number
    >>> mantissa(1.432523)
    0.432523
    >>> mantissa(0.3)
    0.3
    >>> mantissa(-2.5)
    0.5
    """
    return x % 1


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


@ops.vectorize
def maximum(a: Real, b: Real) -> Real:
    """
    Returns the maximum between two elements.
    Behaves like a universal function.
    """
    return (a >= b) * a + b * (a < b)


@ops.vectorize
def minimum(a: Real, b: Real) -> Real:
    """
    Returns the minimum between two elements.
    Behaves like a universal function.
    """
    return (a <= b) * a + b * (a > b)
