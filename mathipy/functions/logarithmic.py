import math
from mathipy.math import ntheory, calculus


class Log(calculus.Function):
    function_type = 'Logarithmic'
    asymptote = True

    def __init__(self, b: float = ntheory.e, **kwargs):
        self.b = b
        self.a: float = kwargs.get('a', 0)
        self.c: float = kwargs.get('c', 0)
        self.k: float = kwargs.get('k', 1)
        self.n: float = kwargs.get('n', 1)
        self.va: float = -self.a / self.k
        if b <= 1:
            raise ValueError('Base must be greater than 1')

    def get_yint(self) -> float:
        return self(0)

    def find_roots(self) -> float:
        exp = -self.c / self.n
        root = ((self.b ** exp) - self.a) / self.k
        return root

    def calculate_values(self, x) -> float:
        return self.n * math.log(self.k * x + self.a, self.b) + self.c

    def plot_func(self, ax) -> None:
        ax.scatter(0, self.get_yint(), color= calculus.Function.function_part['y-intercept'])

        if self.find_roots():
            ax.scatter(self.find_roots(), 0, color= calculus.Function.function_part['roots'])

        y_min, y_max = ax.get_ylim()
        ax.vlines(self.va, y_min, y_max, color= calculus.Function.function_part['asymptote'], linewidth= 2.5, linestyle= '--')

    def __str__(self):
        representation = ''
        if self.n != 1:
            representation += f'{self.n} · '
        if self.b == ntheory.e:
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
