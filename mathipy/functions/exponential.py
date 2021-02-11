from mathipy import calculus, _math
from mathipy.functions import logarithmic

class Exponential(calculus.Function):
    function_type = 'Exponential'
    asymptote = True
    def __init__(self, a = _math.e, **kwargs):
        self.__k = kwargs.get('k', 1)
        self.__a = a
        self.__n = kwargs.get('n', 1)
        self.__b = kwargs.get('b', 0)
        self.__c = kwargs.get('c', 0)
        self.__root = self.find_roots()
        if a == 1 or a == 0:
            raise ValueError('a should not be equal to 0 or 1')

    def get_yint(self):
        return self(0)

    def find_roots(self):
        try:
            root = (_math.log(-self.__c / self.__k, base= self.__a) + self.__b) / self.__n
        except ValueError:
            root = None
        finally:
            return root

    def calculate_values(self, x):
        y = self.__k * (self.__a ** (self.__n * x - self.__b)) + self.__c
        return y

    def plot_func(self, ax):
        y_int = self.get_yint()
        ax.scatter(0, y_int, color= calculus.Function.function_part['y-intercept'])
        if self.__root:
            ax.scatter(self.__root, 0, color= calculus.Function.function_part['roots'])
        h_asymptote = self.__c
        x_min, x_max = ax.get_xlim()
        ax.hlines(h_asymptote, x_min, x_max, color= calculus.Function.function_part['asymptote'], linewidth= 2.5, linestyle= '--')

    def __call__(self, x):
        return Exponential.calculate_values(self, x)

    def __repr__(self):
        representation = ''
        if self.__k != 1:
            representation += str(self.__k) + ' · '
        if self.__a == _math.e:
            representation += 'e^(x'
        else:
            representation += f'{self.__a}^('
        if self.__n != 1:
            representation += f'{self.__n}x'
        else:
            representation += 'x'
        if self.__b > 0:
            representation += f' - {self.__b})'
        elif self.__b < 0:
            representation += f' + {abs(self.__b)})'
        else:
            representation += ')'
        if self.__c > 0:
            representation += f' + {self.__c}'
        elif self.__c < 0:
            representation += f' - {abs(self.__c)}'
        return representation