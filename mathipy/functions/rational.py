import numpy as np
from mathipy import calculus
from typing import TypeVar, Generic

Polynomial = TypeVar('Polynomial')

class Rational(calculus.Function):
    function_type = 'Rational'

    def __init__(self, p: Generic[Polynomial], q: Generic[Polynomial]):
        self.p = p
        self.q = q

        self.v_asymptote: float = self.q.find_roots()
    
    def get_yint(self) -> float:
        return self(0)

    def find_roots(self) -> float:
        return self.p.find_roots()

    def calculate_values(self, x):
        y = self.p(x) / self.q(x)

        lim = 500
        y = np.clip(y, -lim, lim)
        return y

    def __call__(self, x):
        try:
            return self.p(x) / self.q(x)
        except ZeroDivisionError:
            return float('inf')

    def plot_func(self, ax):
        ax.scatter(0, self.get_yint(), color= calculus.Function.function_part['y-intercept'])
        if roots := self.find_roots():
            for root in roots:
                ax.scatter(root, 0, color = calculus.Function.function_part['roots'])
        x_min, x_max = ax.get_xlim()
        y_min, y_max = ax.get_ylim()
        for a in self.v_asymptote:
            ax.vlines(a, y_min, y_max, color= calculus.Function.function_part['asymptote'], linewidth= 2.5, linestyle= '--')

    def __str__(self):
        return f'({self.p}) / ({self.q})'

class Homographic(Rational):
    function_type = 'Homographic'

    def __init__(self, p1, p0, q1, q0):
        self.p = (p0, p1)
        self.q = (q0, q1)
        self.h_asymptote = self.p[1] / self.q[1]
        self.v_asymptote = -self.q[0] / self.q[1]

        if self.p[1] * self.q[0] == self.p[0] * self.q[1]:
            raise ValueError(f'Function is not homographic, received p: {p} and q: {q}')

    def find_roots(self):
        try:
            return [-self.p[0] / self.p[1]]
        except ZeroDivisionError:
            return np.nan

    def get_yint(self):
        return self(0)

    def calculate_values(self, x):
        y = (self.p[1] * x + self.p[0]) / (self.q[1] * x + self.q[0])
        
        #lim = 500
        #y = np.clip(y, -lim, lim)
        return y

    def plot_func(self, ax):
        x_min, x_max = ax.get_xlim()
        y_min, y_max = ax.get_ylim()
        ax.hlines(self.h_asymptote, x_min, x_max, color=calculus.Function.function_part['asymptote'], linewidth= 2.5, linestyle= '--')
        ax.vlines(self.v_asymptote, y_min, y_max, color=calculus.Function.function_part['asymptote'], linewidth= 2.5, linestyle= '--' )

    def __call__(self, x):
        try:
            return self.calculate_values(x)
        except ZeroDivisionError:
            return float('inf')

    def __str__(self):
        return f'{self.p[1]}x + {self.p[0]} / {self.q[1]}x + {self.q[0]}'