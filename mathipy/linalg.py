import numpy as np
import matplotlib.pyplot as plt
from mathipy import _math
from mathipy import numeric_operations as ops

class Tensor():
    """
    Tensor class:
    Vector or Matrix

    """
    pass

class Vector(Tensor):
    rank = 1
    def __init__(self, *args): 
        self.__elements = list(args)
        self.__dimension = len(self.__elements)
        self.__magnitude = _math.sqrt(sum(map(lambda v: v**2, self.__elements)))
        self.__field = 'C'
        for e in self.__elements:
            if isinstance(e, complex):
                break
        else:
            self.__field = 'R'

    @property
    def module(self):
        return self.__magnitude

    def __add__(v, u):
        if v.__dimension == u.__dimension:
            i = zip(v.__elements, u.__elements)
            w_elements = [x + y for x, y in i]
            return Vector(*w_elements)
        else:
            raise ValueError(f'Vector dimension must be equal, but received {v.__dimension} and {u.__dimension}')

    def __sub__(v, u):
        return v + (-u)

    def __neg__(v):
        neg_values = [-x for x in v.__elements]
        return Vector(*neg_values)

    def __mul__(v, u):
        return v.dot_product(u)

    def __matmul__(v, u):
        return v.tensor_product(u)

    def __rmul__(v, u):
        return v.dot_product(u)

    def __abs__(self):
        return self.__magnitude

    def __iter__(self):
        return iter(self.__elements)

    def __getitem__(self, index):
        return self.__elements[index]

    def dot_product(v, u):
        if isinstance(u, Vector):
            if v.__field == 'C' and u.__field == 'C':
                return v.inner_product(u)

            if v.__dimension == u.__dimension:
                cross_product = 0
                for v_el, u_el in zip(v.__elements, u.__elements):
                    cross_product += v_el * u_el
                return cross_product
    
        elif ops.is_scalar(u):
            scaled_v = map(lambda val: val * u, v.__elements)
            return Vector(*scaled_v)

        elif isinstance(u, Matrix):
            return u.__rmul__(v)

    def inner_product(v, u):
        u_prime = Vector(*[i.conjugate() for i in u])
        return v.dot_product(u_prime)

    def cross_product(self, *args):
        pass
    
    def tensor_product(v, u):
        w = []
        for i in v:
            for j in u:
                w.append(i * j)
        return Vector(*w)

    def transpose(self):
        return Matrix(self.__elements)

    def to_matrix(self):
        return Matrix(*[[n] for n in self.__elements])

    def plot(self):
        if self.__dimension != 2:
            raise ValueError('Only 2-dimensional vectors can be graphed')

        i, j = self.__elements
        #i_min, i_max = - abs(i) - 1, abs(i) + 1
        fig, ax = plt.subplots()

        ax.set_title("Vector plot")
        plt.style.use('dark_background')

        plt.ylabel('$j$')
        plt.xlabel('$i$')
        plt.grid()

        head_w = self.__magnitude / 45
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

    def __repr__(self):
        return f'Vector({self.__elements})'

class Matrix(Tensor):
    rank = 2
    def __init__(self, *args):
        self.__elements = ops.round_int(list(args))
        self.m_dimension = len(self.__elements)
        self.n_dimension = max([len(row) for row in self.__elements])
        self.shape = (self.m_dimension, self.n_dimension)
        self.__fill_rows()
        self.__dimension = self.n_dimension * self.m_dimension
        self.__square_matrix = True if self.n_dimension == self.m_dimension else False

    def __fill_rows(self):
        n_dim = self.n_dimension
        for i in range(self.m_dimension):
            while len(self.__elements[i]) < n_dim:
                self.__elements[i].append(0)

    @property
    def t(self):
        return self.transpose()

    @property
    def c(self):
        return self.cofactorial()

    @property
    def a(self):
        return self.adjugate()

    @property
    def det(self):
        return self.determinant()

    @staticmethod
    def k_matrix(k, m, n):
        elements = [[k] * n for _ in range(m)] 
        return Matrix(*elements)

    @staticmethod
    def zeros_matrix(m, n):
        return Matrix.k_matrix(0, m, n)

    @staticmethod
    def ones_matrix(m, n):
        return Matrix.k_matrix(1, m, n)

    @staticmethod
    def identity(size):
        rows = []
        for i in range(size):
            row = [(1 if i == j else 0) for j in range(size)]
            rows.append(row)
        return Matrix(*rows)

    def is_square(self):
        return self.__square_matrix

    def transpose(self):
        t_rows = []
        for i in range(self.n_dimension):
            t_rows.append(self[:, i])
        return Matrix(*t_rows)

    def determinant(self):
        if not self.is_square():
            raise ValueError('Matrix must be square to calculate determinant')
        else:
            if self.shape == (2,2):
                return (self[0][0] * self[1][1]) - (self[0][1] * self[1][0])
            else:
                det = 0
                #Ignore the first row
                A_i = self[1:]
                #Iter over the columns of the matrix
                for i in range(self.n_dimension):
                    #Store the elements that do not correspond 
                    #to the actual row or column
                    cA_ij = []
                    #Iter over the rows of the shortened matrix
                    for j in range(len(A_i)):
                        #Store the row ignoring the actual column
                        cA_ij.append(A_i[j][0:i] + A_i[j][i+1:])
                    #Add the determinant of cA_ij, times 
                    #the a_ij element, fliping the sign
                    det += (-1) ** (i%2) * Matrix(*cA_ij).determinant() * self[0][i]
                return det

    def cofactorial(self):
        if not self.is_square():
            raise ValueError('Matrix must be square to calculate cofactorial')
        else:
            A_c = Matrix.zeros_matrix(*self.shape)
            #Iter over the rows of the matrix
            for i in range(self.m_dimension):
                #Ignore the actual row
                A_i = self[0:i] + self[i+1:]
                #Iter over the columns
                for j in range(self.n_dimension):
                    #Store the elements ignoring the actual row and column
                    cA_ij = []
                    #Iter over the shortened matrix
                    for h in range(len(A_i)):
                        #Add to cA_ij the elements
                        cA_ij.append(A_i[h][0:j] + A_i[h][j+1:])
                    det_ij = Matrix(*cA_ij).determinant()
                    #Set the i-row and j-column equal to the determinant
                    #of cA_ij altering its sign
                    A_c[i, j] = (-1) ** (i + j) * det_ij
            return A_c

    def adjugate(self):
        return self.cofactorial().t

    def inverse(self):
        return self.adjugate() * (1 / self.determinant())

    def __add__(A, B):
        if A.shape == B.shape:
            C = Matrix.zeros_matrix(*A.shape)
            for i in range(C.m_dimension):
                for j in range(C.n_dimension):
                    C[i, j] = A[i][j] + B[i][j]
            return C
        else:
            raise ValueError(f'Matrices can only be summed if they have same shape, received {A.shape} and {B.shape}')

    def __sub__(A, B):
        return A + (-B)

    def __neg__(A):
        return -1 * A

    def __mul__(A, B):
        C = Matrix.zeros_matrix(*A.shape)
        if isinstance(B, Tensor):
            if not A.shape == B.shape:
                raise ValueError(f'Matrices can only be summed if they have same shape, received {A.shape} and {B.shape}')
        for i in range(A.m_dimension):
            for j in range(A.n_dimension):
                C[i, j] = A[i][j] * B[i][j]
        return C


    def __matmul__(A, B):
        if isinstance(B, Tensor):
            if isinstance(B, Vector):
                return A * B.to_matrix()
            elif A.n_dimension == B.m_dimension:
                C = Matrix.zeros_matrix(A.m_dimension, B.n_dimension)
                for i in range(A.m_dimension):
                    for j in range(B.n_dimension):
                        v = Vector(*A[i])
                        u = Vector(*B[:, j])
                        C[i, j] = v * u
                return Matrix(*C.__elements)
            else:
                raise ValueError(
            f"First matrix n-dimension must be equal to second matrix m-dimension. Received {A.n_dimension} and {B.m_dimension}"
            )
        

    def __rmatmul__(A, B):
        if ops.is_scalar(B):
            return A * B
        elif isinstance(B, Vector):
            return B.to_matrix() * A

    def __truediv__(A, B):
        if ops.is_scalar(B):
            return A * (1 / B)
        else:
            return A * (B ** -1)

    def __rtruediv__(A, B):
        if ops.is_scalar(B):
            return (A ** -1) * B

    def __pow__(self, n):
        if not isinstance(n, int):
            raise ValueError('Exponent must be an integer')
        if n == 1 or n == 0:
            return self
        elif n > 1:
            return self * self ** (n - 1)
        else:
            return self.inverse() ** (-n)

    def __iter__(self):
        elements_list = []
        for i in self.__elements:
            elements_list += i
        return iter(elements_list)

    def __getitem__(self, index):
        if isinstance(index, tuple):
            index, col = index
            return [i[col] for i in self.__elements[index]]
        else:
            return self.__elements[index]

    def __setitem__(self, index, value):
        m, n = index
        self.__elements[m][n] = value

    def __repr__(self):
        expression = 'Matrix(\n'
        expression += ' ' + str(np.array(self.__elements))[1:-1]
        expression += ') \n'
        return expression

def linear_transformation(M, V):
    pass