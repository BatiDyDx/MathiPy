import math
from typing import Any, Callable, Dict, List, Sequence, Union, TypeVar, Generic, Optional
from mathipy.math import ntheory
import matplotlib.pyplot as plt

DataValue = TypeVar('DataValue')

class Statistics(Generic[DataValue]):
    """
    Statistics object is used for calculating statistical
    operations on an iterable object.
    """
    iterable: List[DataValue]

    def __init__(self, *args: Sequence[DataValue]):
        iterable: list = []
        for arg in args:
            # Join all iterabels in args to a single list
            iterable.extend(list(arg))
        self.iterable: List[DataValue] = iterable

    def mean(self) -> float:
        """
        Return the mean of self.iterable
        """
        return mean(self.iterable)

    def std(self) -> float:
        """
        Return the standard deviation of self.iterable
        """
        return std(self.iterable)

    def median(self) -> DataValue:
        """
        Return the median of self.iterable
        """
        return median(self.iterable)

    def mode(self) -> List[DataValue]:
        """
        Return the mode of self.iterable
        """
        return mode(self.iterable)

    def max(self) -> DataValue:
        """
        Return the maximum of self.iterable
        """
        return max(self.iterable)

    def min(self) -> DataValue:
        """
        Return the minimum of self.iterable
        """
        return min(self.iterable)

    def frequency(self, x: DataValue, f_type: str) -> Union[int, float]:
        """
        Return the frequency of a number is self.iterable
        f_type can be 'relative' or 'absolute'.
        Relative frequency is the quotient between the amount of
        ocurrences of x in the list over the number of elements
        Absolute frequency is just the number of ocurrences of x in the list
        """
        return frequency(self.iterable, x, f_type)

    def create_ND(self): #-> 'mathipy.functions.normal_dist.NormalDistribution':
        """
        Creates a NormalDistribution object, where mu and sigma are
        obtained from the std and mean of self.iterable
        """
        import mathipy.functions.normal_dist

        mean: float = self.mean()
        std: float = self.std()
        return mathipy.functions.normal_dist.NormalDistribution(mu=mean, sigma=std)
    
    def plot(self, pos: Optional[int] = None, **kwargs: Any) -> None:
        """
        Plots the NormalDistribution Function obtained
        from self.iterable
        """
        pos = pos if pos is not None else int(self.mean())
        r = kwargs.get('range', 5)
        norm_dist = self.create_ND()
        norm_dist.plot(pos, r, **kwargs)

    def plot_hist(self, **kwargs: Any) -> None:
        """
        Plot the histogram corresponding to self.iterable
        kwargs are passed to matplotlib.pyplot.hist
        """
        plt.hist(self.iterable, **kwargs)
        if kwargs.get('grid', False):
            plt.grid()
        plt.ylabel('$P(x)$')
        plt.xlabel('$x$')
        plt.show()

    def __str__(self) -> str:
        return f'Statistics({self.iterable})'

    def __repr__(self) -> str:
        return str(self)


Number = Union[int, float]

def min(args: Sequence[Number]) -> Number:
    """
    Return the minimum value of a series of iterable objects.
    """
    min_n = float('inf')
    for i in args:
        if i is None:
            continue
        elif i < min_n:
            min_n = i
    return min_n


def max(args: Sequence[Number]) -> Number:
    max_n = float('-inf')
    for i in args:
        if i is None:
            pass
        elif i > max_n:
            max_n = i
    return max_n


def mean(args: Sequence[Number]) -> float:
    """
    Return the mean of a series of iterable objects
    """
    return sum(args) / len(args)


def median(args: Sequence[Number]) -> Number:
    args.sort()
    n: int = len(args)
    if n % 2 == 1:
        return args[n // 2]
    else:
        x_1, x_2 = args[(n // 2) - 1], args[n // 2]
        return (x_1 + x_2) / 2 


def mode(args: Sequence[Number]) -> List[Number]:
    items: Dict[Number, int] = {item: args.count(item) for item in set(args)}
    mx_repetitions = max(items.values())
    modes: List[Number] = [k for k in items.keys() if items[k] == mx_repetitions]
    return modes


def frequency(args: Sequence[Number], x: Number, f_type: str = 'absolute') -> Union[int, float]:
    count = args.count(x)
    if f_type == 'absolute':
        return count
    elif f_type == 'relative':
        return count / len(args)


def std(args: Sequence[Number]) -> Number:
    n: int = len(args)
    m: float = mean(args)
    x_1: float = 1. / n
    f: Callable[[int], float] = (lambda x: (args[x] - m) ** 2)
    x_2: float = ntheory.summation(f, up_bound = n - 1, low_bound = 0)
    return math.sqrt(x_1 * x_2)
