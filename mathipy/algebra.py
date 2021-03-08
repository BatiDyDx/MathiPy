from functools import wraps

def setConfig(f: callable) -> callable:
    @wraps(f)
    def setWrapper(A: iter, B: iter) -> iter:
        itype = kwargs.get('itype', list)
        A, B = list(A), list(B)
        C = f(A, B, **kwargs)
        return itype(C)
    return setWrapper

@setConfig
def setUnion(A: iter, B: iter) -> iter:
    A.extend(B)
    return set(A)

@setConfig
def setIntersection(A: iter, B: iter) -> iter:
    return [x for x in A + B if x in A and x in B]

@setConfig
def setSub(A: iter, B: iter) -> iter:
    return [x for x in A + B if x not in B]

def setIsContained(A: iter, B: iter, eq: bool= True) -> bool:
    for a in A:
        if a in B:
            continue
        else: return False
    else:
        return True if eq else set(A) != set(B)

def setContains(A: iter, B: iter, eq: bool= True) -> bool:
    return setIsContained(B, A, eq)

def ruffini(x):
    pass