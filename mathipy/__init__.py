__version__ = '0.1dev'

from . import (
    math,
    arithmetic,
    datastr,
    functions,
    numeric_operations
)

from .math import (
    complex_math,
    _math,
    linalg,
    polynomial,
    statistics
)

from .arithmetic import (
    addition,
    multiplication,
    power,
    Variable,
)

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


from . import numeric_operations
from .numeric_operations import (
    round_if_close,
    is_scalar,
    is_iterable,
    kwargsParser,
)


from .science import c, H, ket, time_dilation

# TODO
# Add all objects to be imported when importing *
__all__ = [
    'algebra', '_complex', 'math', 'arithmetic', 'functions', 'datastr', 'linalg', 'numeric_operations',
    'polynomial', 'science', 'statistics', 'Vector', 'Infinite', 'Variable', 'AbsoluteValue',
    'BinomialDistribution', 'ComplexFunction', 'Exponential', 'Linear', 'Log', 'NormalDistribution',
    'NRoot', 'Quadratic', 'quadratic_roots', 'Rational'
]
