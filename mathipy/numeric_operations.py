def round_int(n, thresh_exp = 3):
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

def is_iter(it, exclude = None) -> bool:
    if hasattr(it, '__iter__'):
        if exclude:
            if isinstance(it, exclude):
                return False
            else: return True
        else: return True
    else: return False

def is_scalar(a):
    return isinstance(a, (int, float, complex))

from mathipy import _math 
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

def min(iterable):
    min_n = float('inf')
    for i in iterable:
        if i == None: pass
        elif i < min_n: min_n = i
    return min_n

def max(iterable):
    max_n = float('-inf')
    for i in iterable:
        if i == None: pass
        elif i > max_n: max_n = i
    return max_n

def mean(iterable):
    return sum(iterable) / len(iterable)

def median(iterable):
    iterable.sort()
    n = len(iterable)
    if n % 2 == 1:
        return iterable[n // 2]
    else:
        x_1, x_2 = iterable[(n // 2) - 1], iterable[n // 2]
        return (x_1 + x_2) / 2 

def mode(self):
        items = {item: 0 for item in set(iterable)}
        for i in iterable:
            items[i] += 1
        mx_repetitions = max(items.values())
        modes = [r for r in items.keys() if items[r] == mx_repetitions]
        return modes

def probability_of(iterable, x):
    count = 0
    for i in iterable:
        if i == x:
            count += 1
    return count / len(iterable)

def std(iterable):
    n = len(iterable)
    m = mean(iterable)
    x_1 = 1 / n
    f = (lambda x: (iterable[x] - m) ** 2)
    x_2 = _math.summation(f, up_bound = n - 1, low_bound = 0)
    std = _math.sqrt(x_1 * x_2)
    return std