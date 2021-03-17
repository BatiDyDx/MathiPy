import numpy as np
from mathipy.linalg import Vector, Matrix
from mathipy._math import sqrt2, tau, cos, sin, e, pi

###Constants########################
h     = 6.62607004e-34      #m^2 * kg / s | planck constant
h_bar = h / tau             #ℏ (reduced planck constant)
m_e   = 9.109383701528e-31  # kg | electron mass
m_p   = 1.6726219236951e-27 # kg | proton mass
m_n   = 1.6749274980495e-27 # kg | neutron mass
####################################

def ket(a: int, n: int= -1) -> Vector:
    if isinstance(a, str):
        if a == '+':
            el = np.array([[1, 1]])
        elif a == '-':
            el = np.array([[1, -1]])
        return Vector(el / sqrt2)

    if n == -1:
        i = 0
        while 2 ** i < a:
            i += 1
        n = i + 1
    el = [[0 if a != i else 1 for i in range(2**n)]]
    return Vector(el)

EPR = (ket(0, 2) + ket(3, 2)) / sqrt2

H = Matrix((1 / sqrt2) * np.array(
    [
        [1,  1],
        [1, -1]
    ]  
))

X = Matrix([
    [0, 1],
    [1, 0]
])

Y = Matrix([
    [0, -1j],
    [1j,  0]
])

Z = Matrix([
    [1,  0],
    [0, -1]
])

def Rx(theta):
    a = cos(theta / 2)
    b = -1j * sin(theta / 2)
    el = np.array([
        [a, b],
        [b, a]
    ])
    return Matrix(el)

def Ry(theta):
    a = cos(theta / 2)
    b = sin(theta / 2)
    el = np.array([
        [a, -b],
        [b,  a]
    ])
    return Matrix(el)

def Rz(theta):
    x = e ** (1j * theta)
    el = np.array([
        [1, 0],
        [0, x]
    ])
    return Matrix(el)

S = Rz(pi / 2)
Sdg = Rz(-pi / 2)
T = Rz(pi / 4)