from mathipy import calculus, _math

class Exponential(calculus.Function):
    function_type = 'Exponential'
    
    def __init__(self, a = _math.e, **kwargs):
        self.k = kwargs.get('k', 1)
        self.a = a
        self.n = kwargs.get('n', 1)
        self.b = kwargs.get('b', 0)
        self.c = kwargs.get('c', 0)
        if a == 1 or a == 0:
            raise ValueError('a should not be equal to 0 or 1')

    def get_yint(self):
        return self(0)

    def find_roots(self):
        try:
            root = (_math.log(-self.c / self.k, base= self.a) + self.b) / self.n
        except ValueError:
            root = None
        finally:
            return root

    def calculate_values(self, x):
        y = self.k * (self.a ** (self.n * x - self.b)) + self.c
        return y

    def plot_func(self, ax):
        y_int = self.get_yint()
        ax.scatter(0, y_int, color= calculus.Function.function_part['y-intercept'])
        if self.find_roots():
            ax.scatter(self.find_roots(), 0, color= calculus.Function.function_part['roots'])
        h_asymptote = self.c
        x_min, x_max = ax.get_xlim()
        ax.hlines(h_asymptote, x_min, x_max, color= calculus.Function.function_part['asymptote'], linewidth= 2.5, linestyle= '--')

    def __call__(self, x):
        return Exponential.calculate_values(self, x)

    def __str__(self):
        representation = ''
        if self.k != 1:
            representation += str(self.k) + ' · '
        if self.a == _math.e:
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

    def __repr__(self):
        return 'Exponential Function'