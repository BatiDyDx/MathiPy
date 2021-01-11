from mathipy import calculus

class NormalDistribution(calculus.Function):
    function_type = 'Normal Distribution'
    def __init__(self, mu, sigma):
        self.mu = mu
        self.sigma = sigma

    def calculate_values(self, x):
        y = 1 / np.sqrt(2 * np.pi * self.sigma)
        y *= np.e ** (-((x - self.mu)**2) / (2 * self.sigma ** 2))
        return y

    def plot_func(self, ax):
        mu = self.mu
        ax.scatter(0, self(0), color = calculus.Function.function_part['y-intercept'])
        ax.scatter(mu, self(mu), color = calculus.Function.function_part['vertex'])

    def __call__(self, x):
        return self.calculate_values(x)

    def __repr__(self):
        return f'Normal Distribution(mu = {self.mu}, sigma = {self.sigma})'