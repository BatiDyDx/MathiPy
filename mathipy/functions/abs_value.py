from mathipy import calculus, _math

class AbsoluteValue(calculus.Function):
    function_type = 'Absolute Value'
    def __init__(self, a, b = 0, h = 0):
        if a == 0:
            raise ValueError('a term cannot be equal to 0')
        else:
            self.a = a
            self.b = b
            self.h = h
            self.x1, self.x2 = self.roots = self.find_roots()

    def get_yint(self):
        return self(0)

    def find_roots(self):
        delta = (-self.b / self.a)
        if delta < 0:
            x1 = x2 = None
        else:
            x1 =   delta + self.h
            x2 = - delta + self.h
        return x1, x2

    def calculate_values(self, x):
        y = self.a * _math.abs(x - self.h) + self.b
        return y

    def plot_func(self, ax):
        y_int = self.get_yint()
        ax.scatter(0, y_int, color= calculus.Function.function_part['y-intercept'])
        x1, x2 = self.find_roots()
        if x1 != None and x2 != None:
            ax.scatter((x1, x2), (0,0), color= calculus.Function.function_part['roots'])
        ax.scatter(self.h, self.b, color= calculus.Function.function_part['vertex'])

    def __call__(self, x):
        return self.calculate_values(x)

    def __str__(self):
        representation = ''
        if self.a != 1:
            representation += str(self.a)
        if self.h > 0:
            representation += f'|x - {self.h}|'
        elif self.h < 0:
            representation += f'|x + {abs(self.h)}|'
        else:
            representation += f'|x|'
        if self.b < 0:
            representation += f' - {abs(self.b)}'
        elif self.b > 0:
            representation += f' + {self.b}'
        return representation

    def __repr__(self):
        return 'Absolute Value Function'