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
    to_Complex, 
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
    gamma,
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
    mcm,
)
#TODO   
#Add algebra
from .algebra import (
    setUnion,
    setIntersection,
    setSub,
    setContains,
    setIsContained
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
    Complex_Function,
    Exponential,
    Linear,
    Log,
    NormalDistribution,
    NRoot,
    Quadratic, quadratic_roots,
    Rational,
)

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
    uFunc,
    kwargsParser,
)

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

from .testing import test_time

#TODO
#Add all objects to be imported when importing *
__all__ = [
    '_complex', '_math', 'arithmetic', 'functions', 'calculus', 'datastr', 'linalg', 'numeric_operations',
    'polynomial', 'statistics', 'Vector', 'Complex', 'Infinite', 'Variable'
    ]