import matplotlib.pyplot as plt
from mathipy import numeric_operations as ops
from mathipy.math import calculus

class BinomialDistribution(calculus.Function):
    function_type = 'Binomial Distribution'

    def __init__(self, n: int, p: float):
        self.n = n
        self.p = p
        if not 0 < p < 1:
            raise ValueError('The probability parameter, p, must be between 0 and 1')
    
    def calculate_values(self, x: int) -> float:
        c: int = ops.combinatorial(n=self.n, k=x)
        y: float = c * self.p ** x * (1 - self.p) ** (self.n - x)
        return y

    def __call__(self, x) -> float:
        return self.calculate_values(x)

    def plot(self, **kwargs) -> None:
        fig, ax = plt.subplots()
        c: str = kwargs.get('c', None)
        plt.xlabel('$x$')
        plt.ylabel('$P(x)$')
        for i in range(self.n):
            ax.scatter(i, self(i), c=c)
        plt.grid()
        plt.show()

    def __str__(self):
        return f'X ~ B({self.n}, {self.p})'
