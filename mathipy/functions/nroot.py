from mathipy import calculus, _math

class NRoot(calculus.Function):
    function_type = 'N-Root'
    def __init__(self, n = 2, **kwargs):
        self.a = kwargs.get('a', 1)
        self.n = n
        self.k = kwargs.get('k', 1)
        self.p = kwargs.get('p', 0)
        self.b = kwargs.get('b', 0)

        if n == 0:
            raise ValueError('Root index cannot be 0')

    def get_yint(self):
        return self(0)

    def find_roots(self):
        r = ((-self.b / self.a) ** (self.n) - self.p) / self.k
        return r if self(r) == 0 else None

    def calculate_values(self, x):
        return self.a * _math.root_n((self.k * x + self.p), self.n, return_complex= False) + self.b


    def __call__(self, x):
        return self.calculate_values(x)

    def plot_func(self, ax):
        ax.scatter(0, self.get_yint(), color= calculus.Function.function_part['y-intercept'])
        ax.scatter(self.find_roots(), 0, color= calculus.Function.function_part['roots'])

    def __str__(self):
        representation = ''
        if self.a != 1:
            representation += f'{self.a} · '
        if self.n != 2:
            representation += f'Root{self.n}('
        else:
            representation += 'Sqrt('
        if self.k != 1:
            representation += f'{self.k}x'
        else:
            representation += 'x'
        if self.p != 0:
            representation += f' + {self.p})'
        else:
            representation += f')'
        if self.b != 0:
            representation += f' + {self.b}'
        return representation

    def __repr__(self):
        return 'N-Root Function'