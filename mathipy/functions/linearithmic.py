import numpy as np
from mathipy.math import calculus, _math

class Linearithmic(calculus.Function):
    """
    f(x) = (mx + h)log_b(kx + a)
    """
    function_type = 'Linearithmic'

    def __init__(self, m = 1, h = 0, b = 10, a = 0, k = 1):
        self.m = m
        self.h = h
        self.b = b
        self.a = a
        self.k = k

    def find_roots(self) -> tuple:
        x1 = - self.h / self.m
        x2 = (1 - self.a) / self.k
        x1 = x1 if self(x1) == 0 else np.nan
        x2 = x2 if self(x2) == 0 else np.nan
        return (x1, x2)

    def plot_func(self, ax):
        ax.scatter(self.find_roots(), (0,0), color=calculus.Function.function_part['roots'])
        ax.scatter(0, self.get_yint(), color=calculus.Function.function_part['y-intercept'])

    def calculate_values(self, x):
        return (self.m * x + self.h) * _math.log(self.k * x + self.a, base = self.b)

    def __call__(self, x):
        return self.calculate_values(x)

    def __str__(self):
        representation = ''
        representation += f'({self.m}x + {self.h})'
        representation += f'log_{self.b}({self.k}x + {self.a})'
        return representation