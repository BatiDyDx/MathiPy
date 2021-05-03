__version__ = '0.1dev'

from . import (
    _complex,
    _math,
    arithmetic,
    functions,
    calculus,
    datastr,
    linalg,
    numeric_operations,
    polynomial,
    statistics,
)

from ._complex import (
    Complex, 
    to_complex,
    real, 
    imag, 
    module, 
    argument,
    circle_roots,
    i,
)

from ._math import (
    abs,
    cos,
    cosec,
    cosech,
    cotan,
    cotanh,
    cosh,
    e,
    factorial,
    fibonacci,
    fibonacci_seq,
    gamma,
    index_of_fib,
    Infinite,
    ln,
    log, 
    phi,
    pi, 
    root_n,
    sec,
    sech,
    sin, 
    sinh,
    sqrt,
    sqrt2,
    tan,
    tanh, 
    tau,
    product,
    summation,
    gcd,
    lcm,
)

from .arithmetic import (
    addition,
    multiplication,
    power,
    Variable,
)

from .calculus import Function, to_degree, to_radian

from .datastr import (
    BinaryTree,
    Stack,
    Node,
    Queue,
    Tree,
)

from .functions import (
    AbsoluteValue,
    BinomialDistribution,
    ComplexFunction,
    Exponential,
    Linear,
    Log,
    NormalDistribution,
    NRoot,
    Quadratic, quadratic_roots,
    Rational,
)

from . import linalg
from .linalg import (
    Vector, 
    Matrix,
    vector_addition,
    dot_product,
    inner_product,
    cross_product,
    tensor_product,
    matrix_addition,
    element_wise_product,
    matrix_product,
    transpose,
    determinant,
    cofactor,
    adjoint,
    inverse,
    k_matrix,
    zeros_matrix,
    ones_matrix,
    identity,
    linear_transformation
)
from. import numeric_operations

from .numeric_operations import (
    max,
    mean,
    min,
    mode,
    frequency,
    std,
    median,
    round_if_close,
    is_scalar,
    is_iterable,
    variation,
    permutation,
    combinatorial,
    kwargsParser,
)

from . import polynomial
from .polynomial import (
    Polynomial,
    polynomial_addition,
    polynomial_product,
    polynomial_division,
    scalar_product,
    max_degree
)

from .science import c, H, ket, time_dilation

from .statistics import Statistics

# TODO
# Add all objects to be imported when importing *
__all__ = [
    'algebra', '_complex', '_math', 'arithmetic', 'functions', 'calculus', 'datastr', 'linalg', 'numeric_operations',
    'polynomial', 'science', 'statistics', 'Vector', 'Complex', 'Infinite', 'Variable', 'AbsoluteValue',
    'BinomialDistribution', 'ComplexFunction', 'Exponential', 'Linear', 'Log', 'NormalDistribution',
    'NRoot', 'Quadratic', 'quadratic_roots', 'Rational'
]
