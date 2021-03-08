import re
import numpy as np
from mathipy import calculus
from mathipy import numeric_operations as ops

class Polynomial(calculus.Function):
    function_type = 'Polynomial'
    def __init__(self, *args, **kwargs):
        if args:
            values = list(enumerate(args[::-1]))[::-1]
        elif kwargs:
            values = self.__process_coefficents(kwargs)
        while values[0][1] == 0 and len(values) > 1:
            del values[0]

        self.values = ops.round_int(values)
        self.degree = len(values) - 1

    def __process_coefficents(self, kwargs):
        f = lambda degree: int(re.findall('\d+$', degree)[0])
        listed_coefficients = [[f(degree), coef] for degree, coef in kwargs.items()]
        listed_coefficients.sort(key = lambda a: a[0], reverse=True)
        listed_coefficients = Polynomial.__complete_coefficients(listed_coefficients)
        return listed_coefficients

    @staticmethod
    def __complete_coefficients(listed_coefficients):
        exponents = [n[0] for n in listed_coefficients]
        limit = listed_coefficients[0][0]
        for i in range(limit):
            if i not in exponents:
                listed_coefficients.insert(i, [i, 0])
        return listed_coefficients

    def __add__(q, p):
        if ops.is_scalar(p):
            p = Polynomial(p)
        return Polynomial(*polynomial_addition(p, q))

    def __radd__(p, q):
        return q.__add__(p)

    def __sub__(p, q):
        return p + (-q)

    def __neg__(p):
        return p * -1

    def __mul__(p, q):
        if isinstance(q, Polynomial):
            return polynomial_product(p, q)
        elif ops.is_scalar(q):
            return scalar_product(p, q)
        else:
            return q.__mul__(p)

    def __rmul__(p, q):
        return p.__mul__(q)

    def __truediv__(p, q):
        pass

    def __floordiv__(p, q):
        pass

    def __mod__(p, q):
        pass

    def __bool__(self):
        return self.coefficients().any() == True

    def __eq__(p, q):
        if isinstance(q, bool):
            return bool(p) == q
        else:
            mx_d = max_degree(p, q)
            return np.array_equal(p.coefficients(mx_d), q.coefficients(mx_d))

    def __getitem__(self, index):
        try:
            i = -(1 + index)
            item = self.coefficients()[i]
        except IndexError:
            item = 0
        finally:
            return item

    def __setitem__(self, index, value):
        i = -(1 + index)
        self.values[i][1] = value

    def __delitem__(self, index):
        i = -(1 + index)
        self.values[i][1] = 0

    def __len__(self):
        return self.degree + 1

    def coefficients(self, length=-1):
        coefs = [x[1] for x in self.values]
        if length > -1:
            if length < len(coefs): raise ValueError('length argument cannot be smaller than polynomial degree')
            while len(coefs) < length:
                coefs.insert(0, 0)
        return np.array([coefs])

    def __iter__(self):
        return iter(self.coefficients())

    def __call__(self, x):
        return self.calculate_values(x)

    def calculate_values(self, x):
        result = 0
        for degree, coef in self.values:
            result += coef * x ** degree 
        return result

    def find_roots(self):
        return np.roots(self.coefficients())

    def get_domain(self):
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
            if coef != 0:
                if degree != 0:
                    s = f'{coef}x^{degree}'
                else:
                    s = str(coef)
                expression.append(s)
        expression = ' + '.join(expression)
        return expression

    def __repr__(self):
        return str(self.coefficients()[0])

def polynomial_addition(p: Polynomial, q: Polynomial) -> Polynomial:
        mx_d = max_degree(p, q)
        coefs_p = p.coefficients(mx_d)
        coefs_q = q.coefficients(mx_d)
        return Polynomial(*(coefs_p + coefs_q))

def polynomial_product(p: Polynomial, q: Polynomial) -> Polynomial:
        r = [0] * (p.degree + q.degree + 1)
        for p_exp, p_coef in p.values:
            for q_exp, q_coef in q.values:
                exp = p_exp + q_exp
                coef = p_coef * q_coef
                r[exp] += coef
        return Polynomial(*r[::-1])

def scalar_product(p: Polynomial, n: int) -> Polynomial:
    return Polynomial(*(p.coefficients() * n))

def polynomial_division():
    pass

def max_degree(p: Polynomial, q: Polynomial) -> int:
    return ops.max([len(p), len(q)])