import math
from typing import Iterator, Tuple, Union, Callable
from abc import ABC, abstractmethod
import numpy as np
from mathipy.math.polynomial import Polynomial
from mathipy.math import trigonometry
from mathipy import numeric_operations as ops
from mathipy.config import Real, Scalar

class Tensor(ABC):
    """
    Tensor abstract base class.
    Matrix and Vector classes inherit from Tensor
    """
    rank: int

    def change_dtype(self, dtype: type):
        self.elements = self.elements.astype(dtype)

    def map(self, f: Callable[[Scalar], Scalar], *args, **kwargs) -> None:
        vfunc = ops.vectorize(f)
        self.elements = vfunc(self.elements, *args, **kwargs)

    @abstractmethod
    def __add__(self) -> 'Tensor':
        pass

    @abstractmethod
    def __sub__(self) -> 'Tensor':
        pass

    @abstractmethod
    def __neg__(self) -> 'Tensor':
        pass

    @abstractmethod
    def __mul__(self) -> 'Tensor':
        pass

    @abstractmethod
    def __rmul__(self) -> 'Tensor':
        pass

    @abstractmethod
    def __truediv__(self) -> 'Tensor':
        pass

    @abstractmethod
    def __matmul__(self) -> 'Tensor':
        pass

    @abstractmethod
    def __getitem__(self): #TODO add return type to __getitem__ abstract method
        pass

    @abstractmethod
    def __iter__(self) -> Iterator:
        pass

    @abstractmethod
    def __len__(self) -> int:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass
    
    @abstractmethod
    def __repr__(self) -> str:
        pass


class Vector(Tensor):
    rank = 1

    def __init__(self, elements): 
        self.elements = np.array(elements)
        
        if self.elements.shape[0] > 1 or len(self.elements.shape) != 2:
            raise TypeError(f'Vector input must be a one dimensional array, received {self.elements.shape}')
        
        self.dimension: int = self.elements.shape[1]
        self.module: float = math.sqrt(sum(map(lambda v: v**2, self.elements[0])))
        self.field: str = 'Complex' if np.issubdtype(self.elements.dtype, np.complex_) else 'Real'
    
    @property
    def T(self):
        return transpose(self)

    def __add__(v, u):
        if isinstance(u, Vector):
            return vector_addition(v, u)
        elif isinstance(u, Matrix):
            return u.__radd__(v)
        raise TypeError(f'Vector addition is not supported between Vector and {type(u)}')

    def __sub__(v, u):
        if isinstance(u, Vector):
            return v + (-u)
        elif isinstance(u, Matrix):
            return u.__rsub__(v)

    def __neg__(v):
        return Vector(v.elements * -1)

    def __mul__(v, u):
        if isinstance(u, Tensor):
            if isinstance(u, Vector):
                return dot_product(v, u)
            else:
                return u.__rmul__(v)
        else:
            return Vector(v.elements * u)

    def __rmul__(v, n):
        return v.__mul__(n)

    def __truediv__(v, n):
        return v.__mul__(1 / n)

    def __matmul__(v, u):
        if isinstance(u, Vector):
            return tensor_product(v, u)
        elif isinstance(u, Matrix):
            return Vector(u.__rmatmul__(v).elements)

    def __abs__(self) -> float:
        return self.module

    def __len__(self) -> int:
        return self.dimension

    def __iter__(self) -> Iterator:
        return iter(self.elements.flatten())

    def __getitem__(self, index: int) -> Scalar:
        return self.elements[0, index]

    def normalize(self):
        return self / self.module

    def to_matrix(self):
        return Matrix(self.elements)

    def __str__(self):
        return f'Vector({repr(self)})'

    def __repr__(self):
        return str(self.elements)


class Matrix(Tensor):
    rank = 2

    def __init__(self, elements):
        self.elements = np.array(elements)
        self.m_dimension, self.n_dimension = self.shape = self.elements.shape
        self.dimension: int = self.elements.size
        self.is_square: bool = True if self.n_dimension == self.m_dimension else False
        if len(self.shape) != Matrix.rank:
            raise TypeError(f'Matrix shape must be of length 2, received {self.shape}')

    @property
    def adj(self):
        return adjoint(self)

    @property
    def C(self):
        return cofactor(self)

    @property
    def det(self) -> Scalar:
        return determinant(self)

    @property
    def inv(self):
        return inverse(self)

    @property
    def T(self):
        return transpose(self)

    def trace(self) -> Scalar:
        if not self.is_square:
            raise ValueError('Matrix must be square to calculate trace')
        else:
            t = 0
            for i in range(self.m_dimension):
                t += self[i][i]
            return t

    @property
    def is_hermitian(self):
        return self == Matrix(self.elements.conjugate())

    @property
    def is_symmetric(self):
        return self == self.T

    def eigen_vectors(self):
        if not self.is_square:
            raise TypeError(f'Only square matrices eigenvectors can be computed, received {self.shape}')
        #if self.is_hermitian:
        #    return np.linalg.eigh(self.elements)
        #else:
        return np.linalg.eig(self.elements)

    def eigen_values(self):
        return np.linalg.eigvals(self.elements)

    def characteristic_poly(self):
        coefs = list(np.poly(self.elements))
        return Polynomial(*coefs)

    def __add__(A, B):
        if not isinstance(B, Matrix):
            raise TypeError(f'Addition is only supported between Matrix instances, received {B.__class__.__name__}')
        return matrix_addition(A, B)

    def __sub__(A, B):
        return A + (-B)

    def __neg__(A):
        return A * -1

    def __mul__(A, B):
        if isinstance(B, Tensor):
            if isinstance(B, Vector):
                B = B.to_matrix()
            return element_wise_product(A, B)
        else:
            return Matrix(A.elements * B)

    def __rmul__(A, B):
        return A.__mul__(B)

    def __matmul__(A, B):
        if isinstance(B, Tensor):
            if isinstance(B, Vector):
                B = B.to_matrix()
            return matrix_product(A, B)
        else:
            raise TypeError(f'Matrix product is only supported between tensor instances, received {B.__class__.__name__}')

    def __rmatmul__(A, B):
        if isinstance(B, Vector):
            return B.to_matrix() @ A

    def __truediv__(A, B):
        if ops.is_scalar(B):
            return A * (1 / B)
        elif isinstance(B, Matrix):
            return A @ (B ** -1)
        else:
            return B.__rtruediv__(A)

    def __rtruediv__(A, B):
        return (A ** -1) * B

    def __pow__(self, n):
        if not isinstance(n, int):
            raise ValueError('Exponent must be an integer')
        if n == 1 or n == 0:
            return self
        elif n > 1:
            return self @ (self ** (n - 1))
        else:
            return self.inv ** (-n)

    def __eq__(A, B):
        return np.array_equal(A.elements, B.elements)

    def __len__(self) -> int:
        return self.m_dimension

    def __iter__(self) -> Iterator:
        return iter(self.elements)

    def __getitem__(self, index):
        return self.elements[index]

    def __setitem__(self, index: Union[tuple[int, int]], value: Union[int, float, complex]):
        m, n = index
        self.elements[m, n] = value

    def __str__(self):
        expression = 'Matrix(\n'
        expression += ' ' + str(self.elements)[1:-1]
        expression += '\n)'
        return expression

    def __repr__(self):
        return str(self.elements)


def vector_addition(v: Vector, u: Vector) -> Vector:
    if v.dimension == u.dimension:
        return Vector(v.elements + u.elements)
    else:
        raise ValueError(f'Vector dimensions must be equal to perform addition, received {v.dimension} and {u.dimension}')


def dot_product(v: Vector, u: Vector) -> Vector:
    if v.field == 'Complex' and u.field == 'Complex':
        return inner_product(v, u)

    if v.dimension == u.dimension:
        return np.dot(v.elements, u.elements)


def inner_product(v: Vector, u: Vector) -> Vector:
    u_hat = Vector(u.elements.conjugate())
    return np.dot(v.elements, u_hat.elements)


def cross_product(v: Vector, u: Vector) -> Vector:
    return Vector(np.cross(v.elements, u.elements))


def mixed_product(v: Vector, u: Vector, w: Vector) -> Scalar:
    """
    Returns the mixed product of 3 vectors: v ∧ u x w
    
    """
    return dot_product(cross_product(v, u), w)


def check_if_parallel(v: Vector, u: Vector) -> bool:
    """
    Evaluates if two vectors are parallel.
    The module of the cross product between two 
    vectors is equivalent to the are of the parallelogram
    formed by them.
    Then, if v || u, the area of the parallelogram is 0,
    which implies |v ∧ u| = 0
    """
    return cross_product(v, u).module == 0


def check_if_orthogonal(v: Vector, u: Vector) -> bool:
    """
    Evaluates if two vectors are orthogonal (perpendicular)
    Two vectors are perpendicular if and only if (v x u) = 0 
    """
    return dot_product(v, u) == 0


def proy_vector(v: Vector, u: Vector) -> Vector:
    """
    Returns the v vector proyection over u
    proy_u(v) = |v| cos(v ^ u) u_0 = (v x u_0)u_0
    """
    u_0 = u.normalize()
    alpha = dot_product(v, u_0)
    return alpha * u_0


def check_if_coplanar(v: Vector, u: Vector, w: Vector) -> bool:
    """
    Evaluates if three vectors are coplanars.
    The absolute value mixed product between v,
    """
    return mixed_product(v, u, w) == 0


def angle_of_vectors(v: Vector, u: Vector) -> Real:
    """
    Returns the angle between two vectors (v ^ u)
    v x u = |v|·|u|·cos(v ^ u) 
    ==> (v x u) / (|v|·|u|) = cos(v ^ u)
    ==> arccos( (v x u) / (|v|·|u|) ) = (v ^ u)
    """
    x = dot_product(v, u) / (v.module * u.module)
    return trigonometry.arccos(x)


def tensor_product(v: Vector, u: Vector) -> Vector:
    w = []
    for i in v:
        for j in u:
            w.append(i * j)
    return Vector([w])


def matrix_addition(A: Matrix, B: Matrix) -> Matrix:
    if A.shape == B.shape:
        return Matrix(A.elements + B.elements)
    else:
        raise ValueError(f'Matrices can only be summed if they have same shape, received {A.shape} and {B.shape}')


def element_wise_product(A: Matrix, B: Matrix) -> Matrix:
    if A.shape == B.shape:
        return Matrix(A.elements * B.elements)
    else:
        raise ValueError(
            f'Matrices can only be element-wise multiplied if they have same shape, received {A.shape} and {B.shape}'
        )


def matrix_product(A: Matrix, B: Matrix) -> Matrix:
    if A.n_dimension == B.m_dimension:
        return Matrix(A.elements @ B.elements)
    else: 
        raise ValueError(
            f"First matrix n-dimension must be equal to second matrix m-dimension. Received {A.n_dimension} and {B.m_dimension}"
        )


def transpose(A: Matrix) -> Matrix:
    return Matrix(A.elements.T)


def determinant(A: Matrix) -> Scalar:
    if A.is_square:
        return np.linalg.det(A.elements)
    else:
        raise ValueError('Matrix must be square to calculate determinant')


def cofactor(A: Matrix) -> Matrix:
    if A.is_square:
        return A.adj.T
    else:
        raise ValueError('Matrix must be square to calculate cofactor')


def adjoint(A: Matrix) -> Matrix:
    if A.is_square:
        return A.inv * A.det
    else:
        raise ValueError('Matrix must be square to calculate adjoint')


def inverse(A: Matrix) -> Matrix:
    return Matrix(np.linalg.inv(A.elements))


def linear_transformation(A: Matrix, *args: Vector) -> None:
    pass


def k_matrix(k: Scalar, shape: Tuple[int, int]) -> Matrix:
    m, n = shape
    elements: list[list] = [[k] * n for _ in range(m)]
    return Matrix(elements)


def zeros_matrix(shape: Tuple[int, int]) -> Matrix:
    return k_matrix(0, shape)


def ones_matrix(shape: Tuple[int, int]) -> Matrix:
    return k_matrix(1, shape)


def identity(n: int) -> Matrix:
    C = zeros_matrix((n, n))
    for i in range(n):
        C[i, i] = 1
    return C
