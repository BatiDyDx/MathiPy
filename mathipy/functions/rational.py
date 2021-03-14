import numpy as np
from mathipy import calculus

class Rational(calculus.Function):
    function_type = 'Rational'

    def __init__(self, p, q):
        self.p = p
        self.q = q
        self.is_homographic = False
        if (p.degree == 0 or p.degree == 1) and q.degree == 1:
            if p[1] * q[0] != p[0] * q[1]:
                self.is_homographic = True
        self.va = self.get_v_asymptote()
        self.ha = self.get_h_asymptote()
    
    def get_yint(self):
        return self(0)

    def get_v_asymptote(self):
        if self.is_homographic:
            return [-self.q[0] / self.q[1]]
        else:
            pass

    def get_h_asymptote(self):
        if self.is_homographic:
            return [self.p[1] / self.q[1]]

    def find_roots(self):
        if self.is_homographic:
            try:
                return [-self.p[0] / self.p[1]]
            except ZeroDivisionError:
                return np.nan

    def calculate_values(self, x):
        def f(x):
            try:
                return self.p(x) / self.q(x)
            except ZeroDivisionError:
                return np.nan

        y_min, y_max = -500, 500
        y = np.clip(f(x), y_min, y_max)
        return y

    def __call__(self, x):
        try:
            return self.p(x) / self.q(x)
        except ZeroDivisionError:
            return float('inf')

    def plot_func(self, ax):
        ax.scatter(0, self.get_yint(), color= calculus.Function.function_part['y-intercept'])
        if self.find_roots():
            for root in self.find_roots():
                ax.scatter(root, 0, color = calculus.Function.function_part['roots'])
        x_min, x_max = ax.get_xlim()
        y_min, y_max = ax.get_ylim()
        ax.hlines(self.get_h_asymptote(), x_min, x_max, color= calculus.Function.function_part['asymptote'], linewidth= 2.5, linestyle= '--')
        for a in self.get_v_asymptote():
            ax.vlines(a, y_min, y_max, color= calculus.Function.function_part['asymptote'], linewidth= 2.5, linestyle= '--')

    def __str__(self):
        return f'({self.p}) / ({self.q})'

    def __repr__(self):
        return 'Rational Function'