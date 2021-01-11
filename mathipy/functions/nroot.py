from mathipy import calculus, _math
from mathipy._complex import Complex

class NRoot(calculus.Function):
    function_type = 'N-Root'
    def __init__(self, n = 2, **kwargs):
        self.__a = kwargs.get('a', 1)
        self.__n = n
        self.__k = kwargs.get('k', 1)
        self.__p = kwargs.get('p', 0)
        self.__b = kwargs.get('b', 0)

        if n == 0:
            raise ValueError('Root index cannot be 0')

    @staticmethod
    def root(arg, index = 2, return_complex = True):
        if _math.is_iter(arg):
            return np.array([NRoot.root(i, index, return_complex) for i in arg])
        if arg >= 0:
            return arg ** (1/index)
        else:
            if index % 2 == 0:
                return Complex(0, NRoot.root(-arg)) if return_complex else None
            else:
                return - NRoot.root(-arg, index)

    def get_yint(self):
        return self(0)

    def find_roots(self):
        r = ((-self.__b / self.__a) ** (self.__n) - self.__p) / self.__k
        if self(r) == 0: return r
        else:
            return None

    def calculate_values(self, x):
        f = lambda x: self.__a * NRoot.root((self.__k * x + self.__p), self.__n, return_complex = False) + self.__b
        try:
            y = f(x)
        except TypeError:
            if _math.is_iter(x):
                return [self.calculate_values(i) for i in x]
            else: return None
        else:
            return y

    def __call__(self, x):
        return self.calculate_values(x)

    def plot_func(self, ax):
        ax.scatter(0, self.get_yint(), color = calculus.Function.function_part['y-intercept'])
        ax.scatter(self.find_roots(), 0, color = calculus.Function.function_part['roots'])

    def __repr__(self):
        representation = ''
        if self.__a != 1:
            representation += f'{self.__a} · '
        if self.__n != 2:
            representation += f'Root{self.__n}('
        else:
            representation += 'Sqrt('
        if self.__k != 1:
            representation += f'{self.__k}x'
        else:
            representation += 'x'
        if self.__p != 0:
            representation += f' + {self.__p})'
        else:
            representation += f')'
        if self.__b != 0:
            representation += f' + {self.__b}'
        return representation