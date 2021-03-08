from functools import wraps

def round_int(n: any, thresh_exp: int= 3) -> any:
    floor_thresh = 1 * (10 ** -thresh_exp)
    ceil_thresh = 1 - floor_thresh
    if isinstance(n, complex):
        t = type(n)
        return t(round_int(n.real, thresh_exp), round_int(n.imag, thresh_exp))
    elif is_iter(n):
        return list(map(lambda n: round_int(n, thresh_exp), n))
    if n >= 0:
        if n % 1 >= ceil_thresh or n % 1 <= floor_thresh:
            return int(round(n))
        else: return n
    elif n < 0:
        return -round_int(-n)

def is_iter(it: any, exclude= None) -> bool:
    if hasattr(it, '__iter__'):
        if exclude:
            if isinstance(it, exclude):
                return False
            else: return True
        else: return True
    else: return False

def is_scalar(a: any) -> bool:
    return isinstance(a, (int, float, complex))

from mathipy import _math
def variation(n: int, k: int, repetitions: bool= False) -> int:
    if not k <= n: raise ValueError('k must be less than n')
    if repetitions:
        return n ** k
    else:
        return _math.factorial(n) // _math.factorial(n - k)

def permutation(n: int, k: (int, None)= None, circular: bool= False) -> int:
    if not k:
        if not circular: return _math.factorial(n) 
        else: return _math.factorial(n - 1)
    else:
        denominator = 1
        for el in range(k):
            denominator *= _math.factorial(el)
        return _math.factorial(n) // denominator

def combinatorial(n: int, k: int, repetitions: bool= False) -> int:
    if not repetitions:
        if k >= n: raise ValueError('n must be greater than p')
        num = _math.factorial(n)
        den = _math.factorial(k) * _math.factorial(n - k)
        return num // den
    else:
        return combinatorial(n + k - 1, k, repetitions= False)

def configIter(f: callable) -> callable:
    @wraps(f)
    def iterWrapper(*args, **kwargs) -> any:
        args = [list(arg) for arg in args]
        iterable = list(sum(args, []))
        return f(iterable, **kwargs)
    return iterWrapper

@configIter
def min(args) -> any:
    """
    Return the minimum value of a series of iterable objects
    """
    min_n = float('inf')
    for i in args:
        if i == None: pass
        elif i < min_n: min_n = i
    return min_n

@configIter
def max(args) -> any:
    max_n = float('-inf')
    for i in args:
        if i == None: pass
        elif i > max_n: max_n = i
    return max_n

@configIter
def mean(args) -> float:
    """
    Return the mean of a series of iterable objects
    """
    return sum(args) / len(args)

@configIter
def median(args):
    args.sort()
    n = len(args)
    if n % 2 == 1:
        return args[n // 2]
    else:
        x_1, x_2 = args[(n // 2) - 1], args[n // 2]
        return (x_1 + x_2) / 2 

@configIter
def mode(args) -> list:
    items = {item: args.count(item) for item in set(args)}
    mx_repetitions = max(items.values())
    modes = [k for k in items.keys() if items[k] == mx_repetitions]
    return modes

@configIter
def probability_of(args, x) -> float:
    count = args.count(x)
    return count / len(args)

@configIter
def std(args) -> float:
    n = len(iterable)
    m = mean(iterable)
    x_1 = 1 / n
    f = (lambda x: (iterable[x] - m) ** 2)
    x_2 = _math.summation(f, up_bound = n - 1, low_bound = 0)
    std = _math.sqrt(x_1 * x_2)
    return std