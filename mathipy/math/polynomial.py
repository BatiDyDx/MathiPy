import re
from enum import Enum, auto
from typing import AnyStr, Callable, Dict, Generic, Iterator, List, Tuple, Union, TypeVar
import numpy as np
from mathipy import numeric_operations as ops
from mathipy.math import calculus

class CoefficientInputError(Exception):
    def __init__(self, msg: AnyStr) -> None:
        self.message = msg
        super().__init__(msg)

class Domain(Enum):    
    """Enumerated class for domain constants"""

    def _generate_next_value_(name, start, count, last_values):
        return name[0] + name[1:].lower()
    
    NATURAL = auto()
    INTEGER = auto()
    REAL = auto()
    COMPLEX = auto()

# TODO
# Add a type variable for polynomial coefficients, and make Polynomial
# a generic class

Coefficient = TypeVar('Coefficient', int, float, complex)

class Polynomial(calculus.Function, Generic[Coefficient]):
    function_type: str = 'Polynomial'

    def __init__(self, *args: Coefficient, **kwargs: Coefficient):
        if args and kwargs:
            raise CoefficientInputError(
                """
                Arguments and keyboard arguments cannot be passed simultaneously as 
                coefficients for a Polynomial instance since its ambiguous at assignment time. 
                Only one of them must be passed.
                """
            )
        if args:
            # If coefficients are passed as arguments, they are taken in order
            # Polynomial(1, 3, -1) is equivalent to x^2 + 3x^1 - 1x^0
            values = list(enumerate(args[::-1]))[::-1]
        elif kwargs:
            # If coefficients are passed as keyboard arguments, the key,
            # a string of type 'aN', determines the degree of the coefficient
            # assigned to it
            # Polynomial(a10 = -3, a3 = 2, a0 = -2) is equivalent to
            # -3x^10 + 2x^3 - 2x^0
            values = self.__complete_coefficents(kwargs)[::-1]
        
        # If the leading coefficients are zeros, don't take them
        # into account
        # Polynomial(0, 0, 1, 3) is equivalent to 1x^1 + 3x^0,
        # and not to 0x^3 + 0x^2 + 1x^1 + 3x^0
        while values[0][1] == 0 and len(values) > 1:
            del values[0]

        self.values = values
        self.degree = len(values) - 1


    @staticmethod
    def __pair_degree_coefficients(pair_string_coef: Dict[str, Coefficient]) -> List[Tuple[int, Coefficient]]:
        """
        Returns a list of 2-tuples,  where the first element corresponds to the
        degree and the second one to the coefficient, changing the string for an int
        __pair_degree_coefficients({'a10': 5, 'a3': 6, 'a0': -1}) == [(10, 5), (3, 6), (0, -1)]
        """
        # f is a function that given a string with a format like 'aN',
        # where a is any letter and N is an integer, returns n as an int.
        # f('a10') == 10
        f: Callable[[str], int] = lambda s: int(re.findall('\d+$', s)[0])
        
        # pdc stands for pair degree-coefficient
        # pdc is a list of tuples, with every tuple 
        # containing two elements, the first one being the degree,
        # and the second one the corresponding coefficient 
        pdc: Iterator[Tuple[int, Coefficient]] = map(lambda key: (f(key), pair_string_coef[key]), pair_string_coef)
        pdc: List[Tuple[int, Coefficient]] = list(pdc)
        
        # Sort pdc by the first components of their elements.
        # Practically, it sorts the list by the degrees of the polynomial
        pdc.sort(key=lambda a: a[0])
        return pdc

    def __complete_coefficents(self, kw_coefs: Dict[str, Coefficient]) -> List[Tuple[int, Coefficient]]:
        pair_dc: List[Tuple[int, Coefficient]] = Polynomial.__pair_degree_coefficients(kw_coefs)
        
        # Get a list of all degrees
        degrees: List[int] = [a[0] for a in pair_dc] 
        
        # Limit is the biggest of degrees and the last in the degrees list, since pair_dc is sorted
        limit: int = degrees[-1]
        
        # Iterate through all integers until the limit
        for i in range(limit):
            # If the degree is not in the list of degrees, it is added
            # to pair_dc, with a coefficient of 0
            if i not in degrees:
                pair_dc.insert(i, [i, 0])
        return pair_dc

    def __add__(p, q: 'Polynomial') -> 'Polynomial':
        """
        Method for adding self to a Polynomial instance q.
        """
        return polynomial_addition(p, q)

    def __radd__(p, q: 'Polynomial') -> 'Polynomial':
        return q.__add__(p)

    def __iadd__(p, q: 'Polynomial') -> None:
        """
        Modifies the first polynomial to be equal to the sum of p and q,
        without having to create a new instance of the class.
        """
        poly_sum: Polynomial = polynomial_addition(p, q)
        p.values = poly_sum.values
        p.degree = poly_sum.degree

    def __sub__(p, q: 'Polynomial') -> 'Polynomial':
        """
        Method for substracting q from self.
        Equivalent to self + (- q)
        """
        return p + (-q)

    def __rsub__(p, q: 'Polynomial') -> 'Polynomial':
        pass

    def __isub__(p, q: 'Polynomial') -> None:
        p.__iadd__(-q)

    def __neg__(p) -> 'Polynomial':
        """
        Returns the opposite of self, equivalent to multiplying
        by the scalar -1
        """
        return p * -1

    def __mul__(p, q: Union[int, float, complex, 'Polynomial']) -> 'Polynomial':
        """
        Multiplies self by q.
        If q is a polynomial, it returns the polynomial product
        between them, if it's a scalar it returns the scalar product,
        else, tries calling q.__mul__(p)
        """
        if isinstance(q, Polynomial):
            return polynomial_product(p, q)
        elif ops.is_scalar(q):
            return scalar_product(p, q)
        else:
            return q.__mul__(p)

    def __rmul__(p, q: Union[int, float, complex, 'Polynomial']) -> 'Polynomial':
        return p.__mul__(q)

    def __imul__(p, q: Union[int, float, complex, 'Polynomial']) -> 'Polynomial':
        new_poly: Polynomial = polynomial_product(p, q)
        p.values = new_poly.values
        p.degree = new_poly.degree

    def __truediv__(p, q: Union[int, float, complex, 'Polynomial']) -> Tuple['Polynomial', 'Polynomial']:
        """
        Returns an array with 2 elements, where the first one
        is the quotient polynomial and the second is the remainder
        polynomial of the division between p and q
        """
        raise NotImplementedError
        return polynomial_division(p, q)

    def __mod__(p, q: 'Polynomial') -> 'Polynomial':
        """
        Returns the remainder of the division between p and q.
        """
        raise NotImplementedError
        return polynomial_division(p, q)[1]

    def __bool__(self) -> bool:
        return self.coefficients().any() is True

    def __eq__(p, q: Union[bool, 'Polynomial']):
        if isinstance(q, bool):
            return bool(p) is q
        else:
            mx_d = max_degree(p, q)
            return np.array_equal(p.coefficients(mx_d), q.coefficients(mx_d))

    def __getitem__(self, index: int) -> Coefficient:
        """
        Returns the ith coefficient of the polynomial.
        If i is greater than the coefficients degree, returns 0
        """
        try:
            i = -(1 + index)
            item = self.coefficients()[i]
        except IndexError:
            item = 0
        finally:
            return item

    def __setitem__(self, index: int, value: Coefficient) -> None:
        """
        Sets the ith coefficient of the polynomial to the value assigned
        """
        i = -(1 + index)
        self.values[i][1] = value

    def __delitem__(self, index: int) -> None:
        """
        Sets the ith coefficient of the polynomial to 0
        """
        i = -(1 + index)
        self.values[i][1] = 0

    def coefficients(self, length: int = -1) -> np.ndarray:
        """
        Returns an np.array of the coefficients
        If length is passed, and greater than the degree of the polynomial,
        it returns the array filled with zeros until the length needed. If
        length argument is less than the polynomial degree, it raises a ValueError
        """
        coefs = [x[1] for x in self.values]
        if length > -1:
            if length < len(coefs): raise ValueError('length argument cannot be smaller than polynomial degree')
            while len(coefs) < length:
                coefs.insert(0, 0)
        return np.array(coefs)

    def __iter__(self) -> Iterator:
        """
        Returns an iterable of the coefficients
        """
        return iter(self.coefficients())

    def __call__(self, x: Union[int, float, complex]) -> Union[int, float, complex]:
        """
        Evaluates the polynomial in the value x
        """
        return self.calculate_values(x)

    def calculate_values(self, x: Union[int, float, complex]) -> Union[int, float, complex]:
        """
        Takes a number and returns the poly evaluated at x
        """
        result = 0
        for degree, coef in self.values:
            result += coef * x ** degree 
        return result

    def find_roots(self) -> np.ndarray:
        """
        Returns the values where p(x) = 0.
        """
        return np.roots(self.coefficients())

    def get_domain(self) -> Domain:
        """
        Returns a Domain class instance with information about the coefficients of the
        polynomial. Mathematically, p ∈ A[x], where A is the domain of the coefficients
        
        Possible domains are:
        - Domain.Natural
        - Domain.Integer
        - Domain.Real
        - Domain.Complex
        """
        domain = Domain.COMPLEX
        for i in self.values:
            if isinstance(i[1], complex):
                break
        else:
            domain = Domain.REAL
            for i in self.values:
                if not float(i[1]).is_integer():
                    break
            else:
                domain = Domain.INTEGER
                for i in self.values:
                    if i[1] < 0:
                        break
                else:
                    domain = Domain.NATURAL
        return domain

    def plot_func(self, ax) -> None:
        y_intercept = self(0)
        ax.scatter(0, y_intercept, color = calculus.Function.function_part['y-intercept'])

    def __str__(self) -> str:
        expression = []
        #TODO algebraic expression
        for degree, coef in self.values:
            if coef != 0 or degree == 0:
                if degree != 0:
                    s = f'{coef}x^{degree}'
                else:
                    s = str(coef)
                expression.append(s)
        expression = ' + '.join(expression)
        return expression

    def __repr__(self) -> str:
        return str(self.coefficients())

def polynomial_addition(p: Polynomial, q: Polynomial) -> Polynomial:
    """
    Adds two polynomials, adding the corresponding coefficients according
    to their degree.
    Mathematically, degree(p + q) <= max(degree(p), degreee(q))
    """
    mx_d = max_degree(p, q)
    coefs_p = p.coefficients(mx_d)
    coefs_q = q.coefficients(mx_d)
    return Polynomial(*(coefs_p + coefs_q))

def polynomial_product(p: Polynomial, q: Polynomial) -> Polynomial:
    """
    Returns the product between two polynomials.
    degree(p * q) = degree(p) + degree(q)
    """
    r = [0] * (p.degree + q.degree + 1)
    for p_exp, p_coef in p.values:
        for q_exp, q_coef in q.values:
            exp = p_exp + q_exp
            coef = p_coef * q_coef
            r[exp] += coef
    return Polynomial(*r[::-1])

def scalar_product(p: Polynomial, n: int) -> Polynomial:
    """
    Multiplies a polynomial by a scalar. Equivalent to multiplying all
    coefficients of p by the scalar
    """
    return Polynomial(*(p.coefficients() * n))

"""
def polynomial_division(p: Polynomial, q: Polynomial) -> tuple[Polynomial, Polynomial]:
    #TODO
    assert p.degree >= q.degree

    c = []
    r = p.coefficients()
    q_coefs = q.coefficients()

    for i in range(p.degree - q.degree + 1):
        if q_coefs[i] == 0:
            c.append(r[0] / q_coefs[i])
    	    r = [r[j] - (c[i] * q_coefs[j]) for j in range(1, q.degree + 1)]
        
    return (c, r)
"""

def max_degree(p: Polynomial, q: Polynomial) -> int:
    """
    Returns the max degree between two instances of Polynomial
    """
    return max(p.degree, q.degree)
