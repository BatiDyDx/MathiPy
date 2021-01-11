from mathipy import calculus

class Linear(calculus.Function):
    function_type = 'Linear'
    def __init__(self, a = 1, b = 0):
        if a == 0:
            raise ValueError('a term cannot be equal to 0')
        else:
            self.__a = a
            self.__b = b
            self.__root = -self.__b / self.__a

    def get_yint(self):
        return self.__b

    def calculate_values(self, x):
        y = self.__a * x + self.__b
        return y
    
    def plot_func(self, ax):
        ax.scatter(0, self.__b, c = calculus.Function.function_part['y-intercept'])
        ax.scatter(self.__root, 0, c = calculus.Function.function_part['roots'])

    def __call__(self, x):
        y = self.calculate_values(x)
        return y

    def __repr__(self):
        representation = f'{self.__a}x'
        if self.__b > 0:
            representation += f' + {self.__b}'
        if self.__b < 0:
            representation += f' - {abs(self.__b)}'
        return representation