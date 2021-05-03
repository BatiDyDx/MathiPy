from mathipy import calculus


class Linear(calculus.Function):
    function_type = 'Linear'

    def __init__(self, a: float = 1, b: float = 0):
        if a == 0:
            raise ValueError('a term cannot be equal to 0')
        else:
            self.a = a
            self.b = b

    def get_yint(self) -> float:
        return self.b

    def find_roots(self) -> float:
        return -self.b / self.a

    def calculate_values(self, x) -> float:
        y = self.a * x + self.b
        return y
    
    def plot_func(self, ax) -> None:
        ax.scatter(0, self.b, c=calculus.Function.function_part['y-intercept'])
        ax.scatter(self.find_roots(), 0, c=calculus.Function.function_part['roots'])

    def __call__(self, x) -> float:
        y = self.calculate_values(x)
        return y

    def __str__(self):
        representation = f'{self.a}x'
        if self.b > 0:
            representation += f' + {self.b}'
        if self.b < 0:
            representation += f' - {-self.b}'
        return representation
