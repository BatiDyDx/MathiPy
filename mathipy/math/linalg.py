import numpy as np
from mathipy.math.polynomial import Polynomial
from mathipy.math import trigonometry
from mathipy.config import Real, Scalar

###############################################################
# Linalg will be modified, adopting a different paradigm.
# The idea is to migrate from objected oriented tools to
# a more functional paradigm.
# Functions in this submodule will operate with numpy arrays
# natively, instead of having to instantiate classes like
# it was before. 
# This will increase usability, development, and debugging
# since numpy has already dealt with the majority of problems
# related to optimization and efficiency in calculations.
# On top of this, NumPy provides a wide variety of operations
# for linear algebra, so the idea is not to reinvent the wheel,
# and try to complement with new functionalities and tools
# provided by mathipy.math.linalg submodule
###############################################################

def is_vector(v: np.ndarray) -> bool:
    return is_col_vector(v) or is_row_vector(v)


def is_row_vector(v: np.ndarray) -> bool:
    return v.shape[0] == 1


def is_col_vector(v: np.ndarray) -> bool:
    return v.shape[1] == 1


def is_matrix(A: np.ndarray) -> bool:
    return A.ndim == 2


def is_square_matrix(A: np.ndarray) -> bool:
    m, n = A.shape
    return is_matrix(A) and (m == n) 


def cofactor(A: np.ndarray) -> np.ndarray:
    if is_square_matrix(A):
        return adjoint(A).T
    else:
        raise ValueError('Matrix must be square to calculate cofactor')


def adjoint(A: np.ndarray) -> np.ndarray:
    if is_square_matrix(A):
        return np.linalg.inv(A) * np.linalg.det(A)
    else:
        raise ValueError('Matrix must be square to calculate adjoint')


def matrix_decomposition(A: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Given a matrix A, return the symmetric and antisymmetric matrices that
    add up to A.
    Every square matrix can be uniquely decomposed into a sum of two matrices
    where one is symmetric and the other is antisymmetric
    """
    if not is_square_matrix(A):
        raise ValueError("Matrix A must be a square matrix")
    A_sim = 0.5 * (A + A.T)  # Simmetric component of A
    A_anti = 0.5 * (A - A.T) # Antisymmetric component of A
    return (A_sim, A_anti)


def dist(A: np.ndarray, B: np.ndarray) -> float:
    return np.sqrt(np.trace((B - A) @ (B - A).T))

def linear_transformation(A: np.ndarray, *args: np.ndarray) -> None:
    pass


def module(v: np.ndarray):
    return np.sqrt(np.sum(v ** 2))


def inner_product(u: np.ndarray, v: np.ndarray) -> np.ndarray:
    return np.dot(u, v.conjugate())


def mixed_product(v: np.ndarray, u: np.ndarray, w: np.ndarray) -> Scalar:
    """
    Returns the mixed product of 2 vectors: (v ∧ u) x w or (v x u) · w,
    depending on the notation used
    """
    return np.dot(np.cross(v, u), w)


def parallel_vectors(v: np.ndarray, u: np.ndarray) -> bool:
    """
    Evaluates if two vectors are parallel.
    The module of the cross product between two 
    vectors is equivalent to the area of the parallelogram
    formed by them.
    Then, if v || u, the area of the parallelogram is 0,
    which implies |v ∧ u| = 0
    """
    return module(np.cross(v, u)) == 0


def orthogonal_vectors(u: np.ndarray, v: np.ndarray) -> bool:
    """
    Evaluates if two vectors are orthogonal (perpendicular)
    Two vectors are perpendicular if and only if (v x u) = 0 
    """
    return np.dot(u, v) == 0


def proy_vector(u: np.ndarray, v: np.ndarray) -> np.ndarray:
    """
    Returns the u vector proyection over v
    proy_u(v) = |v| cos(v ^ u) u_0 = (v x u_0)u_0
    """
    v_0 = normalize(v)
    alpha = np.dot(u, v_0)
    return alpha * v_0


def check_if_coplanar(u: np.ndarray, v: np.ndarray, w: np.ndarray) -> bool:
    """
    Evaluates if three vectors are coplanars.
    The absolute value mixed product between v,
    """
    return mixed_product(u, v, w) == 0


def angle_of_vectors(u: np.ndarray, v: np.ndarray) -> Real:
    """
    Returns the angle between two vectors (v ^ u)
    v · u = |v||u|·cos(v ^ u) 
    ==> (v x u) / (|v|·|u|) = cos(v ^ u)
    ==> arccos( (v x u) / (|v|·|u|) ) = (v ^ u)
    """
    x = np.dot(u, v) / (module(u) * module(v))
    return trigonometry.arccos(x)


def tensor_product(u: np.ndarray, v: np.ndarray) -> np.ndarray:
    w = []
    for i in u:
        for j in v:
            w.append(i * j)
    return np.array([w])


def characteristic_poly(A: np.ndarray) -> Polynomial:
    coefs = list(np.poly(A))
    return Polynomial(*coefs)


def is_symmetric(A: np.ndarray) -> bool:
    return A == A.T


def is_antisymmetric(A: np.ndarray):
    return -A == A.T


def is_hermitian(A: np.ndarray) -> bool:
    return A == A.conjugate()


def normalize(v: np.ndarray) -> np.ndarray:
    """
    Returns the associated versor to the vector v,
    often called v_0.
    An associated versor of v is a vector such that
    it has the same direction and sense of v, but with
    module of 1. This can be obtained by multiplying v
    by a scalar equal to |v| ^ (-1) = 1 / |v|
    """
    return v / module(v)


def suppress_matrix(i: int, j: int, A: np.ndarray) -> np.ndarray:
    if i == j == -1:
        raise ValueError("i or j must be different from -1")
    
    m, n = A.shape
    
    if m <= i:
        raise IndexError(f"i = {i} is out of range for a matrix with first dimension {m}")
    elif n <= j:
        raise IndexError(f"j = {j} is out of range for a matrix with second dimension {n}")

    B = A.copy()
    if 0 <= i:
        B = np.vstack((B[:i], B[i+1:]))
    if 0 <= j:
        B = np.hstack((B[:,:j], B[:,j+1:]))

    return B


def vector_field(v: np.ndarray) -> str:
    """
    Returns a string refering to the mathematical
    vector field where v lives.
    - CC: complex field
    - RR: real field
    - ZZ: integer field
    - NN: natural field
    """
    dt = str(v.dtype)
    if "complex" in dt:
        # If dtype of array is complex then 
        # the vector field where v lives on is
        # assumed to be CC
        field = "CC"
    else:
        field = "RR"
        # Check if components are of type integer.
        # If not, then the field is assumed to be RR.
        if "int" in dt:
            # If all components are greater than 0,
            # then the vector field will be taken as NN,
            # else ZZ
            field = "NN" if np.all(v > 0) else "ZZ"
    return field

def perm(A: np.ndarray):
    if not is_square_matrix(A):
        raise np.LinalgError("Matrix must be square to calculate permanent")
    if A.shape[0] >= 10:
        pass # Raise warning for non-polynomial operation, may take a lot of time
    
