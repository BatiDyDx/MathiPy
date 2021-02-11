import matplotlib.pyplot as plt
from mathipy import numeric_operations as ops

class Statistics(object):
    def __init__(self, iterable, *args):
        self.iterable = iterable
        if args:
            self.iterable.extend(args)

    def mean(self):
        return ops.mean(self.iterable)

    def std(self):
        return ops.std(self.iterable)

    def median(self):
        return ops.median(self.iterable)

    def mode(self):
        return ops.mode(self.iterable)

    def max(self):
        return ops.max(self.iterable)

    def min(self):
        return ops.min(self.iterable)

    def probability_of(self, x):
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
        norm_dist.plot(pos, r)

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

    def __repr__(self):
        return f'Statistics({self.iterable})'
