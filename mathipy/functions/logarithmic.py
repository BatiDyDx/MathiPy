import mathipy as mpy
from mathipy import calculus, _math

class Log(calculus.Function):
    function_type = 'Logarithmic'
    asymptote = True
    def __init__(self, b = _math.e, **kwargs):
        self.b = b
        self.a = kwargs.get('a', 0)
        self.c = kwargs.get('c', 0)
        self.k = kwargs.get('k', 1)
        self.n = kwargs.get('n', 1)
        self.va = -self.a / self.k
        if b <= 1:
            raise ValueError('Base must be greater than 1')

    def get_yint(self):
        return self(0)

    def find_roots(self):
        exp = -self.c / self.n
        root = ((self.b ** exp) - self.a) / self.k
        return root

    def calculate_values(self, x):
        return self.n * _math.log(self.k * x + self.a, base= self.b) + self.c

    def plot_func(self, ax):
        ax.scatter(0, self.get_yint(), color= calculus.Function.function_part['y-intercept'])

        if self.find_roots():
            ax.scatter(self.find_roots(), 0, color= calculus.Function.function_part['roots'])

        y_min, y_max = ax.get_ylim()
        ax.vlines(self.va, y_min, y_max, color= calculus.Function.function_part['asymptote'], linewidth= 2.5, linestyle= '--')

    def __call__(self, x):
        return self.calculate_values(x)

    def __str__(self):
        representation = ''
        if self.n != 1:
            representation += f'{self.n} · '
        if self.b == _math.e:
            representation += 'ln('
        elif self.b == 10:
            representation += 'log('
        else:  
            representation += f'log_{self.b}('
        if self.k != 1:
            representation += f'{self.k}x'
        else:
            representation += 'x'
        if self.a > 0:
            representation += f' + {self.a})'
        elif self.a < 0:
            representation += f' - {-self.a})'
        else:
            representation += ')'
        if self.c > 0:
            representation += f' + {self.c}'
        elif self.c < 0:
            representation += f' - {-self.c}'

    def __repr__(self):
        return 'Log Function'