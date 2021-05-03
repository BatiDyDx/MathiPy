#include "../../headers/cython_utils.h"
#include <math.h>

/* 
Used for evaluating Taylor Polynomials with no symmetry
or parity. e.g.:

exp(x) = 1 + x + x^2 / 2 + x^3 / 6 + x^4 / 24 + x^5 / 120

*/
double evaluate_poly(double x, double *poly, int len)
{
    int i;
    double y = 0.0;
    for (i = 0; i < len; i++) 
    {
        y += pow(x, i) * poly[i];
    }
    return y;
}

/* 
Used for evaluating Taylor Polynomials which present 
some kind of parity, e.g.:

PARITY 0:
    cos(x) = 1 - x^2 / 2 + x^4 / 24 - x^6 / 720 ...

PARITY 1:
    sin(x) = x - x^3 / 6 + x^5 / 120 - x^7 / 5040 ...

This way, with a polynomial of degree n, the iteration
is of length n / 2

*/
double evaluate_poly_w_parity(double x, double *poly, int len, int parity)
{
    int i, exp;
    double y = 0.0;
    for (i = 0; i < len; i++) 
    {
        exp = (2 * i) + parity;
        y += pow(x, exp) * poly[i];
    }
    return y;
}

int magnitude_order(double x) 
{
    double x_prime = fabs(x);
    int magnitude = 0;

    // Loop for x of magnitude greater than 0
    while (x_prime >= 10){
        x /= 10;
        magnitude++;
    }

    // Loop for x of magnitude lower than zero
    while (x < 1){
    x *= 10;
    magnitude--;
    }

    return magnitude;
};