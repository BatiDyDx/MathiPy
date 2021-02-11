from mathipy import calculus, polynomial as poly
from mathipy import numeric_operations as ops

class Rational(calculus.Function):
    function_type = 'Rational'

    def __init__(self, p: poly.Polynomial, q: poly.Polynomial, **kwargs):
        self.p = p
        self.q = q
        self.is_homographic = False
        if (p.degree == 0 or p.degree == 1) and q.degree == 1:
            if p[1] * q[0] != p[0] * q[1]:
                self.is_homographic = True
        self.roots = self.find_roots()
        self.va = self.get_v_asymptote()
        self.ha = self.get_h_asymptote()
    
    def get_yint(self):
        return self(0)

    def get_v_asymptote(self):
        if self.is_homographic:
            return [-self.q[0] / self.q[1]]
        else:
        #return all roots of q
            pass

    def get_h_asymptote(self):
        if self.is_homographic:
            return [self.p[1] / self.q[1]]

    def find_roots(self):
        if self.is_homographic:
            try:
                return [-self.p[0] / self.p[1]]
            except ZeroDivisionError:
                return None

    def calculate_values(self, x):
        y = self.p(x) / self.q(x)
        if not ops.is_iter(x):
            y = np.array([y])
        y = [i if -150 <= i <= 150 else None for i in y]
        return y

    def __call__(self, x):
        try:
            return self.p(x) / self.q(x)
        except ZeroDivisionError:
            return float('inf')

    def plot_func(self, ax):
        ax.scatter(0, self.get_yint(), color = calculus.Function.function_part['y-intercept'])
        if self.roots:
            for root in self.roots:
                ax.scatter(root, 0, color = calculus.Function.function_part['roots'])
        x_min, x_max = ax.get_xlim()
        y_min, y_max = ax.get_ylim()
        ax.hlines(self.ha, x_min, x_max, color = calculus.Function.function_part['asymptote'], linewidth = 2.5, linestyle = '--')
        for a in self.va:
            ax.vlines(a, y_min, y_max, color = calculus.Function.function_part['asymptote'], linewidth = 2.5, linestyle = '--')
