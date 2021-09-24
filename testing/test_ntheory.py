import math
import mathipy as mpy
from mathipy.math.ntheory import *
import numpy as np

#TODO
#Migrate testing to pytest

# Significant places for when comparing
# with assertAlmostEqual
sig_places = 10
def test_Infinite():
    assert Infinite() == -Infinite(sign=False)
    assert Infinite() == Infinite() + 10e10
    assert -Infinite() == 10e7 - Infinite()

def test_pascal_triangle():
    pass



def test_gcd(self):
    self.assertEqual(gcd(100, 10), 10)
    self.assertEqual(gcd(250, 3), 1)
    self.assertEqual(gcd(-18, 9), 9)

def test_lcm(self):
    self.assertEqual(lcm(2, 6), 6)
    self.assertEqual(lcm(8, 6), 24)


def test_fibonacci(self):
    self.assertEqual(fibonacci(1), 1)
    self.assertEqual(fibonacci(3), 5)

    with self.assertRaises(TypeError):
        fibonacci(1.5)
        fibonacci(3.0)

def test_fibonacci_seq(self):
    seq1 : list[int] = list(fibonacci_seq(5))
    seq2 : list[int] = list(fibonacci_seq(10))

    self.assertEqual(seq1, [0, 1, 1, 2, 3])
    self.assertEqual(seq2, [0, 1, 1, 2, 3, 5, 8, 13, 21, 34])     

def test_index_of_fib(self):
    self.assertEqual(index_of_fib(5), 6)
    self.assertEqual(index_of_fib(55), 11)
    self.assertEqual(index_of_fib(7), None)

def test_abs(self):
    self.assertEqual(mpy.abs(-100), 100)
    self.assertEqual(mpy.abs(3 + 4j), 5)
    self.assertAlmostEqual(mpy.abs(1 + 1j), mpy.sqrt(2), self.sig_places)

def test_factorial(self):
    self.assertEqual(factorial(5), 120)
    self.assertEqual(factorial(0), 1)

    with self.assertRaises(ValueError, TypeError):
        factorial(3.5)
        factorial(-1)

def test_subfactorial(self):
    self.assertEqual(subfactorial(16), 7697064251745)
    self.assertEqual(subfactorial(1), 0)
    self.assertEqual(subfactorial(0), 1)

    with self.assertRaises(ValueError, TypeError):
        subfactorial(-1)
        subfactorial(-4.1)


def test_summation():
    a = 4
    r = 3
    k = 55
    arithmetic_prog_test = summation(lambda n: a + n * r, k, 0)
    geometric_prog_test = summation(lambda n: a * (r ** n), k, 0)
    assert arithmetic_prog_test == arithmetic_prog(k)
    assert geometric_prog_test == geometric_prog(k)
    assert summation(lambda n: n, 1, 5) == 0

def test_productory():
    k_0 = 30
    assert productory(lambda n: 1 - n, k_0, 2) == (1 / k_0)

    k_1 = 25
    x = np.random.randint(100, size=k_1)
    y = np.random.randint(100, size=k_1)
    
    prod1 = productory(lambda i: x[i-1] * y[i-1], k_1, 1)
    prod2 = productory(lambda i: x[i-1], k_1, 1) * productory(lambda i: y[i-1], k_1, 1)
    assert prod1 == prod2

    k_2 = 18
    z = np.random.randint(100, size=k_2)
    c = 3
    assert productory(lambda i: c * z[i-1], k_2, 1) == c ** k_2 * productory(lambda i: z[i-1], k_2, 1)

def test_differential():
    pass

def test_sin(self):
    self.assertAlmostEqual(mpy.sin(1.345), np.sin(1.345), self.sig_places)
    self.assertEqual(mpy.sin(mpy.pi), 1)
    self.assertEqual(mpy.sin(- math_constants['tau']), 0)

def test_cos(self):
    self.assertEqual(mpy.cos(0), 1)
    self.assertEqual(mpy.cos(math_constants['pi/2']), 0)
    self.assertAlmostEqual(mpy.cos(-mpy.pi / 4), mpy.sqrt2 / 2, self.sig_places)

def test_tan(self):
    self.assertAlmostEqual(mpy.tan(mpy.pi / 2), 1, 3)
    self.assertAlmostEqual(mpy.tan(mpy.pi), 0, 3)
    self.assertAlmostEqual(mpy.tan((2/3) * mpy.pi) -math.sqrt(3), self.sig_places)
    self.assertEqual(mpy.tan(0), 0)
    self.assertEqual(mpy.tan(math_constants['pi/2']), Infinite())

def test_arcsin(self):
    self.assertEqual(mpy.arcsin(0), 0)
    self.assertAlmostEqual(mpy.arcsin(1), math_constants['pi/2'], self.sig)
    self.assertAlmostEqual(mpy.arcsin(-mpy.srqt2 / 2), -mpy.pi / 4, self.sig_places)

def test_arccos(self):
    pass

def test_arctan(self):
    pass

def test_cosh(self):
    pass

def test_sinh(self):
    pass

def test_tanh(self):
    pass

def test_cosec(self):
    pass

def test_sec(self):
    pass

def test_cotan(self):
    pass

def test_cosech(self):
    pass

def test_sech(self):
    pass

def test_cotanh(self):
    pass

def test_ln(self):
    pass

def test_log(self):
    pass


if __name__ == '__main__':
    pass