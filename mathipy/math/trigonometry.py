import math
from mathipy.cfuncs.bin import trigonometry as ctrig
from mathipy import numeric_operations as ops
from mathipy.math import ntheory

############################################
# Trignometric functions, and their inverses
############################################

def sin(x):
    """
    The sin trig function, defined as the
    quotient between the opposite leg and the hypotenuse of
    an angle in a triangle. The input must be in radians
    """
    def complex_sin(z):
        return (ntheory.e ** (1j * z) - ntheory.e ** (-1j * z)) / 2j

    if x.imag != 0:
        return complex_sin(x)
    else:
        return ctrig.sin(x)


def cos(x):
    """
    The cos trig function, defined as the
    quotient between the adjacent leg and the hypotenuse of
    an angle in a triangle. The input must be in radians
    """
    def complex_cos(z):
        return (ntheory.e ** (1j * z) + ntheory.e ** (-1j * z)) / 2

    if x.imag != 0:
        return complex_cos(x)
    else:
        return ctrig.cos(x)


@ops.handleZeroDivision
def tan(x):
    """
    The tan trig function, defined as the
    quotient between the opposite leg and the adjacent leg of
    an angle in a triangle. The input must be in radians
    """
    def complex_tan(z):
        y = (ntheory.e ** (1j * z) - ntheory.e ** (-1j * z)) * -1j
        y /= (ntheory.e ** (1j * z) + ntheory.e ** (-1j * z))
        return y

    if x.imag != 0:
        return complex_tan(x)
    else:
        return ctrig.tan(x)


def arcsin(x):
    """
    Inverse function of the sin, sometimes called sin^-1
    """
    def complex_arcsin(z):
        y = z * 1j + (1 - z ** 2) ** .5
        y = math.log(y) / 1j
        return y
    
    if x.imag != 0:
        return complex_arcsin(x)
    else:
        return ctrig.arcsin(x)


def arccos(x):
    """
    Inverse function of the cos, sometimes called cos^-1
    """
    def complex_arccos(z):
        y = z + (z ** 2 - 1) ** .5
        y = math.log(y) / 1j
        return y

    if x.imag != 0:
        return complex_arccos(x)
    else:
        if x == 0:
            return ntheory.math_constants['pi/2']
        return ctrig.arccos(x)

def arctan(x):
    """
    Inverse function of the tan, sometimes called tan^-1
    """
    def complex_arctan(z):
        y = (1 + z * 1j) / (1 - z * 1j)
        y = -0.5j * math.log(y)
        return y

    if x.imag != 0:
        return complex_arctan(x)
    return ctrig.arctan(x)


###################################################
# Hyperbolic and reciprocal trigonometric functions
###################################################
def cosh(x):
    """
    Hyperbolic cosine function. Input must
    be in radians 
    """
    return cos(x * -1j)


def sinh(x):
    """
    Hyperbolic sine function. Input must
    be in radians 
    """
    return sin(x * -1j) * 1j


def tanh(x):
    """
    Hyperbolic tangent function. Input must
    be in radians 
    """
    return sinh(x) / cosh(x)


@ops.handleZeroDivision
def cosec(x):
    """
    Trigonometric cosecant function, reciprocal of sine,
    so that cosec(x) = 1 / sin(x)
    Input must be in radians 
    """
    return 1 / sin(x)


@ops.handleZeroDivision
def sec(x):
    """
    Trigonometric secant function, reciprocal of cosine,
    so that sec(x) = 1 / cos(x)
    Input must be in radians 
    """
    return 1 / cos(x)


@ops.handleZeroDivision
def cotan(x):
    """
    Trigonometric cotangent function, reciprocal of tangent,
    so that cotan(x) = 1 / tan(x) = cos(x) / sin(x)
    Input must be in radians 
    """
    return cos(x) / sin(x)

############################################
# Reciprocal of hyperbolic functions
############################################
@ops.handleZeroDivision
def cosech(x):
    """
    Hyperbolic cosecant function, reciprocal of sinh,
    so that cosech(x) = 1 / sinh(x)
    Input must be in radians 
    """
    return 1 / sinh(x)


def sech(x):
    """
    Hyperbolic secant function, reciprocal of cosh,
    so that sech(x) = 1 / cosh(x)
    Input must be in radians 
    """
    return 1 / cosh(x)


@ops.handleZeroDivision
def cotanh(x):
    """
    Hyperbolic cotangent function, reciprocal of tanh,
    so that cotanh(x) = 1 / tanh(x) = cosh(x) / sinh(x)
    Input must be in radians 
    """
    return cosh(x) / sinh(x)


############################################
# Inverse of reciprocal trig functions
############################################
def arcsec(x):
    pass

def arccosec(x):
    pass

def arccotan(x):
    pass


############################################
# Inverse of hyperbolic functions
############################################

def arcsinh(x):
    pass

def arccosh(x):
    pass


def arctanh(x):
    pass

############################################
# Inverse of reciprocal hyperbolic functions
############################################

def arccosech(x):
    pass

def arcsech(x):
    pass

def arccotanh(x):
    pass

############################################
