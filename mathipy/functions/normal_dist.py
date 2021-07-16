from mathipy.math import _math, calculus

class NormalDistribution(calculus.Function):
    function_type = 'Normal Distribution'

    def __init__(self, mu: float, sigma: float):
        self.mu = mu
        self.sigma = sigma

    def calculate_values(self, x) -> float:
        y = 1 / _math.sqrt(_math.tau * self.sigma)
        y *= _math.e ** (-((x - self.mu)**2) / (2 * self.sigma ** 2))
        return y

    def plot_func(self, ax) -> None:
        ax.scatter(0, self(0), color=calculus.Function.function_part['y-intercept'])
        ax.scatter(self.mu, self(self.mu), color=calculus.Function.function_part['vertex'])

    def __call__(self, x) -> float:
        return self.calculate_values(x)

    def __str__(self):
        return f'Normal Distribution(mu = {self.mu}, sigma = {self.sigma})'
