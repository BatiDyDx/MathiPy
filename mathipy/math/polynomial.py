import re
from typing import Callable, Union, TypeVar
import numpy as np
from mathipy import numeric_operations as ops
from mathipy.math import _math, calculus

# TODO define a generic type for coefficients of polynomials
# Coefficient = TypeVar['Coefficient', int, float, complex, Complex]

class Polynomial(calculus.Function):
    function_type: str = 'Polynomial'

    def __init__(self, *args, **kwargs):
        if args and kwargs:
            raise ValueError(
                """
                Arguments and keyboard arguments cannot be passed simultaneously,
                since its ambiguous for coefficients assignment. Only one of them must be used
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

    def __pair_degree_coefficients(pair_string_coef):
        """
        pair_string_coef is an argument of type list[list[str, Union[int, float, complex]]]
        __pair_degree_coefficients return is of type list[list[int, Union[int, float, complex]]],
        that returns a modified version of pair_string_coef, changing the string for an int

        f([['a10', 5], ['a3', 6], ['a0', -1]]) == [[10, 5], [3, 6], [0, -1]]
        """
        # f is a function that given a string with a format like 'aN',
        # where a is any letter and N is an integer, returns n as an int.
        # f('a10') == 10
        f: Callable[[str], int] = lambda s: int(re.findall('\d+$', s)[0])
        
        # pdc stands for pair degree-coefficient
        # pdc is a list of lists, where the ith element is a list
        # containing two elements, the first one being the degree,
        # and the second one the corresponding coefficient 
        pdc: list[list[int, Union[int, float, complex]]] = map(lambda pair: [f(pair[0]), pair[1]], pair_string_coef)
        
        # Sort pdc by the first components of their elements.
        # Practically, it sorts the list by the degrees of the polynomial
        pdc.sort(key=lambda a: a[0])
        return pdc

    def __complete_coefficents(self, kwargs: dict[str, Union[int, float, complex]]):
        pair_dc: list[list[int, Union[int, float, complex]]] = Polynomial.__pair_degree_coefficients(kwargs.items())
        
        # Get a list of all degrees
        degrees: list[int] = [a[0] for a in pair_dc] 
        
        # Limit is the biggest of degrees, since pair_dc is sorted
        limit: int = pair_dc[-1][0]
        
        # Iterate through all integers until the limit
        for i in range(limit):
            # If the degree is not in the list of degrees, it is added
            # to pair_dc, with a coefficient of 0
            if i not in degrees:
                pair_dc.insert(i, [i, 0])
        return pair_dc

    
    def __add__(p, q):
        """
        Method for adding self to a Polynomial instance q.
        """
        if ops.is_scalar(q):
            q = Polynomial(q)
        return Polynomial(*polynomial_addition(p, q))

    def __radd__(p, q):
        return q.__add__(p)

    def __sub__(p, q):
        """
        Method for substracting q from self.
        Equivalent to self + (- q)
        """
        return p + (-q)

    def __neg__(p):
        """
        Returns the opposite of self, equivalent to multiplying
        by the scalar -1
        """
        return p * -1

    def __mul__(p, q):
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

    def __rmul__(p, q):
        return p.__mul__(q)

    def __truediv__(p, q):
        """
        Returns an array with 2 elements, where the first one
        is the quotient polynomial and the second is the remainder
        polynomial of the division between p and q
        """
        raise NotImplementedError
        return polynomial_division(p, q)

    def __mod__(p, q):
        """
        Returns the remainder of the division between p and q.
        """
        raise NotImplementedError
        return polynomial_division(p, q)[1]

    def __bool__(self):
        return self.coefficients().any() is True

    def __eq__(p, q):
        if isinstance(q, bool):
            return bool(p) == q
        else:
            mx_d = max_degree(p, q)
            return np.array_equal(p.coefficients(mx_d), q.coefficients(mx_d))

    def __getitem__(self, index):
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

    def __setitem__(self, index, value):
        """
        Sets the ith coefficient of the polynomial to the value assigned
        """
        i = -(1 + index)
        self.values[i][1] = value

    def __delitem__(self, index):
        """
        Sets the ith coefficient of the polynomial to 0
        """
        i = -(1 + index)
        self.values[i][1] = 0

    def coefficients(self, length=-1):
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

    def __iter__(self):
        """
        Returns an iterable of the coefficients
        """
        return iter(self.coefficients())

    def __call__(self, x):
        """
        Evaluates the polynomial in the value x
        """
        return self.calculate_values(x)

    def calculate_values(self, x):
        """
        Takes a number and returns the poly evaluated at x
        """
        result = 0
        for degree, coef in self.values:
            result += coef * x ** degree 
        return result

    def find_roots(self):
        """
        Returns the values where p(x) = 0.
        """
        return np.roots(self.coefficients())

    def get_domain(self):
        """
        Returns a string with information about the coefficients of the
        polynomial. Mathematically, p ∈ A[x], where A is the domain of the coefficients
        
        Possible domains are:
        - Complex
        - Real
        - Integer
        - Natural
        """
        domain = 'Complex'
        for i in self.values:
            if isinstance(i[1], (complex)):
                break
        else:
            domain = 'Real'
            for i in self.values:
                if not float(i[1]).is_integer():
                    break
            else:
                domain = 'Integer'
                for i in self.values:
                    if i[1] < 0:
                        break
                else:
                    domain = 'Natural'
        return domain

    def plot_func(self, ax):
        y_intercept = self(0)
        ax.scatter(0, y_intercept, color= calculus.Function.function_part['y-intercept'])

    def __str__(self):
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

    def __repr__(self):
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
    return _math.maximum(p.degree, q.degree)
