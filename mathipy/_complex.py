import numpy as np
import matplotlib.pyplot as plt
from mathipy import _math
from mathipy import arithmetic as arm
from mathipy import linalg

class Complex(object):
    __class__ = complex
    def __init__(self, x, y, coordinate = 'Cartesian'):
        if coordinate == 'Cartesian':
            self.a = x
            self.b = y
            self.r = np.sqrt(self.a**2 + self.b**2)
            self.theta = self.phase()
        elif coordinate == 'Polar':
            self.r = x
            self.theta = y
            a = self.r * np.cos(self.theta)
            self.a = _math.round_int(a)
            b = self.r * np.sin(self.theta)
            self.b = _math.round_int(b)

        self.__cartesian_representation = f'({self.a} + {self.b}i)'
        self.__polar_representation = f'{self.r} * e^i({self.theta})'

    @property
    def real(self):
        return self.a

    @property
    def imag(self):
        return self.b
        
    def __add__(z, w):
        z_real, z_imag = z.split()
    
        if isinstance(w, (int, float)):
            return Complex(z_real + w, z_imag)  
        elif isinstance(w, complex):
            return Complex(z_real + w.real, z_imag + w.imag)
        else:
            w_real, w_imag = w.split()
            real_part = z_real + w_real
            real_part = _math.round_int(real_part)
            imag_part = z_imag + w_imag
            imag_part = _math.round_int(imag_part)
            return Complex(real_part, imag_part)

    def __radd__(z, w):
        return z + w

    def __sub__(z, w):
        return z + (-w)

    def __rsub__(z, w):
        return w + (-z)

    def __mul__(z, w):
        z_real, z_imag = z.split()
        if isinstance(w, (int, float)):
            return Complex(z_real * w, z_imag * w)  
        elif isinstance(w, complex):
            w_real, w_imag = w.real, w.imag
        elif isinstance(w, linalg.Tensor):
            return w.__rmul__(z)
        else:
            w_real, w_imag = w.split()

        real_part = (z_real * w_real) - (z_imag * w_imag)
        real_part = _math.round_int(real_part)
        imag_part = (z_real * w_imag) + (z_imag * w_real)
        imag_part = _math.round_int(imag_part)
        return Complex(real_part, imag_part)

    def __rmul__(z, w):
        return z * w

    def __truediv__(z, w):
        if isinstance(w, (int, float)):
            return Complex(z.a / w, z.b / w)  
        elif isinstance(w, complex):
            return z * (1 / w)
        elif isinstance(w, Complex):
            return z * w.inverse()
        else:
            raise TypeError(f'{type(w)} does not support Complex division')

    def __rtruediv__(z, w):
        return z.inverse() * w

    def __floordiv__(z, w):
        if isinstance(w, (int, float)):
            return Complex(z.a // w, z.b // w)  
        elif isinstance(w, complex):
            result = z * (1 / w)
            result.a, result.b = int(result.a), int(result.b)
            return result
        elif isinstance(w, Complex):
            result = z * w.inverse()
            result.a, result.b = int(result.a), int(result.b)
            return result
        else:
            raise TypeError(f'{type(w)} does not support Complex floor division')

    def __pow__(z, exp):
        if isinstance(exp, complex):
            return arm.e ** (exp * _math.ln(z))
        if exp == 1:
            return z
        elif exp > 1:
            return z * (z ** (exp - 1))
        elif exp < 0:
            return z.inverse() ** -exp
        elif exp == 0:
            return 1
        elif 0 < exp < 1:
            return z.root(1 / exp)

    def __rpow__(z, a):
        if isinstance(a, complex):
            return arm.e ** (z * _math.ln(a))
        else:
            x = _math.round_int(_math.cos(_math.ln(a) * z.b))
            y = _math.round_int(_math.sin(_math.ln(a) * z.b))
            w = Complex(x, y)
            return (a ** z.a) * w

    def __neg__(z):
        real_part, imag_part = z.split()
        return Complex(-real_part, -imag_part)

    def __eq__(z, w):
        z_real, z_imag = z.split()
        if isinstance(w, (int, float)):
            if z_real == w and z_imag == 0:
                return True
            else:
                return False
        elif isinstance(w, bool):
            return bool(z) == w
        else:
            w_real, w_imag = w.real, w.imag
            if (z_real == w_real) and (z_imag == w_imag):
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

    def add(self, w):
        return self + w

    def sub(self, w):
        return self - w

    def mul(self, w):
        return self * w

    def divide(self, w):
        return self / w

    def power(self, w):
        return self ** w

    def split(self):
        return self.a, self.b

    def root(self, exp: float, all_roots = False):
        r = self.r ** (1 / exp)
        theta_n = tuple((self.theta + arm.tau * k) / exp for k in range(round(exp)))
        if all_roots:
            roots = []
            for theta in theta_n:
                roots.append(Complex(r, theta, coordinate='Polar'))
            return roots
        else:
            return Complex(r, theta_n[0], coordinate='Polar')

    def conjugate(self):
        real_part = self.a
        real_part = _math.round_int(real_part)
        imag_part = - self.b
        imag_part = _math.round_int(imag_part)
        return Complex(real_part, imag_part)

    def inverse(self):
        real_denominator, imag_denominator = self.split() 

        denominator = (self.a)**2 + (self.b)**2
        real_part = self.a/denominator
        real_part = _math.round_int(real_part)
        imag_part = - self.b/denominator
        imag_part = _math.round_int(imag_part)

        return Complex(real_part, imag_part)

    def plot(self):
        angle = np.linspace(0, self.theta, 100)
        x = self.r * np.cos(angle) / 5
        y = self.r * np.sin(angle) / 5
        a, b = self.split()
        fig, ax = plt.subplots()
    
        ax.set_title('Complex number plot')
        plt.style.use('dark_background')

        plt.ylabel('Imaginary axis')
        plt.xlabel('Real axis')
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

    def phase(self):
        if self.a == 0:
            if self.b > 0:
                return np.pi / 2
            elif self.b < 0:
                return - np.pi / 2
            else:
                return None
        elif self.a < 0:
            if self.b >= 0:
                return np.arctan(self.b / self.a) + np.pi
            else:
                return np.arctan(self.b / self.a) - np.pi
        else:
            return np.arctan(self.b / self.a)

    def polar_expression(self):
        return self.__polar_representation

    def cartesian_expression(self):
        return self.__cartesian_representation

    def __str__(self):
        return self.cartesian_expression()
        #display(Latex(f'${self.r}  e^{{i {self.theta}}}$'))

    def __repr__(self):
        return str(self)