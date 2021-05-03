import matplotlib.pyplot as plt
from mathipy import numeric_operations as ops
from typing import Iterable, Union, TypeVar, Generic, NoReturn, Optional

NormalDistribution = TypeVar('NormalDistribution')

class Statistics:
    """
    Statistics object is used for calculating statistical
    operations on an iterable object.
    """
    def __init__(self, *args: tuple[Iterable[Union[int, float]], ...]):
        iterable: list = []
        for arg in args:
            iterable.extend(list(arg))
        self.iterable: list[Union[int, float]] = iterable

    def mean(self) -> float:
        return ops.mean(self.iterable)

    def std(self) -> float:
        return ops.std(self.iterable)

    def median(self) -> Union[int, float]:
        return ops.median(self.iterable)

    def mode(self) -> list[Union[int, float]]:
        return ops.mode(self.iterable)

    def max(self) -> Union[int, float]:
        return ops.max(self.iterable)

    def min(self) -> Union[int, float]:
        return ops.min(self.iterable)

    def frequency(self, x, f_type) -> float:
        return ops.frequency(self.iterable, x, f_type)

    def __call__(self, x):
        return self.frequency(x, f_type='relative')

    def create_ND(self) -> Generic[NormalDistribution]:
        import mathipy.functions.normal_dist as nd   
        mean = self.mean()
        std = self.std()
        return nd.NormalDistribution(mu=mean, sigma=std)

    def plot(self, **kwargs) -> NoReturn:
        pos = kwargs.get('pos', self.mean())
        r = kwargs.get('range', 5)
        norm_dist = self.create_ND()
        norm_dist.plot(pos, r, **kwargs)

    def plot_hist(self, absolute = False, **kwargs) -> NoReturn:
        a: float = kwargs.get('alpha', 1.0)
        c: Optional[str] = kwargs.get('color', None)
        h: str = kwargs.get('histtype', 'bar')
        plt.hist(self.iterable, density=absolute, histtype=h, alpha=a, facecolor=c)
        if kwargs.get('grid', False):
            plt.grid()
        plt.ylabel('$P(x)$')
        plt.xlabel('$x$')
        plt.show()

    def __str__(self):
        return f'Statistics({self.iterable})'

    def __repr__(self):
        return str(self)