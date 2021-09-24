from typing import List, Tuple


def generate_permutations(n: int) -> List[Tuple[int]]:
    """
    Generate list of posible permutations of the first
    n natural numbers
    
    >>> generate_permutations(1)
    [(1,)]
    >>> generate_permutations(3)
    [(1,2,3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)]
    """
    pass


def reduce_permutation(perm: Tuple[int], j: int) -> Tuple[int]:
    check_valid_perm(perm)
    j = perm[0] # The element that perm maps 1 to
    rperm = [] # Reduced permutation
    for i in range(1, len(perm)):
        sig_i = perm[i] # Sigma(i)
        if sig_i < j:
            rperm.append(sig_i)
        elif sig_i > j:
            rperm.append(sig_i - 1)
    return tuple(rperm)


def natural_interval(m: int, n: int) -> List[int]:
    return list(range(m, n + 1))


def check_valid_perm(perm: Tuple[int]) -> None:
    # Check if all elements are naturals (from 1 to n)
    # Check if there are skipped elements
    # Check that there are no repeated elements
    n: int = len(perm)
    interval = natural_interval(1, n)
    for i in perm:
        if not isinstance(i, int):
            raise TypeError("Elements of the permutation must be all integers")
        if not (1 <= i <= n):
            raise ValueError("Elements of the permutation must range from 1 to n")
        if perm.count(i) > 1:
            raise ValueError("Elements of the permutation can not be repeated")

    return

def transposition(perm: Tuple[int], i: int, j: int) -> Tuple[int]:
    check_valid_perm(perm)
    if not (i in perm and j in perm):
        raise ValueError("i and j must be in the partition")

    index_i, index_j = perm.index(i), perm.index(j)
    temp = list(perm)
    temp[index_i] = j
    temp[index_j] = i
    return tuple(temp)


def transposition_dec(i: int, j: int, sgm: Callable) -> Callable:
    if i == j:
        raise ValueError("i and j must be different")

    def transposition_wrapper(k: int):
        k_p = sgm(k)
        if k_p == i:
            return j
        elif k_p == j:
            return i
        else:
            return k_p

    return transposition_wrapper
