from typing import Iterable, Tuple, Union
import numpy as np
from mathipy.math import _math
from mathipy.numeric_operations import is_iterable
from mathipy.math.quaternion import (
    Quaternion,
    quaternion_multiplication, 
    quaternion_conjugate
)
from mathipy.config import Real, Scalar


class Octonion:
    e0: Real
    e1: Real
    e2: Real
    e3: Real
    e4: Real
    e5: Real
    e6: Real
    e7: Real
    v: Tuple[Real, Real, Real, Real, Real, Real, Real]

    def __init__(self, __obj: Union[Scalar, Quaternion, Iterable]):
        if isinstance(__obj, (int, float, complex)):
            self.e0, self.e1 = __obj.real, __obj.imag
            self.e2, self.e3 = 0, 0
            self.e4, self.e5 = 0, 0
            self.e6, self.e7 = 0, 0

        elif isinstance(__obj, Quaternion):
            self.e0, self.e1 = __obj.a, __obj.b
            self.e2, self.e3 = __obj.c, __obj.d
            self.e4, self.e5 = 0, 0
            self.e6, self.e7 = 0, 0

        elif is_iterable(__obj):
            if not len(__obj) == 8:
                raise ValueError(f'Length of the input must be 8, recieved {len(__obj)}')
            self.e0, self.e1 = __obj[0:2]
            self.e2, self.e3 = __obj[2:4]
            self.e4, self.e5 = __obj[4:6]
            self.e6, self.e7 = __obj[6:8]

        else:
            raise TypeError(f'Cannot instantiate Octonion from type {__obj.__class__.__name__}')

        self.v = (self.e1, self.e2, self.e3, self.e4, self.e5, self.e6, self.e7)

    @property
    def real(self) -> Real:
        return self.e0

    def __add__(p, q: Union[Real, complex, Quaternion, 'Octonion']) -> 'Octonion':
        if isinstance(q, Octonion):
            return Octonion(p.as_array() + q.as_array())
        
        elif isinstance(q, (int, float, complex, Quaternion)):
            _q = Octonion(q)
            return p.__add__(_q)

        return q.__rmul__(p)

    def __sub__(p, q: Union[Real, complex, Quaternion, 'Octonion']) -> 'Octonion':
        return p + (-q)

    def __neg__(p) -> 'Octonion':
        return p * -1

    def __mul__(p, q: Union[Real, complex, Quaternion, 'Octonion']) -> 'Octonion':
        if isinstance(q, (int, float)):
            return Octonion(q * p.as_array())

        elif isinstance(q, complex):
            _q = Octonion(q)
            return p.__mul__(_q)

        elif isinstance(q, (complex, Quaternion, Octonion)):
            q_array = q.as_array()

            if len(q.ordered_pair()) == 4:
                q_array = np.hstack([q_array, (0,) * 4])

            result: np.ndarray = octonion_multiplication(p.as_array(), q_array)
            return Octonion(result)

        return q.__rmul__(p)

    def __truediv__(p, q: Union[Real, complex, Quaternion, 'Octonion']):
        if isinstance(q, (int, float, complex)):
            return p * (1 / q)
        
        elif isinstance(q, Quaternion):
            return p * Octonion(q).inverse()
        
        return p * q.inverse()

    def __abs__(self) -> Real:
        return _math.sqrt(sum(map(lambda x: x ** 2, self.ordered_pair())))

    def conjugate(self) -> 'Octonion':
        result = octonion_conjugate(self.as_array())
        return Octonion(result)

    def inverse(self) -> 'Octonion':
        return self.conjugate() / abs(self)

    def as_array(self) -> np.ndarray:
        return np.array(self.ordered_pair())

    def ordered_pair(self) -> Tuple[Real, Real, Real, Real, Real, Real, Real, Real]:
        return (self.real,) + self.v


def octonion_conjugate(p: np.ndarray) -> np.ndarray:
    y = np.ones(8) * -1
    y[0] = 1
    return p * y

def octonion_multiplication(p: np.ndarray, q: np.ndarray) -> np.ndarray:
    a, b = p[:4], p[4:]
    c, d = q[:4], q[4:]

    c_star: np.ndarray = quaternion_conjugate(c)
    d_star: np.ndarray = quaternion_conjugate(d)

    z1 = quaternion_multiplication(a, c) - quaternion_multiplication(d_star, b)
    z2 = quaternion_multiplication(d, a) + quaternion_multiplication(b, c_star)
    return np.hstack([z1, z2])