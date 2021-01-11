from mathipy.functions import normal_dist as nd   
import matplotlib.pyplot as plt
from mathipy import _math
from mathipy import arithmetic as artc 

def variation(n, k, repetitions = False):
    if not k <= n: raise ValueError('k must be less than n')
    if repetitions:
        return n ** k
    else:
        return _math.factorial(n) // _math.factorial(n - k)

def permutation(n, k = None, circular = False):
    if not k:
        if not circular: return _math.factorial(n) 
        else: return _math.factorial(n - 1)
    else:
        denominator = 1
        for el in k:
            denominator *= _math.factorial(el)
        return _math.factorial(n) // denominator

def combinatorial(n, k, repetitions = False):
    if not repetitions:
        if k >= n: raise ValueError('n must be greater than p')
        num = _math.factorial(n)
        den = _math.factorial(k) * _math.factorial(n - k)
        return num // den
    else:
        return combinatorial(n + k - 1, k, repetitions=False)

class Statistics(object):
    def __init__(self, iterable, *args):
        self.iterable = iterable
        if args:
            self.iterable.extend(args)

    def mean(self):
        return sum(self.iterable) / len(self.iterable)

    def std(self):
        n = len(self.iterable)
        mean = self.mean()
        x_1 = 1 / n
        arg = artc.Power(artc.Minus(artc.Variable('x'), artc.Constant(mean)), artc.Constant(2))
        x_2 = _math.summation(arg, upper_bound = n, lower_bound = 0, iterable = self.iterable)
        s = np.sqrt(x_1 * x_2)
        return s

    def median(self):
        iterable = self.iterable
        iterable.sort()
        n = len(iterable)
        if n % 2 == 1:
            return iterable[int(n / 2)]
        else:
            x_1, x_2 = iterable[n/2 - 1], iterable[n/2]
            return (x_1 + x_2) / 2 

    def mode(self):
        items = {item: 0 for item in set(self.iterable)}
        for i in self.iterable:
            items[i] += 1
        mx_repetitions = Statistics(list(items.values())).max()
        modes = [r for r in items.keys() if items[r] == mx_repetitions]
        return modes

    def max(self):
        max_n = float('-inf')
        for i in self.iterable:
            if i == None: pass
            elif i > max_n: max_n = i
        return max_n

    def min(self):
        min_n = float('inf')
        for i in self.iterable:
            if i == None: pass
            elif i < min_n: min_n = i
        return min_n

    def probability(self, value):
        count = 0
        for i in self.iterable:
            if i == value:
                count += 1
        return count / len(self.iterable)

    def __call__(self, x):
        return self.probability(x)

    def create_ND(self):
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
