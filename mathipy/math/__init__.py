
from ._math import (
    abs,
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
    pi_2,
    root_n,
    sqrt,
    sqrt2, 
    tau,
    productory,
    summation,
    gcd,
    lcm,
    maximum,
    mantissa,
    minimum,
    floor,
    ceil,
    trunc,
    combinatorial,
    variation,
    permutation
)

from .trigonometry import (
    arcsin,
    arccos,
    arctan,
    arcsec,
    arccosec,
    arccotan,
    arcsinh,
    arccosh,
    arctanh,
    arccosech,
    arcsech,
    arccotanh,
    cos,
    cosec,
    cosech,
    cotan,
    cotanh,
    cosh,
    sec,
    sech,
    sin, 
    sinh,
    tan,
    tanh,
)

from .calculus import Function, to_degree, to_radian, differential

from .complex_math import (
    to_cartesian,
    to_polar,
    phase,
    conjugate,
    complex_roots,
    ordered_pair,
    normalize,
    real,
    imag,
    module,
    argument,
    i,
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

from .polynomial import (
    Polynomial,
    polynomial_addition,
    polynomial_product,
    #polynomial_division,
    scalar_product,
    max_degree
)

from .statistics import (
    Statistics,
    max,
    min,
    std,
    median,
    mode,
    frequency
)

from .quaternion import (
    Quaternion,
    quaternion_conjugate,
    quaternion_multiplication
)

from .octonion import (
    Octonion,
    octonion_conjugate,
    octonion_multiplication
)