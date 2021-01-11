import re
from mathipy import calculus
from mathipy._complex import Complex
from mathipy import _math

class Polynomial(calculus.Function):
    function_type = 'Polynomial'
    def __init__(self, *args, **kwargs):
        if args:
            values = [[degree, coef] for degree, coef in enumerate(args)]
        elif kwargs:
            values = self.__process_coefficents(kwargs)
        while values[-1][1] == 0:
            del values[-1]

        domain = 'Complex'
        for i in values:
            if isinstance(i[1], (complex, Complex)):
                break
        else:
            domain = 'Real'
            for i in values:
                if not float(i[1]).is_integer():
                    break
            else:
                domain = 'Integer'
                for i in values:
                    if i[1] < 0:
                        break
                else:
                    domain = 'Natural'

        self.__domain = domain
        self.__values = values
        self.degree = len(values) - 1
        self.__algebraic_expression = self.alg_exp(self.__values[::-1])

    def __process_coefficents(self, kwargs):
        f = lambda degree: int(re.findall('\d+$', degree)[0])
        listed_coefficients = [[f(degree), coef] for degree, coef in kwargs.items()]
        listed_coefficients.sort(key = lambda a: a[0])
        listed_coefficients = Polynomial.__complete_coefficients(listed_coefficients)
        return listed_coefficients

    @staticmethod
    def __complete_coefficients(listed_coefficients):
        exponents = [n[0] for n in listed_coefficients]
        limit = listed_coefficients[-1][0]
        for i in range(limit):
            if i not in exponents:
                listed_coefficients.insert(i, [i, 0])
        return listed_coefficients

    def __add__(q, p):
        poly1 = q.coefficients()
        poly2 = p.coefficients()
        coef_tuple = list(zip(poly1, poly2))
        poly3 = [x + y for x,y in coef_tuple]
        return Polynomial(*(poly3))

    def __sub__(q, p):
        return q + (-p)

    def __neg__(q):
        coefs = q.coefficients()
        neg_coefs = map(lambda x: -x, coefs)
        return Polynomial(*(neg_coefs))

    def __mul__(q, p):
        if isinstance(p, Polynomial):
            poly1 = q.__values
            poly2 = p.__values
            r = [0] * (q.degree + p.degree + 1)
            for c in poly1:
                for k in poly2:
                    exp = c[0] + k[0]
                    coef = c[1] * k[1]
                    r[exp] += coef
            return Polynomial(*r)
        else:
            poly1 = q.coefficients()
            f = lambda item: item * p
            poly2 = list(map(f, poly1))
            return Polynomial(*(poly2))

    def __rmul__(q, p):
        return q * p

    def __truediv__(q, p):
        pass

    def __bool__(self):
        for coef in self.coefficients():
            if coef == 0:
                continue
            else:
                break
        else:
            return True
        return False

    def __eq__(q, p):
        if isinstance(p, bool):
            return bool(q) == p
        elif isinstance(p, Polynomial):
            poly1 = q.coefficients()
            poly2 = p.coefficients()
            if poly1 == poly2:
                return True
            else:
                return False
        else:
            return False

    def __getitem__(self, index):
        try:
            item = self.__values[index][1]
        except IndexError:
            item = 0
        finally:
            return item

    def __setitem__(self, index, value):
        self.__values[index][1] = value

    def __delitem__(self, index):
        self.__values[index][1] = 0

    def __len__(self):
        return self.degree

    def add(self, p):
        return self + p

    def sub(self, p):
        return self - p

    def coefficients(self):
        coefs = [x[1] for x in self.__values]
        return coefs

    def __call__(self, x):
        return self.calculate_values(x)

    def calculate_values(self, x):
        result = 0
        for degree, coef in enumerate(self.coefficients()):
            result += coef * (x)**degree 
        return result

    def get_domain(self):
        return self.__domain

    def get_values(self):
        return self.__values

    def plot_func(self, ax):
        y_intercept = self(0)
        ax.scatter(0, y_intercept, color = calculus.Function.function_part['y-intercept'])

    def alg_exp(self, iter):
        expression = ''
        #TODO algebraic expression

        for degree, coef in iter:
            if coef > 0:
                if degree == 0:
                    expression += f'+ {coef}'
                elif degree == 1:
                    expression += f'+ {coef}x '
                elif degree == self.degree:
                    expression += f'{coef}x^{degree} '
                else:
                    expression += f'+ {coef}x^{degree} '
            elif coef < 0:
                if degree == 0:
                    expression += f'- {_math.abs(coef)}'
                elif degree == 1:
                    expression += f'- {_math.abs(coef)}x '
                elif degree == self.degree:
                    expression += f'- {_math.abs(coef)}x^{degree} '
                else:
                    expression += f'- {_math.abs(coef)}x^{degree} '

        return expression

    def __repr__(self):
        return self.__algebraic_expression