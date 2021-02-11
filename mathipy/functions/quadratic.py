from mathipy import calculus, polynomial, _complex 

class Quadratic(polynomial.Polynomial):
    function_type = 'Quadratic'
    def __init__(self, a = 1, **kwargs):
        self.__a = a
        self.degree = 2
        if 'b' in kwargs and 'c' in kwargs:
            b, c = kwargs['b'], kwargs['c']
            self.__b = b
            self.__c = c
            self.__x1, self.__x2 = self.__roots = Quadratic.find_roots(a = self.__a, b = self.__b, c = self.__c)
            self.__xv = - self.__b / (2 * self.__a)
            self.__yv = self.__a * (self.__xv ** 2) + self.__b * self.__xv + self.__c
        elif 'xv' in kwargs and 'yv' in kwargs:
            xv, yv = kwargs['xv'], kwargs['yv']
            self.__xv = xv
            self.__yv = yv
            self.__b = (-2 * self.__xv) * self.__a
            self.__c = ((self.__xv ** 2) * self.__a) + self.__yv
            self.__x1, self.__x2 = self.__roots = Quadratic.find_roots(a = self.__a, b = self.__b, c = self.__c)
        elif 'x1' in kwargs and 'x2' in kwargs:
            x1, x2 = kwargs['x1'], kwargs['x2']
            self.__x1, self.__x2 = x1, x2
            self.__b = -(self.__x1 + self.__x2) * self.__a
            self.__c = (self.__x1 * self.__x2) * self.__a
            self.__xv = - self.__b / (2 * self.__a)
            self.__yv = self.__a * (self.__xv ** 2) + self.__b * self.__xv + self.__c
            self.__roots = [self.__x1, self.__x2]
        else:
            raise ValueError('Expression type not admitted') 

        if self.__a == 0:
            raise ValueError('a term cannot be equal to 0')

        values = polynomial.Polynomial(self.__c, self.__b, self.__a).get_values()
        self.__algebraic_expression = self.alg_exp(values[::-1])

    def get_roots(self):
        return self.__roots

    def get_vertex(self):
        return self.__xv, self.__yv

    @staticmethod
    def find_roots(a, b, c):
        root_body = b**2 - (4 * a * c)
        if a == 0:
            raise ValueError('a term cannot be equal to 0')
    
        if root_body == 0:
            return -b/(2*a)
    
        elif root_body < 0:
            x1_real = x2_real = - b / (2 * a)
            x1_imag = np.sqrt(abs(root_body)) / (2 * a)
            x2_imag = - np.sqrt(abs(root_body)) / (2 * a)
            x1 = _complex.Complex(x1_real, x1_imag)
            x2 = _complex.Complex(x2_real, x2_imag)

        elif root_body > 0:
            x1 = (-b + np.sqrt(root_body)) / (2 * a)
            x2 = (-b - np.sqrt(root_body)) / (2 * a)

        return x1, x2

    def calculate_values(self, x):
        y = (self.__a * (x**2)) + (self.__b * x) + self.__c
        return y

    def plot_func(self, ax):
        vertex = self.__xv, self.__yv
        roots = self.__x1, self.__x2
        if not isinstance(roots[0], _complex.Complex):
            ax.scatter(roots, (0,0), c = calculus.Function.function_part['roots'])
        ax.scatter(*vertex, c = calculus.Function.function_part['vertex'])
        ax.scatter(0, self.__c, c = calculus.Function.function_part['y-intercept'])

    def __str__(self):
        return self.__algebraic_expression

    def vertex_expression(self):
        vertex_exp = f'{self.__a}'
        if self.__xv > 0:
            vertex_exp += f'(x - {self.__xv})^2'
        elif self.__xv < 0:
            vertex_exp += f'(x + {abs(self.__xv)})^2'
        else:
            vertex_exp += 'x^2'
    
        if self.__yv > 0:
            vertex_exp += f' + {self.__yv}'
        elif self.__yv < 0:
            vertex_exp += f' - {abs(self.__yv)}'
    
        return vertex_exp

    def factored_expression(self):
        factored_exp = f'{self.__a}'
        if self.__x1 == self.__x2:
            if self.__x1 > 0:
                factored_exp += f'(x - {self.__x1})^2'
            elif self.__x1 < 0:
                factored_exp += f'(x + {abs(self.__x1)})^2'
            else:
                factored_exp += 'x^2'
        else:
            if self.__x1 > 0:
                factored_exp += f'(x - {self.__x1})'
            elif self.__x1 < 0:
                factored_exp += f'(x + {abs(self.__x1)})'
            else:
                factored_exp += 'x'

            if self.__x2 > 0:
                factored_exp += f'(x - {self.__x2})'
            elif self.__x2 < 0:
                factored_exp += f'(x + {abs(self.__x2)})'
            else:
                factored_exp += 'x'

        return factored_exp