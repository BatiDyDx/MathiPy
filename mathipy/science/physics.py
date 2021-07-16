from numpy import linspace
from mathipy.math import _math
from mathipy import numeric_operations as ops
from mathipy.math.linalg import Matrix
import math

## Constants #######################
alpha = 7.297352568e-3          # adimensional | finite structure
c     = 299_792_458             # m / s | relativistic speed of light
G     = 6.6743015e-11           # metres^3 / (kg * s) | newtonian constant of gravitation
k     = 8.987551792314e9        # N * m^2 / C^2 | Coulomb's constant
q_e   = 1.602176634e-19         # C | elementary charge
Z_0   = 376.730313668           # ohm | impedance of void
epsilon_0   = 8.8541878128e-12        # F / m | vacuum electric permitivity
mu_0   = 1.25663706212e-6        # N / A^2 | vacuum magnetic permeability
h     = 6.6260693e-34           # m^2 * kg / s | planck constant
h_bar = 1.054571628e-34         # m^2 * kg / s | reduced planck constant
m_u   = 1.66053886e-27          # kg | atomic mass constant
m_e   = 9.109383701528e-31      # kg | electron mass
m_p   = 1.6726219236951e-27     # kg | proton mass
m_n   = 1.6749274980495e-27     # kg | neutron mass
E_h   = 4.35974417e-18          # J | energy of Hartree
R     = 8.314472                # J * (K ^ -1) * mol ^ -1 | universal constant of ideal gases
F     = 96_485.3383             # C / mol | Faraday's constant
k_B   = 1.3806505e-23           # J / K | Boltzmann's constant
a_0   = 0.5291772108e-10        # m | Bohr's radius
####################################


class Measure:
    
    def __init__(self, x, delta):
        
        if ops.is_iterable(x):
            self.measure = ops.mean(x)
            mx, mn = ops.max(x) + delta, ops.min(x) - delta

            self.abs_error = max(abs(mx - self.measure), abs(mn - self.measure))
            self.relative_error = self.abs_error / abs(self.measure)
            self.percentual_error = str(self.relative_error * 100) + "%"

        elif ops.is_scalar(x):
            self.measure = x
            
            if type(delta) is str:
                
                if delta[-1] == '%':
                    epsilon = float(delta[:-1])
                else:
                    epsilon = float(delta)
                
                self.relative_error = epsilon / 100
                self.percentual_error = str(epsilon) + "%"
            
                self.abs_error = self.relative_error * abs(self.measure)
            
            else:
                self.abs_error = delta

                self.relative_error = self.abs_error / abs(self.measure)
                self.percentual_error = str(self.relative_error * 100) + "%"

        self._round_sig_figs()
        assert self.abs_error > 0, f'Absolute error must be greater than zero, but received delta: {delta}'


    def percentual_expression(self):
        return f"({self.measure} ± {self.percentual_error})"

    def _round_sig_figs(self):
        fsfp = -int(ops.floor(math.log10(abs(self.abs_error)))) # first significant figure place
        self.abs_error = round(self.abs_error, fsfp)
        self.measure = round(self.measure, fsfp)

    def sign_disc(self, m):
        if not isinstance(m, Measure):
            raise TypeError('sign_disc recieved {m.__class__.__name} instead of Measure type')

        delta = abs(self.measure - m.measure)
        return delta > self.abs_error + m.abs_error

    @staticmethod
    def make_constant(k: float, *args, epsilon_factor: int = 1) -> float:
        # Minimum relative error of the measures passed as arguments
        mn_relative_error = min(args, key=(lambda m: m.relative_error)).relative_error
        
        # Take the order of magnitude of the minimum relative error
        rel_error_order = int(ops.floor(math.log10(abs(mn_relative_error))))
        
        # Assign a number of an order of magnitude less
        epsilon_k = epsilon_factor * 10 ** (rel_error_order - 1)
        
        # Get the absolute error of the constant k
        delta_k = epsilon_k * k
        
        # Get the order of magnitude of delta k
        k_order = int(ops.floor(math.log10(abs(delta_k))))

        # Truncate k to the order of magnitude of its absolute error
        return ops.trunc(k, -k_order)

    def __add__(self, m):
        if not isinstance(m, Measure):
            raise TypeError(f'Cannot perform addition on Measure and {m.__class__.__name__}')
        
        y = self.measure + m.measure
        delta_y = self.abs_error + m.abs_error
        
        return Measure(y, delta_y)

    def __neg__(self):
        return Measure(-self.measure, self.abs_error)

    def __sub__(self, m):
        return self + (-m)

    def __mul__(self, m):
        if isinstance(m, Measure):
            y = self.measure * m.measure
            delta_y = (self.relative_error + m.relative_error) * y
            return Measure(y, delta_y)

        elif ops.is_scalar(m) and not isinstance(m, complex):
            return Measure(self.measure * m, self.abs_error * m)

        else:
            raise TypeError(f'Product is not supported between Measure type and {m.__class__.__name__}')

    def __rmul__(self, m):
        return self.__mul__(m)

    def __truediv__(self, m):
        if isinstance(m, Measure):
            return self * Measure(1 / m.measure, m.abs_error)
        
        elif ops.is_scalar(m) and not isinstance(m, complex):
            return Measure(self.measure / m, self.abs_error / m)
        
        else:
            raise TypeError(f'Division is not supported between Measure type and {m.__class__.__name__}')

    def __pow__(self, n):
        if not ops.is_scalar(n) or isinstance(n, complex):
            raise TypeError(f'Power is not supported between Measure type and {n.__class__.__name__}')
        else:
            y = self.measure ** n
            delta_y = self.relative_error * n * y
            return Measure(y, delta_y)

    def __eq__(self, m):
        return not self.sign_disc(m)

    def __ne__(self, m):
        return self.sign_disc(m)

    def __set__(self):
        return set(linspace(self.measure - self.abs_error, self.measure + self.abs_error))

    def __str__(self):
        return f"({self.measure} ± {self.abs_error})"

    def __repr__(self):
        return 'Measure object'


minkowski_metric = Matrix([
    [ 1,  0,  0,  0],
    [ 0, -1,  0,  0],
    [ 0,  0, -1,  0],
    [ 0,  0,  0, -1],
])

def distance(x: tuple, g = minkowski_metric):
    dist = 0
    for i in range(g.m_dimension):
        for j in range(g.n_dimension):
            dist += g[i, j] * x[i] * x[j]
    return _math.sqrt(dist)

def time_dilation(x: tuple):
    """
    time must be measured in lightseconds. To achieve this
    multiply time by c:

    >>> time(seconds) * c(metres / seconds) = light_seconds(metres)
    """
    tau = distance(x)
    t, *D = x
    v = _math.sqrt(sum(map(lambda d: d ** 2, D))) / t
    try:
        vt = t / tau
    except ZeroDivisionError:
        vt = float('inf')

    vx = v * vt
    velocity = _math.sqrt(c ** 2 * vt ** 2 - vx ** 2)

    print('vx is: ', vx)
    print('velocity is: ', velocity)

    return vt

# TODO
def space_dilation():
    pass
