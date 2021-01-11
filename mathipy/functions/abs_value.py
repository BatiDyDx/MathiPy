from mathipy import calculus, _math

class AbsoluteValue(calculus.Function):
    function_type = 'Absolute Value'
    def __init__(self, a, b = 0, h = 0):
        if a == 0:
            raise ValueError('a term cannot be equal to 0')
        else:
            self.__a = a
            self.__b = b
            self.__h = h
            self.__x1, self.__x2 = self.__roots = self.find_roots()

    def get_yint(self):
        return self.y_intercept

    def find_roots(self):
        delta = (-self.__b / self.__a)
        if delta < 0:
            x1 = x2 = None
        else:
            x1 =   delta + self.__h
            x2 = - delta + self.__h
        return x1, x2

    def calculate_values(x):
        y = self.a * _math.abs(x - self.h) + self.b
        return y

    def plot_func(self, ax):
        y_intercept = self(0)
        ax.scatter(0, y_intercept, c = calculus.Function.function_part['y-intercept'])
        if self.__x1 != None and self.__x2 != None:
            ax.scatter(self.__roots, (0,0), c = calculus.Function.function_part['roots'])
        ax.scatter(self.__h, self.__b, c = calculus.Function.function_part['vertex'])

    def __call__(self, x):
        y = self.calculate_values(x)
        return y

    def __repr__(self):
        representation = ''
        if self.__a != 1:
            representation += str(self.__a)
        if self.__h > 0:
            representation += f'|x - {self.__h}|'
        elif self.__h < 0:
            representation += f'|x + {_math.abs(self.__h)}|'
        else:
            representation += f'|x|'
        if self.__b < 0:
            representation += f' - {_math.abs(self.__b)}'
        elif self.__b > 0:
            representation += f' + {self.__b}'
        return representation