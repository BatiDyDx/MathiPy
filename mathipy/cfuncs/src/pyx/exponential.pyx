cdef:
	double[8] exp_poly = [1., 1., 1./2, 1./6, 1./24, 1./120, 1./720, 1./5040] # no parity
	double[8] ln_poly = [1., 1./3, 1./5, 1./7, 1./9, 1./11, 1./13, 1./15] # parity 1

	double e = 2.718281828459045
	double ln_10 = 2.302585092994046

cdef extern from '../../headers/cython_utils.h':
	double evaluate_poly_w_parity(double x, double *poly, int len, int parity)
	double evaluate_poly(double x, double *poly, int len)
	int magnitude_order(double x)


def exp(double x):
	cdef int n = int(x)
	cdef double r = x - n

	cdef:
		int i
		double y = 1.0

	for i from 0 <= i < n:
		y *= e

	length = len(exp_poly)
	y *= evaluate_poly(r/5, exp_poly, length) ** 5
	return y

def exp2_0(double x):
	cdef:
		int p = magnitude_order(x)
		int order_diff = p + 10
		int m = 10 ** order_diff
	
	cdef double y = evaluate_poly(x / m, exp_poly, 8) ** m
	return y	


def ln(double x):

	cdef int p = magnitude_order(x)
	cdef double mantissa = x / (10 ** p)

	cdef int root_index = 5
	cdef double n = root(mantissa, root_index)
	cdef double y = (n - 1) / (n + 1)
	
	length = len(ln_poly)
	out = 2 * evaluate_poly_w_parity(y, ln_poly, length, 1)

	return root_index * out + ln_10 * p


cpdef double root(double x, int n, double init_value=0.):

	if init_value == 0.:
		init_value = x / n

	cdef int i
	cdef double x_n = init_value

	for i from 0 <= i < 10:
		x_n = (1. / n) * ((n - 1) * x_n + x / (x_n ** (n - 1)))

	if x_n ** n - x > 1e-15:
		return root(x, n, x_n)

	return x_n
