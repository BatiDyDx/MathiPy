import matplotlib.pyplot as plt
from mathipy import numeric_operations as ops

class Statistics(object):
    """
    Statistics object is used for calculating statistical
    operations on an iterable object.
    """
    def __init__(self, iterable: iter, *args: iter):
        self.iterable = iterable
        if args:
            #Join all args with self.iterable
            for arg in args:
                self.iterable.extend(arg)

    def mean(self) -> float:
        return ops.mean(self.iterable)

    def std(self) -> float:
        return ops.std(self.iterable)

    def median(self):
        return ops.median(self.iterable)

    def mode(self) -> list:
        return ops.mode(self.iterable)

    def max(self):
        return ops.max(self.iterable)

    def min(self):
        return ops.min(self.iterable)

    def probability_of(self, x) -> float:
        return ops.probability_of(self.iterable, x)

    def __call__(self, x):
        return self.probability_of(x)

    def create_ND(self):
        import mathipy.functions.normal_dist as nd   
        mean = self.mean()
        std = self.std()
        return nd.NormalDistribution(mu = mean, sigma = std)

    def plot(self, **kwargs):
        pos = kwargs.get('pos', self.mean())
        r = kwargs.get('range', 5)
        norm_dist = self.create_ND()
        norm_dist.plot(pos, r, **kwargs)

    def plot_hist(self, absolute = False, **kwargs):
        a = kwargs.get('alpha', 1)
        c = kwargs.get('color', None)
        h = kwargs.get('histtype', 'bar')
        d = False if not absolute else True
        g = kwargs.get('grid', False)
        plt.hist(self.iterable, density = d, histtype = h, alpha = a, facecolor = c)
        if g:
            plt.grid()
        plt.ylabel('$P(x)$')
        plt.xlabel('$x$')
        plt.show()

    def __str__(self):
        return f'Statistics({self.iterable})'

    def __repr__(self):
        return str(self)