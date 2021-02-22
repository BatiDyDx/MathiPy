import re
from mathipy import calculus
from mathipy import _math
from mathipy import numeric_operations as ops

class Polynomial(calculus.Function):
    function_type = 'Polynomial'
    def __init__(self, *args, **kwargs):
        if args:
            values = [[degree, coef] for degree, coef in enumerate(args)]
        elif kwargs:
            values = self.__process_coefficents(kwargs)
        while values[-1][1] == 0 and len(values) > 1:
            del values[-1]

        domain = 'Complex'
        for i in values:
            if isinstance(i[1], (complex)):
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
        if ops.is_scalar(p):
            p = Polynomial(p)
        max_degree = ops.max([len(q), len(p)]) + 1
        coefs_1 = q.coefficients(max_degree)
        coefs_2 = p.coefficients(max_degree)
        coef_tuple = list(zip(coefs_1, coefs_2))
        coefs_3 = [x + y for x, y in coef_tuple]
        return Polynomial(*(coefs_3))

    def __radd__(q, p):
        return q + p

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
        elif ops.is_scalar(p):
            poly1 = q.coefficients()
            poly2 = [i * p for i in poly1]
            return Polynomial(*(poly2))
        else:
            return p * q

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

    def coefficients(self, length=-1):
        coefs = [x[1] for x in self.__values]
        if length > -1:
            while len(coefs) < length:
                coefs.append(0)
        return coefs

    def __iter__(self):
        return iter(self.coefficients())

    def __call__(self, x):
        return self.calculate_values(x)

    def calculate_values(self, x):
        result = 0
        for degree, coef in enumerate(self.coefficients()):
            result += coef * (x)**degree 
        return result

    def find_roots(self):
        pass

    def get_domain(self):
        return self.__domain

    def get_values(self):
        return self.__values

    def plot_func(self, ax):
        y_intercept = self(0)
        ax.scatter(0, y_intercept, color = calculus.Function.function_part['y-intercept'])

    def __repr__(self):
        expression = []
        #TODO algebraic expression
        for degree, coef in self.__values:
            if coef != 0:
                if degree != 0:
                    s = f'{coef}x^{degree}'
                else:
                    s = str(coef)
                expression.append(s)
        expression = ' + '.join(expression[::-1])
        return expression