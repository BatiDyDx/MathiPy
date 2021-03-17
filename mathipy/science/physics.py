from mathipy._math import differential, sqrt
from mathipy.linalg import Matrix

###Constants########################
c     = 299792458             #m / s | relativistic speed of light
G     = 6.6743015e-11         #metres^3 / (kg * s) | Newtonian constant of gravitation
k     = 8.987551792314e9      #N * m^2 / C^2 | Coulomb constant
q_e   = 1.602176634e-19       #C | elementary charge
alpha = 7.297352569311e-3     #finite structure
####################################

minkowski_metric = Matrix([
    [ 1,  0,  0,  0],
    [ 0, -1,  0,  0],
    [ 0,  0, -1,  0],
    [ 0,  0,  0, -1],
])

def distance(x: tuple, g=minkowski_metric):
    dist = 0
    for i in range(g.m_dimension):
        for j in range(g.n_dimension):
            dist += g[i, j] * x[i] * x[j]
    return sqrt(dist)

def time_dilation(x: tuple):
    """
    time must be measured in lightseconds. To achieve this
    multiply time by c:

    >>> time(seconds) * c(metres / seconds) = light_seconds(metres)
    """
    tau = distance(x)
    t, *D = x
    v = sqrt(sum(map(lambda d: d ** 2, D))) / t
    try:
        vt = differential(t) / differential(tau)
    except ZeroDivisionError:
        vt = float('inf')

    vx = v * vt
    velocity = sqrt(c ** 2 * vt ** 2 - vx ** 2)

    print('vx is: ', vx)
    print('velocity is: ', velocity)

    return vt

