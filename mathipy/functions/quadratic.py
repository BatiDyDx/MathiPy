from mathipy import calculus, polynomial, _complex, _math


class Quadratic(calculus.Function):
    function_type = 'Quadratic'

    def __init__(self, a: float = 1, **kwargs):
        self.a = a
        self.degree: int = 2
        if 'b' in kwargs and 'c' in kwargs:
            b, c = kwargs['b'], kwargs['c']
            self.b: float = b
            self.c: float = c
            self.x1, self.x2 = self.roots = quadratic_roots(a=self.a, b=self.b, c=self.c)
            self.xv: float = - self.b / (2 * self.a)
            self.yv: float = self.a * (self.xv ** 2) + self.b * self.xv + self.c
        elif 'xv' in kwargs and 'yv' in kwargs:
            xv, yv = kwargs['xv'], kwargs['yv']
            self.xv: float = xv
            self.yv: float = yv
            self.b: float = (-2 * self.xv) * self.a
            self.c: float = ((self.xv ** 2) * self.a) + self.yv
            self.x1, self.x2 = self.roots = quadratic_roots(a=self.a, b=self.b, c=self.c)
        elif 'x1' in kwargs and 'x2' in kwargs:
            x1, x2 = kwargs['x1'], kwargs['x2']
            self.x1, self.x2 = x1, x2
            self.b: float = -(self.x1 + self.x2) * self.a
            self.c: float = (self.x1 * self.x2) * self.a
            self.xv: float = - self.b / (2 * self.a)
            self.yv: float = self.a * (self.xv ** 2) + self.b * self.xv + self.c
            self.roots: list[float, float] = [self.x1, self.x2]
        else:
            raise ValueError('Expression type not admitted') 

        if self.a == 0:
            raise ValueError('a term cannot be equal to 0')

    def get_roots(self) -> list[float, float]:
        return self.roots

    def get_vertex(self) -> tuple[float, float]:
        return self.xv, self.yv

    def calculate_values(self, x) -> float:
        y = (self.a * (x**2)) + (self.b * x) + self.c
        return y

    def plot_func(self, ax) -> None:
        if not isinstance(self.x1, _complex.Complex):
            ax.scatter(self.roots, (0,0), c=calculus.Function.function_part['roots'])
        ax.scatter(*self.get_vertex(), c=calculus.Function.function_part['vertex'])
        ax.scatter(0, self.c, c=calculus.Function.function_part['y-intercept'])

    def vertex_expression(self) -> str:
        vertex_exp = f'{self.a}'
        if self.xv > 0:
            vertex_exp += f'(x - {self.xv})^2'
        elif self.xv < 0:
            vertex_exp += f'(x + {-self.xv})^2'
        else:
            vertex_exp += 'x^2'
    
        if self.yv > 0:
            vertex_exp += f' + {self.yv}'
        elif self.yv < 0:
            vertex_exp += f' - {-self.yv}'
    
        return vertex_exp

    def factored_expression(self) -> str:
        factored_exp = f'{self.a}'
        if self.x1 == self.x2:
            if self.x1 > 0:
                factored_exp += f'(x - {self.x1})^2'
            elif self.x1 < 0:
                factored_exp += f'(x + {-self.x1})^2'
            else:
                factored_exp += 'x^2'
        else:
            if self.x1 > 0:
                factored_exp += f'(x - {self.x1})'
            elif self.x1 < 0:
                factored_exp += f'(x + {-self.x1})'
            else:
                factored_exp += 'x'

            if self.x2 > 0:
                factored_exp += f'(x - {self.x2})'
            elif self.x2 < 0:
                factored_exp += f'(x + {-self.x2})'
            else:
                factored_exp += 'x'

        return factored_exp

    def __str__(self):
        return polynomial.Polynomial(
            a2= self.a, 
            a1= self.b, 
            a0= self.c
        ).__str__()


def quadratic_roots(a, b, c):
    root_body = b ** 2 - (4 * a * c)
    if a == 0:
        raise ValueError('a term cannot be equal to 0')

    if root_body == 0:
        return -b/(2*a)

    elif root_body < 0:
        x1_real = x2_real = - b / (2 * a)
        x1_imag = _math.sqrt(_math.abs(root_body)) / (2 * a)
        x2_imag = - _math.sqrt(_math.abs(root_body)) / (2 * a)
        x1 = _complex.Complex(x1_real, x1_imag)
        x2 = _complex.Complex(x2_real, x2_imag)

    elif root_body > 0:
        x1 = (-b + _math.sqrt(root_body)) / (2 * a)
        x2 = (-b - _math.sqrt(root_body)) / (2 * a)

    return x1, x2
