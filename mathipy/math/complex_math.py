import numpy as np
from mathipy.math import _math, trigonometry as trig
from mathipy import numeric_operations as ops
from typing import Union

def phase(x: Union[int, float, complex]) -> float:
    """
    Given a number, it returns its phase, or argument 
    Mathematically, the phase is the angle between the line from
    the origin to the number in the complex plane and the 
    positive real axis

    >>> phase(1)
    0
    >>> phase(1j)
    pi / 2
    """
    if x.real == 0:
        if x.imag > 0:
            return _math.pi / 2
        elif x.imag < 0:
            return - _math.pi / 2
        else:
            return None
    elif x.real < 0:
        if x.imag >= 0:
            return trig.arctan(x.imag / x.real) + _math.pi
        else:
            return trig.arctan(x.imag / x.real) - _math.pi
    else:
        return trig.arctan(x.imag / x.real)


def to_cartesian(module: Union[int, float], arg: float) -> complex:
    return module * cis(arg)


def cis(theta):
    """
    cis(theta) is equal to cos(theta) + i sin(theta)
    It is used for converting a complex number in the polar
    form to the trigonometric, or cartesian form
    >>> cis(0)
    1
    >>> cis(pi / 2)
    1j
    """
    return _math.cos(theta) + _math.sin(theta) * 1j

def to_polar(x: Union[int, float, complex]) -> tuple[float, float]:
    return (abs(x), phase(x))


def conjugate(x: complex) -> complex:
        """
        Returns the conjugate of a complex number
        """
        return x.real - x.imag * 1j

def ordered_pair(x: complex) -> tuple[float, float]:
        """
        Returns the tuple (a, b), like the ordered pair
        in the complex plane
        """
        return (x.real, x.imag)

def normalize(x: complex) -> complex:
        """
        Returns the normalized corresponding complex number,
        which has the same argument, but module of 1.
        A normalized complex number is one with module of 1
        To get the normalized version of a number, it has to be divided
        by its module.
        """
        return x / _math.abs(x)

def complex_roots(x: complex, n: int) -> list[complex]:
    """
    Given the number of roots n, the distance to the origin r,
    and the initial angle, theta, it calculates all k such that
    k ^ n = r * e^(i * theta)
    """
    r, theta = to_polar(x)
    roots: list = []
    w: float = _math.tau / n
    for k in range(n):
        arg = w * k + theta
        z = to_cartesian(r, arg)
        roots.append(z)
    return roots


@ops.vectorize
def real(z):
    """
    Returns the real part of a number
    """
    return z.real


@ops.vectorize
def imag(z):
    """
    Returns the imaginary part of a number
    """
    return z.imag


@ops.vectorize
def module(z):
    """
    Returns the module of a number
    """
    return _math.abs(z)


@ops.vectorize
def argument(z):
    """
    Returns the argument of a number
    """
    return phase(z)


def i(exp: int) -> complex:
    """
    Get the nth power of i, instead of having to
    calculate it recursively
    """
    if exp % 4 == 0:
        return 1
    elif exp % 4 == 1:
        return 1j
    elif exp % 4 == 2:
        return -1
    elif exp % 4 == 3:
        return -1j
