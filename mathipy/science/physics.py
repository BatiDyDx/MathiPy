import numpy as np
from mathipy._math import differential

c = 3e8

def d(x, t):
    return np.sqrt(c ** 2 * t ** 2 - x ** 2)

def time_dilation(x, t):
    v = x/t
    tau = d(x, t)
    try:
        vt = c * differential(t) / differential(tau)
        vt = np.round(vt, decimals = 15)
    except ZeroDivisionError:
        vt = float('inf')

    vx = v * vt
    velocity = np.sqrt(c ** 2 * vt ** 2 - vx ** 2)

    print('vt is equal to: ', vt)
    print('Tau in light meters is: ', tau)
    print('Tau in seconds is: ', tau / c)

