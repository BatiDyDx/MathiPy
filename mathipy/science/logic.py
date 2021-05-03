from typing import Iterable, Union, Callable

def imply(p: bool, q: bool) -> bool:
    return (not p) or q

def biconditional(p: bool, q: bool) -> bool:
    return p is q

def xor(p: bool, q: bool) -> bool:
    return x is not q

def set_is_contained(iter1: Iterable[Union[int, float]], iter2: Iterable[Union[int, float]], eq: bool = True) -> bool:
    s1 = set(iter1)
    s2 = set(iter2)
    
    truth = s1 & s2 == s1 and (s1 - s2 == set())
    if eq:
        return truth
    else:
        return truth and s1 != s2


def set_contains(iter1: Iterable[Union[int, float]], iter2: Iterable[Union[int, float]], eq: bool = True) -> bool:
    return set_is_contained(iter2, iter1, eq)


def test_proposition(P: Callable[[bool], bool], n: int):
    k = 2 ** n
    values: list[bool] = [False for _ in range(n)]
    #TODO
    pass
