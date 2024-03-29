import math
from mathipy.math import ntheory, calculus


class Exponential(calculus.Function):
    """
    f(x) = k · a ^ (nx - b) + c
    """
    function_type = 'Exponential'
    
    def __init__(self, a: float = ntheory.e, **kwargs):
        self.k: float = kwargs.get('k', 1)
        self.a = a
        self.n: float = kwargs.get('n', 1)
        self.b: float = kwargs.get('b', 0)
        self.c: float = kwargs.get('c', 0)
        if a == 1 or a == 0:
            raise ValueError('a should not be equal to 0 or 1')

    def get_yint(self) -> float:
        return self(0)

    def find_roots(self) -> float:
        return (math.log(-self.c / self.k, self.a) + self.b) / self.n

    def calculate_values(self, x) -> float:
        y = self.k * (self.a ** (self.n * x - self.b)) + self.c
        return y

    def plot_func(self, ax) -> None:
        ax.scatter(0, self.get_yint(), color=calculus.Function.function_part['y-intercept'])
        ax.scatter(self.find_roots(), 0, color=calculus.Function.function_part['roots'])
        h_asymptote = self.c
        x_min, x_max = ax.get_xlim()
        ax.hlines(h_asymptote, x_min, x_max,
                  color=calculus.Function.function_part['asymptote'],
                  linewidth=2.5,
                  linestyle='--'
        )

    def __str__(self):
        representation = ''
        if self.k != 1:
            representation += str(self.k) + ' · '
        if self.a == ntheory.e:
            representation += 'e^(x'
        else:
            representation += f'{self.a}^('
        if self.n != 1:
            representation += f'{self.n}x'
        else:
            representation += 'x'
        if self.b > 0:
            representation += f' - {self.b})'
        elif self.b < 0:
            representation += f' + {-self.b})'
        else:
            representation += ')'
        if self.c > 0:
            representation += f' + {self.c}'
        elif self.c < 0:
            representation += f' - {-self.c}'
        return representation
