from mathipy import calculus, _math
from mathipy import numeric_operations as ops

class Log(calculus.Function):
    function_type = 'Logarithmic'
    asymptote = True
    def __init__(self, b = _math.e, **kwargs):
        self.__b = b
        self.__a = kwargs.get('a', 0)
        self.__c = kwargs.get('c', 1)
        self.__k = kwargs.get('k', 1)
        self.__n = kwargs.get('n', 1)
        self.__va = -self.__a / self.__k
        self.__root = self.find_roots()
        if b <= 1:
            raise ValueError('Base must be greater than 1')

    def get_yint(self):
        try:
            return self(0)
        except ValueError:
            return None

    def find_roots(self):
        exp = -self.__c / self.__n
        root = ((self.__b ** exp) - self.__a) / self.__k
        return root

    def calculate_values(self, x):
        if ops.is_scalar(x):
            try:
                return self.__n * _math.log(self.__k * x + self.__a, base= self.__b) + self.__c
            except ValueError:
                return None
        else:
            return list(map(self.calculate_values, x))

    def plot_func(self, ax):
        if self.get_yint() != None:
            y_intercept = self.get_yint()
            ax.scatter(0, y_intercept, color= calculus.Function.function_part['y-intercept'])

        if self.__root:
            ax.scatter(self.__root, 0, color= calculus.Function.function_part['roots'])

        v_asymptote = self.__va
        y_min, y_max = ax.get_ylim()
        ax.vlines(v_asymptote, y_min, y_max, color= calculus.Function.function_part['asymptote'], linewidth= 2.5, linestyle= '--')

    def __call__(self, x):
        return self.calculate_values(x)

    def __repr__(self):
        representation = ''
        if self.__n != 1:
            representation += f'{self.__n} · '
        if self.__b == _math.e:
            representation += 'ln('
        elif self.__b == 10:
            representation += 'log('
        else:  
            representation += f'log_{self.__b}('
        if self.__k != 1:
            representation += f'{self.__k}x'
        else:
            representation += 'x'
        if self.__a > 0:
            representation += f' + {self.__a})'
        elif self.__a < 0:
            representation += f' - {abs(self.__a)})'
        else:
            representation += ')'
        if self.__c > 0:
            representation += f' + {self.__c}'
        elif self.__c < 0:
            representation += f' - {abs(self.__c)}'