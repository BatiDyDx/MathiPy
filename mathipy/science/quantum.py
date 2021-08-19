import numpy as np
from mathipy.math.linalg import Vector, Matrix
from mathipy.math import trigonometry as trig, ntheory


def ket(a: int, n: int= -1) -> Vector:
    if isinstance(a, str):
        if a == '+':
            el = np.array([[1, 1]])
        elif a == '-':
            el = np.array([[1, -1]])
        return Vector(el / ntheory.math_constants['sqrt2'])

    if n == -1:
        i = 0
        while 2 ** i < a:
            i += 1
        n = i + 1
    el = [[0 if a != i else 1 for i in range(2**n)]]
    return Vector(el)

EPR = (ket(0, 2) + ket(3, 2)) / ntheory.math_constants['sqrt2']

H = Matrix((1 / ntheory.math_constants['sqrt2']) * np.array(
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
    a = trig.cos(theta / 2)
    b = -1j * trig.sin(theta / 2)
    el = np.array([
        [a, b],
        [b, a]
    ])
    return Matrix(el)

def Ry(theta):
    a = trig.cos(theta / 2)
    b = trig.sin(theta / 2)
    el = np.array([
        [a, -b],
        [b,  a]
    ])
    return Matrix(el)

def Rz(theta):
    x = ntheory.e ** (1j * theta)
    el = np.array([
        [1, 0],
        [0, x]
    ])
    return Matrix(el)

S = Rz(ntheory.math_constants['pi/2'])
Sdg = Rz(-ntheory.math_constants['pi/2'])
T = Rz(ntheory.pi / 4)