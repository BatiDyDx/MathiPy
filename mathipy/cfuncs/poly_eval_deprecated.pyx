cdef double evaluate_poly_w_parity(double x, list poly, int parity):
    cdef int i
    cdef double y = 0.0
    cdef int d = len(poly)
    for i from 0 <= i < d:
        exp = 2 * i + parity
        y += (x ** exp) * poly[i]
    return y

cdef double evaluate_poly(double x, list poly):
    cdef int i
    cdef double y = 0.0
    cdef int d = len(poly)
    for i from 0 <= i < d:
        y += (x ** i) * poly[i]
    return y