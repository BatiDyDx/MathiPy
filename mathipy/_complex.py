from fractions import Fraction
import numpy as np
import matplotlib.pyplot as plt
from mathipy import _math
from mathipy import numeric_operations as ops

class Complex(object):
    __class__ = complex
    def __init__(self, x, y, coordinate = 'Cartesian'):
        if coordinate == 'Cartesian':
            self.a = x
            self.b = y
            self.r = _math.sqrt(self.a**2 + self.b**2)
            self.theta = self.phase()
        elif coordinate == 'Polar':
            self.r = x
            self.theta = y
            a = self.r * _math.cos(self.theta)
            self.a = ops.round_int(a)
            b = self.r * _math.sin(self.theta)
            self.b = ops.round_int(b)
        
        self.a, self.b, self.r = ops.round_int([self.a, self.b, self.r])
    
    @property
    def real(self):
        return self.a

    @property
    def imag(self):
        return self.b

    @property
    def mod(self):
        return self.r

    @property
    def arg(self):
        return self.theta

    def __add__(z, w):
        if isinstance(w, (int, float)):
            return Complex(z.real + w, z.imag)  
        elif isinstance(w, complex):
            real_part = z.real + w.real
            imag_part = z.imag + w.imag
            return Complex(real_part, imag_part)
        else:
            return w.__add__(z)

    def __radd__(z, w):
        return z + w

    def __sub__(z, w):
        return z + (-w)

    def __rsub__(z, w):
        return (-z) + w

    def __mul__(z, w):
        if ops.is_scalar(w):
            if isinstance(w, (int, float)):
                return Complex(z.real * w, z.imag * w)  
            else:
                real_part = (z.real * w.real) - (z.imag * w.imag)
                imag_part = (z.real * w.imag) + (z.imag * w.real)
                return Complex(real_part, imag_part)
        else:
            return w.__rmul__(z)

    def __rmul__(z, w):
        return z * w

    def __truediv__(z, w):
        if ops.is_scalar(w):
            if isinstance(w, (int, float)):
                return Complex(z.a / w, z.b / w)  
            elif isinstance(w, complex):
                return z * (1 / w)
            elif isinstance(w, Complex):
                return z * w.inverse()
        else:
            return w.__rtruediv__(z)

    def __rtruediv__(z, w):
        return z.inverse() * w

    def __floordiv__(z, w):
        if isinstance(w, (int, float)):
            return Complex(z.a // w, z.b // w)  
        elif isinstance(w, complex):
            r = z * (1 / w)
            r.a, r.b = int(r.a), int(r.b)
            return r
        else:
            raise TypeError(f'{type(w)} does not support Complex floor division')

    def __pow__(z, exp):
        if isinstance(exp, complex):
            return _math.e ** (exp * _math.ln(z))
        if exp == 1:
            return z
        elif exp > 1:
            return z * (z ** (exp - 1))
        elif exp < 0:
            return z.inverse() ** -exp
        elif exp == 0:
            return 1
        elif 0 < exp < 1:
            exp_frac = str(Fraction(exp).limit_denominator())
            frac_numerator, frac_denominator = exp_frac.split('/')
            return z.root(int(frac_denominator)) ** int(frac_numerator)

    def __rpow__(z, a):
        if isinstance(a, complex):
            return _math.e ** (z * _math.ln(a))
        else:
            x = ops.round_int(_math.cos(_math.ln(a) * z.b))
            y = ops.round_int(_math.sin(_math.ln(a) * z.b))
            w = Complex(x, y)
            return (a ** z.a) * w

    def __neg__(z):
        return Complex(-z.real, -z.imag)

    def __eq__(z, w):
        if isinstance(w, (int, float)):
            if z.real == w and z.imag == 0:
                return True
            else:
                return False
        elif isinstance(w, bool):
            return bool(z) == w
        else:
            if (z.real == w.real) and (z.imag == w.imag):
                return True
            else:
                return False

    def __int__(self):
        return int(self.a)

    def __float__(self):
        return float(self.a)

    def __complex__(self):
        return self.a + self.b*1j

    def __bool__(self):
        if self.a == 0 and self.b == 0:
            return False
        else:
            return True

    def split(self):
        return self.a, self.b

    def root(self, n: int, all_roots= False):
        r = self.r ** (1 / n)
        if all_roots:
            #return Complex.unit_circle_roots(self.mod, )
            roots = []
            theta_n = tuple((self.theta + _math.tau * k) / n for k in range(n))
            for theta in theta_n:
                roots.append(Complex(r, theta, coordinate='Polar'))
            return roots
        else:
            theta = self.theta / n
            return Complex(r, theta, coordinate='Polar')

    def conjugate(self):
        return Complex(self.real, -self.imag)

    def inverse(self):
        real_denominator, imag_denominator = self.split() 
        denominator = (self.a) ** 2 + (self.b) ** 2
        real_part = self.a / denominator
        imag_part = - self.b / denominator
        
        return Complex(real_part, imag_part)

    def plot(self, coordinate='cartesian'):
        angle = np.linspace(0, self.theta, 100)
        x = self.r * _math.cos(angle) / 5
        y = self.r * _math.sin(angle) / 5
        a, b = self.split()
        fig = plt.figure()
        #TODO
        #POLAR REPRESENTATION
        p = 'rectilinear' if coordinate == 'cartesian' else 'polar'
        ax = fig.add_subplot(projection=p)
    
        ax.set_title('Complex number plot')
        plt.style.use('dark_background')

        plt.xlabel('Real axis')
        plt.ylabel('Imaginary axis')
        plt.grid()

        if abs(a) >= 1:
            x_min, x_max = - abs(a) - 1, abs(a) + 0.5
        else:
            x_min, x_max = -1.5, 1.5

        if abs(b) >= 1:
            y_min, y_max = - abs(b) - 0.5, abs(b) + 0.5
        else:
            y_min, y_max = -1.5, 1.5

        ax.hlines(0 ,x_min, x_max, color = 'white')
        ax.vlines(0, y_min, y_max, color = 'white')

        element_a = plt.plot([0,a] ,[0,0], '-', linewidth = 3 , c='green')
        element_b = plt.plot([a, a] ,[0,b], '-', linewidth = 3 , c='orange')
        element_r = plt.plot([0,a] ,[0,b], '--', linewidth = 3, c='blue' )
        element_theta = plt.plot(x, y, color='red')

        textstr = '\n'.join(('$a: green$', '$bi: orange$', '$r: blue$', '$\\theta: red$'))
        props = dict(boxstyle='round', facecolor='lightblue', alpha=0.5)
        ax.text(0.05,0.95, textstr, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=props)

        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)
        plt.show()

    @staticmethod
    def i(exp):
        if exp % 4 == 0:
            return 1
        elif exp % 4 == 1:
            return Complex(0,1)
        elif exp % 4 == 2:
            return -1
        elif exp % 4 == 3:
            return Complex(0,-1)

    @staticmethod
    def circle_roots(n: int, r= 1):
        roots = []
        w = _math.tau / n
        for k in range(n):
            theta = w * k
            roots.append(Complex(r, theta, coordinate='Polar'))
        return roots

    def phase(self):
        if self.a == 0:
            if self.b > 0:
                return _math.pi / 2
            elif self.b < 0:
                return - _math.pi / 2
            else:
                return None
        elif self.a < 0:
            if self.b >= 0:
                return np.arctan(self.b / self.a) + _math.pi
            else:
                return np.arctan(self.b / self.a) - _math.pi
        else:
            return np.arctan(self.b / self.a)

    def polar_expression(self):
        return f'{self.r} * e^i({self.theta})'
    
    def cartesian_expression(self):
        return f'({self.a} + {self.b}i)'
    
    def __str__(self):
        return self.cartesian_expression()
        #display(Latex(f'${self.r}  e^{{i {self.theta}}}$'))

    def __repr__(self):
        return str(self)

def real(Z):
    if ops.is_scalar(Z):
        return Z.real
    elif ops.is_iter(Z):
        return np.array(list(map(real, Z)))

def imag(Z):
    if ops.is_scalar(Z):
        return Z.imag
    elif ops.is_iter(Z):
        return np.array(list(map(imag, Z)))

def module(Z):
    if ops.is_scalar(Z):
        try:
            return Z.mod
        except AttributeError:
            return Complex(Z.real, Z.imag).mod
    elif ops.is_iter(Z):
        return np.array(list(map(module, Z)))

def argument(Z):
    if ops.is_scalar(Z):
        try:
            return Z.arg
        except AttributeError:
            return Complex(Z.real, Z.imag).arg
    elif ops.is_iter(Z):
        return np.array(list(map(argument, Z)))

def to_Complex(Z):
    if ops.is_iter(Z):
        f = lambda z: to_Complex(z)
        return list(map(f, Z))
    else:
        return Complex(Z.real, Z.imag)