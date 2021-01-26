import matplotlib.pyplot as plt
import numpy as np
from mathipy import _complex

class LinearAlgebra():
    pass

class Vector(LinearAlgebra):
    def __init__(self, *args):
        self.__elements = [x for x in args]
        self.__dimension = len(self.__elements)
        self.__magnitude = np.sqrt(sum(map(lambda v: v**2, self.__elements)))
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
    
        elif isinstance(u, (int, float, complex, _complex.Complex)):
            scaled_v = map(lambda val: val * u, v.__elements)
            return Vector(*scaled_v)

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

class Matrix(LinearAlgebra):
    def __init__(self, *args):
        self.__elements = list(args)
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

    def __add__(A, B):
        if A.shape == B.shape:
            pass
        else:
            raise ValueError(f'Matrices can only be summed if they have same shape, received {A.shape} and {B.shape}')

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

    def __repr__(self):
        expression = 'Matrix('
        for row in self.__elements:
            expression += '\n    ' + str(row)
        expression += ')'
        return expression