import matplotlib.pyplot as plt
from mathipy import calculus, numeric_operations as ops

class BinomialDistribution(calculus.Function):
    function_type = 'Binomial Distribution'
    def __init__(self, n, p):
        self.n = n
        self.p = p
        if not 0 <= p <= 1:
            raise ValueError('The probability parameter, p, must be between 0 and 1')
    
    def calculate_values(self, x):
        c = ops.combinatorial(n = self.n, k = x)
        y = c * self.p ** (x) * (1 - self.p) ** (self.n - x)
        return y

    def __call__(self, x):
        return self.calculate_values(x)

    def plot(self, **kwargs):
        fig, ax = plt.subplots()
        c = kwargs.get('c', None)
        plt.xlabel('$x$')
        plt.ylabel('$P(x)$')
        for i in range(1, self.n):
            ax.scatter(i, self(i), c = c)
        plt.show()

    def __repr__(self):
        return f'X ~ B({self.n}, {self.p})'