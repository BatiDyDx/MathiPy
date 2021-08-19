import numpy as np
import math
from mathipy.math.linalg import Matrix
from typing import Iterable, Tuple, Union
from mathipy.config import Real, Scalar
from mathipy.numeric_operations import is_iterable

class Quaternion:
    a: Real
    b: Real
    c: Real
    d: Real
    v: Tuple[Real, Real, Real]

    def __init__(self, __obj: Union[Scalar, Iterable]):
        if isinstance(__obj, (int, float, complex)):
            self.a, self.b = __obj.real, __obj.imag
            self.c, self.d = 0, 0

        elif is_iterable(__obj):
            if not len(__obj) == 4:
                raise ValueError(f'Length of the input must be 4, recieved {len(__obj)}')
            self.a, self.b = __obj[0:2]
            self.c, self.d = __obj[2:4]

        self.v = (self.b, self.c, self.d)

    @property
    def real(self) -> Real:
        return self.a

    def __add__(p, q: Union[Real, complex, 'Quaternion']) -> 'Quaternion':
        if isinstance(q, Quaternion):
            return Quaternion((m + n for m, n in zip(p.ordered_pair(), q.ordered_pair())))
        
        elif isinstance(q, (int, float, complex)):
            return Quaternion((p.a + q.real, p.b + q.imag, p.c, p.d))
        
        else:
            return q.__radd__(p)

    def __sub__(p, q: Union[Real, complex, 'Quaternion']) -> 'Quaternion':
        return p + (-q)

    def __neg__(p) -> 'Quaternion':
        return p * -1

    def __mul__(p, q: Union[Real, complex, 'Quaternion']) -> 'Quaternion':
        if isinstance(q, Quaternion):
            real = p.a * q.a - p.b * q.b - p.c * q.c - p.d * q.d
            i    = p.a * q.b + p.b * q.a + p.c * q.d - p.d * q.c
            j    = p.a * q.c - p.b * q.d + p.c * q.a + p.d * q.b
            k    = p.a * q.d + p.b * q.c - p.c * q.b + p.d * q.a
            return Quaternion((real, i, j, k))
        
        elif isinstance(q, complex):
            return p.__mul__(Quaternion((p.real, p.imag) + (0,) * 2))
        
        elif isinstance(q, (int, float)):
            return Quaternion((k * q for k in p.ordered_pair()))

        else:
            return q.__rmul__(p)

    def __truediv__(p, q: Union[Real, complex, 'Quaternion']) -> 'Quaternion':
        if isinstance(q, (int, float, complex)):
            return p * (1 / q)
        
        elif isinstance(q, Quaternion):
            return p * q.inverse()

    def __eq__(p, q: Union[Real, complex, 'Quaternion']) -> bool:
        if isinstance(q, (int, float)):
            return p.real == q.real and p.v == (0,) * 3
        return p.ordered_pair() == q.ordered_pair()

    def __bool__(self) -> bool:
        return bool(self.ordered_pair() != (0,) * 4)

    def conjugate(self) -> 'Quaternion':
        return Quaternion((self.a, -self.b, -self.c, -self.d))

    def inverse(self) -> 'Quaternion':
        return self.conjugate() / abs(self)

    def as_complex_matrix(self) -> Matrix:
        a_11: complex =   self.a + self.b * 1j
        a_12: complex =   self.c + self.d * 1j
        a_21: complex = - self.c + self.d * 1j
        a_22: complex =   self.a - self.b * 1j
        return Matrix(
            [
                [a_11, a_12], 
                [a_21, a_22]
            ]
        )

    def as_matrix(self) -> Matrix:
        a_11, a_12, a_13, a_14 = self.ordered_pair()
        a_21, a_22, a_23, a_24 = -self.b,  self.a, -self.d,  self.c
        a_31, a_32, a_33, a_34 = -self.c,  self.d,  self.a, -self.b
        a_41, a_42, a_43, a_44 = -self.d, -self.c,  self.b,  self.a
        return Matrix(
            [
                [a_11, a_12, a_13, a_14],
                [a_21, a_22, a_23, a_24],
                [a_31, a_32, a_33, a_34],
                [a_41, a_42, a_43, a_44],
            ]
        )

    def __abs__(self) -> Real:
        return math.sqrt(sum(map(lambda x: x ** 2), self.ordered_pair()))

    def as_array(self) -> np.ndarray:
        return np.array(self.ordered_pair())

    def ordered_pair(self) -> Tuple[Real, Real, Real, Real]:
        return (self.real,) + self.v

    def __str__(self) -> str:
        return f'{self.a} + {self.b}i + {self.c}j + {self.d}k'


def quaternion_conjugate(p: np.ndarray) -> np.ndarray:
    y = np.ones(4) * -1
    y[0] = 1
    return p * y

def quaternion_multiplication(p: np.ndarray, q: np.ndarray) -> np.ndarray:
    x0 = p[0] * q[0] - p[1] * q[1] - p[2] * q[2] - p[3] * q[3]
    x1 = p[0] * q[1] + p[1] * q[0] + p[2] * q[3] - p[3] * q[2]
    x2 = p[0] * q[2] - p[1] * q[3] + p[2] * q[0] + p[3] * q[1]
    x3 = p[0] * q[3] + p[1] * q[2] - p[2] * q[1] + p[3] * q[0]

    return np.array((x0, x1, x2, x3))