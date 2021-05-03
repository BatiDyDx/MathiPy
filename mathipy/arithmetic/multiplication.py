from mathipy.arithmetic import algebraic_expression


class Product(algebraic_expression.AlgebraicExpression):
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.__config__()

    def __repr__(self):
        return f'({self.a} * {self.b})'

    def evaluate(self, vars):
        return self.a.evaluate(vars) * self.b.evaluate(vars)


class Division(algebraic_expression.AlgebraicExpression):
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.__config__()

    def __repr__(self):
        return f'([{self.a}] / [{self.b}])'

    def evaluate(self, vars):
        try:
            return self.a.evaluate(vars) / self.b.evaluate(vars)
        except ZeroDivisionError:
            return algebraic_expression.Infinite()
