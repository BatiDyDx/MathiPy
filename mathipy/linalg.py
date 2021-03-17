import numpy as np
import matplotlib.pyplot as plt
import mathipy as mpy
from mathipy import numeric_operations as ops

class Tensor():
    """
    Tensor class:
    Vector or Matrix

    """
    pass

class Vector(Tensor):
    rank = 1
    def __init__(self, elements): 
        self.elements = np.array(elements)
        
        if self.elements.shape[0] > 1 or len(self.elements.shape) != 2:
            raise TypeError(f'Vector input must be a one dimensional array, received {self.elements.shape}')
        
        self.dimension = self.elements.shape[1]
        self.module = mpy.sqrt(sum(map(lambda v: v**2, self.elements)))
        self.field = 'Complex' if np.issubdtype(self.elements.dtype, np.complex_) else 'Real'
    
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

    def __abs__(self):
        return self.module

    def __len__(self):
        return self.dimension

    def __iter__(self):
        return iter(self.elements.flatten())

    def __getitem__(self, index):
        return self.elements[0][index]

    def to_matrix(self):
        return Matrix(self.elements)

    def plot(self):
        if self.dimension != 2:
            raise ValueError('Only 2-dimensional vectors can be graphed')

        i, j = self.elements
        #i_min, i_max = - abs(i) - 1, abs(i) + 1
        fig, ax = plt.subplots()

        ax.set_title("Vector plot")
        plt.style.use('dark_background')

        plt.ylabel('$j$')
        plt.xlabel('$i$')
        plt.grid()

        head_w = self.module / 45
        plt.arrow(0, 0, i, j, head_width = head_w, length_includes_head = True, color='r')

        #ax.annotate("", xy=(i, j), xytext=(0, 0), arrowprops=dict(arrowstyle=))

        g_dim = abs(i) if abs(i) >= abs(j) else abs(j)

        if i > 0:
            i_min, i_max = 0, g_dim
        elif i < 0:
            i_min, i_max = -g_dim, 0
        else:
            i_min, i_max = -j / 2, j / 2

        if j > 0:
            j_min, j_max = 0, g_dim
        elif j < 0:
            j_min, j_max = -g_dim, 0
        else:
            j_min, j_max = -i / 2, i / 2

        plt.xlim(i_min, i_max)
        plt.ylim(j_min, j_max)

        plt.show()

    def __str__(self):
        return f'Vector({repr(self)})'

    def __repr__(self):
        return str(self.elements)

class Matrix(Tensor):
    rank = 2
    def __init__(self, elements):
        self.elements = np.array(elements)
        self.m_dimension, self.n_dimension = self.shape = self.elements.shape
        self.dimension = self.elements.size
        self.is_square = True if self.n_dimension == self.m_dimension else False
        if len(self.shape) != Matrix.rank:
            raise TypeError(f'Matrix shape must be of length 2, received {self.shape}')

    def change_dtype(self, dtype):
        self.elements = self.elements.astype(dtype)

    @property
    def adj(self):
        return adjoint(self)

    @property
    def C(self):
        return cofactor(self)

    @property
    def det(self):
        return determinant(self)

    @property
    def inv(self):
        return inverse(self)

    @property
    def T(self):
        return transpose(self)

    def trace(self):
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
        return mpy.Polynomial(*coefs)

    def __add__(A, B):
        if isinstance(B, Tensor):
            if isinstance(B, Vector):
                B = B.to_matrix()
            return matrix_addition(A, B)
        else: raise TypeError(f'Addition is only supported between Tensor instances, received {type(B)}')

    def __radd__(A, B):
        return A.__add__(B)

    def __sub__(A, B):
        return A + (-B)

    def __rsub__(A, B):
        return (-A).__add__(B)

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
            raise TypeError(f'Matrix product is only supported between tensor instances, received {type(B)}')

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

    def __len__(self):
        return self.m_dimension

    def __iter__(self):
        return iter(self.elements)

    def __getitem__(self, index):
        return self.elements[index]

    def __setitem__(self, index, value):
        m, n = index
        self.elements[m, n] = value

    def __str__(self):
        expression = 'Matrix(\n'
        expression += ' ' + str(self.elements)[1:-1]
        expression += '\n)'
        return expression

    def __repr__(self):
        return str(self.elements)

def vector_addition(v: Vector, u: Vector):
    if v.dimension == u.dimension:
        return Vector(v.elements + u.elements)
    else:
        raise ValueError(f'Vector dimensions must be equal to perform addition, received {v.dimension} and {u.dimension}')

def dot_product(v: Vector, u: Vector):
    if v.field == 'Complex' and u.field == 'Complex':
        return inner_product(v, u)

    if v.dimension == u.dimension:
        return np.dot(v.elements, u.elements)

def inner_product(v: Vector, u: Vector):
    u_hat = Vector(u.elements.conjugate())
    return dot_product(v, u_hat)

def cross_product(v: Vector, u: Vector):
    return Vector(np.cross(v.elements, u.elements))

def tensor_product(v: Vector, u: Vector):
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

def transpose(A: Matrix):
    return Matrix(A.elements.T)

def determinant(A: Matrix) -> float:
    if A.is_square:
        return np.linalg.det(A.elements)
    else:
        raise ValueError('Matrix must be square to calculate determinant')

def cofactor(A: Matrix):
    if A.is_square:
        return A.adj.T
    else:
        raise ValueError('Matrix must be square to calculate cofactor')

def adjoint(A: Matrix):
    if A.is_square:
        return A.inv * A.det
    else:
        raise ValueError('Matrix must be square to calculate adjoint')

def inverse(A: Matrix):
    return Matrix(np.linalg.inv(A.elements))

def linear_transformation(A: Matrix, *args: Vector) -> None:
    pass

def k_matrix(k, shape: tuple) -> Matrix:
    m, n = shape
    elements = [[k] * n for _ in range(m)] 
    return Matrix(elements)

def zeros_matrix(shape: tuple) -> Matrix:
    return k_matrix(0, shape)

def ones_matrix(shape: tuple) -> Matrix:
    return k_matrix(1, shape)

def identity(n: int) -> Matrix:
    C = zeros_matrix((n, n))
    for i in range(n):
        C[i, i] = 1
    return C