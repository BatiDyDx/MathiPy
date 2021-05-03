cdef:
    double[7] sin_poly = [1., -1./6, 1./120, -1./5040, 1./362880, -1./39916800, 1./6227020800] # parity 1
    double[8] cos_poly = [1., -1./2, 1./24, -1./720, 1./40320, -1./3628800, 1./479001600, -1./87178291200] #parity 0
    double[8] tan_poly = [1., 1./3, 2./15, 17./315, 62./2835, 1382./155925, 21844./6081075, 929569./638512875] # parity 1
    double[10] arctan_poly = [1., -1./3, 1./5, -1./7, 1./9, -1./11, 1./13, -1./15, 1./17, -1./19] # parity 1

    pi    = 3.141592653589793
    pi_2  = 1.5707963267948966
    tau   = 6.283185307179586

cdef extern from '../../headers/cython_utils.h':
    double evaluate_poly_w_parity(double x, double *poly, int len, int parity)


cpdef double sin(double x):

    if not 0 <= x < tau:
        x %= tau

    if pi_2 < x <= pi:  # x is in second quadrant
        return sin(-x -pi)
    elif pi < x <= 3 / 2 * pi:  # x is in third quadrant
        return -sin(x - pi)
    elif 3 / 2 * pi < x < tau:  # x is in fourth quadrant
        return -sin(-(x + tau))

    if x > pi / 4:
        return cos(pi_2 - x)

    length = len(sin_poly)
    return evaluate_poly_w_parity(x, sin_poly, length, 1)


cpdef double cos(double x):

    if not 0 <= x < tau:
        x %= tau

    if pi_2 < x <= pi:  # x is in second quadrant
        return -cos(-x - pi)
    elif pi < x <= 3 / 2 * pi:  # x is in third quadrant
        return -cos(x - pi)
    elif 3 / 2 * pi < x < tau:  # x is in fourth quadrant
        return cos(-(x + tau))

    if x > pi / 4:
        return sin(pi_2 - x)

    length = len(cos_poly)
    return evaluate_poly_w_parity(x, cos_poly, length, 0)


def tan(double x):
    if not 0 <= x < pi:
        x %= pi

    if pi_2 < x < pi:  # x is in second quadrant
        return -tan(-x -pi)

    if pi / 4 <= x:
        return 1 / tan(pi_2 - x)

    if pi / 8 <= x:
        y = tan(x / 2)
        return 2 * y / (1 - (y ** 2))

    length = len(tan_poly)
    return evaluate_poly_w_parity(x, tan_poly, length, 1)


def arcsin(double x):
    return arctan(x / ((1 - x ** 2) ** 0.5))


def arccos(double x):
    cdef double y = arctan(((1 - x ** 2) ** 0.5) / x)
    if x < 0:
        y += pi
    return y


cpdef double arctan(double x):
    if x < 0:
        return -arctan(-x)

    if 1 < x:
        return pi_2 - arctan(1 / x)

    if 2 - (3 ** .5) < x:
        return pi / 6 + arctan(((3 ** .5) * x - 1) / (3 ** .5 + x))

    length = len(arctan_poly)
    return evaluate_poly_w_parity(x, arctan_poly, length, 1)
