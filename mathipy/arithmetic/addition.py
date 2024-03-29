from mathipy import arithmetic

class Sum(arithmetic.algebraic_expression.AlgebraicExpression):
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.__config__()

    def __repr__(self):
        return f'({self.a} + {self.b})'

    def evaluate(self, vars):
        return self.a.evaluate(vars) + self.b.evaluate(vars)


class Minus(arithmetic.algebraic_expression.AlgebraicExpression):
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.__config__()

    def __repr__(self):
        return f'({self.a} - {self.b})'

    def evaluate(self, vars):
        return self.a.evaluate(vars) - self.b.evaluate(vars)
