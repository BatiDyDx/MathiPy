from mathipy import calculus, _math, _complex
import numpy as np

class Log(calculus.Function):
    function_type = 'Logarithmic'
    asymptote = True
    def __init__(self, b = np.e, **kwargs):
        self.__b = b
        self.__a = kwargs.get('a', 0)
        self.__c = kwargs.get('n', 1)
        self.__k = kwargs.get('k', 1)
        self.__n = kwargs.get('n', 1)
        self.__va = -self.__a / self.__k
        self.__root = self.find_roots()
        if b <= 1:
            raise ValueError('Base must be greater than 1')

    def get_yint(self):
        try:
            return self(0)
        except ValueError:
            return None

    def find_roots(self):
        exp = -self.__c / self.__n
        root = ((self.__b ** exp) - self.__a) / self.__k
        return root

    @staticmethod
    def ln(x):
        if isinstance(x, _complex.Complex):
            return _complex.Complex(Log.ln(x.r), x.theta)
        elif isinstance(x, complex):
            return Log.ln(_complex.Complex(x.real, x.imag))
        if x <= 0:
            raise ValueError('Argument must be positive')
        else:
            return 2 * np.arctanh((x - 1)/(x + 1))

    @staticmethod
    def log(x, base = 10):
        if isinstance(x, _complex.Complex):
            return _complex.Complex(Log.ln(x.r), x.theta) / Log.ln(base)
        elif isinstance(x, complex):
            return Log.log(_complex.Complex(x.real, x.imag), base= base) 
        if x <= 0:
            raise ValueError('Argument must be positive')
        elif base <= 1:
            raise ValueError('Base must be greater than 1')
        if base == np.e:
            return Log.ln(x)
        else:
            log_n = Log.ln(x) / Log.ln(base)
            return _math.round_int(log_n)

    def calculate_values(self,x):
        if _math.is_iter(x):
            return list(map(self.calculate_values, x))
        else:
            try:
                return self.__n * Log.log(self.__k * x + self.__a, base = self.__b) + self.__c
            except ValueError:
                return None

    def plot_func(self, ax):
        if self.get_yint() != None:
            y_intercept = self.get_yint()
            ax.scatter(0, y_intercept, c = calculus.Function.function_part['y-intercept'])

        if self.__root:
            ax.scatter(self.__root, 0, color = calculus.Function.function_part['roots'])

        v_asymptote = self.__va
        y_min, y_max = ax.get_ylim()
        ax.vlines(v_asymptote, y_min, y_max, color = calculus.Function.function_part['asymptote'], linewidth = 2.5, linestyle = '--')

    def __call__(self, x):
        return self.__n * Log.log(self.__k * x + self.__a, base = self.__b) + self.__c

    def __repr__(self):
        representation = ''
        if self.__n != 1:
            representation += f'{self.__n} · '
        if self.__b == np.e:
            representation += 'ln('
        elif self.__b == 10:
            representation += 'log('
        else:  
            representation += f'log_{self.__b}('
        if self.__k != 1:
            representation += f'{self.__k}x'
        else:
            representation += 'x'
        if self.__a > 0:
            representation += f' + {self.__a})'
        elif self.__a < 0:
            representation += f' - {_math.abs(self.__a)})'
        else:
            representation += ')'
        if self.__c > 0:
            representation += f' + {self.__c}'
        elif self.__c < 0:
            representation += f' - {_math.abs(self.__c)}'