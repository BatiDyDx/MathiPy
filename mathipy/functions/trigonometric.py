import numpy as np
from mathipy import calculus, _math

class Trigonometric(calculus.Function):
    function_type = 'Trigonometric'
    def __init__(self, n = 1, **kwargs):
        self.a = kwargs.get('a', 1)
        self.n = n
        self.k = kwargs.get('k', 0)
        self.c = kwargs.get('c', 0)
        self.exp = kwargs.get('exp', 1)
        self.period = _math.tau / self.n

    def calculate_values(self, x):
        y = self.a * (self.trigonometric_function(self.n * x + self.k) ** self.exp) + self.c
        return y

    def __call__(self, x):
        return self.calculate_values(x)

    def plot_func(self, ax):
        ax.scatter(0, self(0), color=calculus.Function.function_part['y-intercept'])
        x_min, x_max = ax.get_xlim()
        roots = [root for root in self.find_roots(x_min, x_max)]
        zeros = [0] * len(roots)
        print(roots, zeros)
        ax.scatter(roots, zeros, color = calculus.Function.function_part['roots'])
        #temporal solution
        try:
            if isinstance(self, (Tan, Cotan, Cosec, Sec)):
                ax.set_ylim(-3,3)
        except NameError:
            ax.set_ylim(-3,3)

    def __repr__(self):
        representation = ''
        if self.a != 1:
            representation += f'{self.a}'
        representation += self.function_representation
        if self.exp != 1:
            representation += f'^({self.exp})'
        if self.n != 1:
            representation += f'({self.n}x'
        else:
            representation += '(x'
        if self.k != 0:
            representation += f' + {self.k})'
        else:
            representation += ')'
        if self.c != 0:
            representation += f'{self.c}'
        return representation

#TODO
#programar seno, coseno, tangente, 
#sus reciprocas y sus inversas

class Sin(Trigonometric):
    trigonometric_function = lambda s, x: _math.sin(x)
    function_representation = 'Sin'

    def find_roots(self, lower_bound, upper_bound, **kwargs):
        min_int = int(np.floor(lower_bound * abs(self.n) / _math.pi - 1))
        max_int = int(np.ceil( upper_bound * abs(self.n) / _math.pi + 1))
        ints = [i for i in range(min_int, max_int)]
        #f = lambda i:(_math.pi * i  - self.k) / self.n
        f = lambda i: i * (np.arcsin(-self.c / self.a)  - self.k) / self.n
        if f(1) == 0:
            f = lambda i: i * _math.pi
        p_roots = [f(i) for i in ints if lower_bound <= f(i) <= upper_bound]
        roots = list(filter(lambda root: True if -1e-14 < self(root) < 1e-14 else False, p_roots))
        return roots

    def find_roots2(self, lower_bound, upper_bound, **kwargs):
        x = (np.arcsin(-self.c / self.a) - self.k) / self.n
        if x == 0:
            x = _math.pi
        ints = range(lower_bound, upper_bound + 1)
        p_roots = [x * i for i in ints if lower_bound <= (x * i) <= upper_bound]
        roots = [root for root in p_roots if -1e-14 < self(root) < 1e-14]
        return roots

class Cos(Trigonometric):
    trigonometric_function = lambda s, x: _math.cos(x)
    function_representation = 'Cos'

    def find_roots(self, lower_bound, upper_bound, **kwargs):
        min_int = int(np.floor(lower_bound * abs(self.n) / _math.pi - 1))
        max_int = int(np.ceil( upper_bound * abs(self.n) / _math.pi + 1))
        ints = [i for i in range(min_int, max_int)]
        f = lambda i:(_math.pi * i + _math.pi/2 - self.k) / self.n
        p_roots = [f(i) for i in ints if lower_bound <= f(i) <= upper_bound]
        roots = list(filter(lambda root: True if -1e-14 < self(root) < 1e-14 else False, p_roots))
        return roots

class Tan(Trigonometric):
    trigonometric_function = _math.tan
    function_representation = 'Tg'

#class Cosec(Trigonometric):
#  trigonometric_function = Cosec().csc
#  function_representation = 'Csc'
#
#  @classmethod
#  def csc(cls,x):
#    y = _math.sin(x)
#    if y != 0:
#      return 1 / y
#    else:
#      return Infinite()

#class Sec(Trigonometric):
#  trigonometric_function = Sec.sec
#  function_representation = 'Sec'
#  
#  @classmethod
#  def sec(cls, x):
#    return 1 / _math.cos(x)
#
#class Cotan(Trigonometric):
#  trigonometric_function = Cotan.ctg
#  function_representation = 'Ctg'
#  
#  @classmethod
#  def ctg(cls, x):
#    return 1 / _math.tan(x)
