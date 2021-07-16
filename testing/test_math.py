import unittest
import mathipy as mpy
from mathipy.math._math import *
import numpy as np

class MathTest(unittest.TestCase):
    
    # Significant places for when comparing
    # with assertAlmostEqual
    sig_places = 10

    @classmethod
    def setUpClass(cls) -> None:
        return super().setUpClass()
    
    @classmethod
    def tearDownClass(cls) -> None:
        return super().tearDownClass()

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass
    
    def test_Infinite(self):
        self.assertEqual(mpy.Infinite(), - mpy.Infinite(sign=False))
        self.assertEqual(mpy.Infinite(), mpy.Infinite() + 10e10)
        self.assertEqual(-mpy.Infinite(), 10e7 - mpy.Infinite())

    def test_pascal_triangle(self):
        pass

    def test_summation(self):
        a = 4
        r = 3
        arithmetic_progression = lambda n: (2 * a + (n - 1) * r) * (n / 2)
        geometric_progression = lambda n: a * (r ** (n + 1) - 1) / (r - 1)
        k = 55
        arithmetic_prog_test = mpy.summation(lambda n: a + n * r, k, 0)
        geometric_prog_test = mpy.summation(lambda n: a * (r ** n), k, 0)
        self.assertEqual(arithmetic_prog_test, arithmetic_progression(k))
        self.assertEqual(geometric_prog_test, geometric_progression(k))
        self.assertEqual(mpy.summation(lambda n: n, 1, 5), 0)

    def test_productory(self):
        k_0 = 30
        self.assertAlmostEqual(
            mpy.productory(lambda n: 1 - n, k_0, 2)
            (1 / k_0)
        )

        k_1 = 25
        x = np.random.randint(100, size=k_1)
        y = np.random.randint(100, size=k_1)
        self.assertEqual(
            mpy.productory(
                lambda i: x[i-1] * y[i-1],
                k_1,
                1),
            mpy.productory(lambda i: x[i-1], k_1, 1) * mpy.productory(lambda i: y[i-1], k_1, 1)
        )

        k_2 = 18
        z = np.random.randint(100, size=k_2)
        c = 3
        self.assertEqual(
            mpy.productory(lambda i: c * z[i-1], k_2, 1),
            c ** k_2 * mpy.productory(lambda i: z[i-1], k_2, 1)
        )


    def test_gcd(self):
        self.assertEqual(gcd(100, 10), 10)
        self.assertEqual(gcd(250, 3), 1)
        self.assertEqual(gcd(-18, 9), 9)

    def test_lcm(self):
        self.assertEqual(lcm(2, 6), 6)
        self.assertEqual(lcm(8, 6), 24)

    def test_sci_notation(self):
        pass

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

    def test_differential(self):
        pass

    def test_sin(self):
        self.assertAlmostEqual(mpy.sin(1.345), np.sin(1.345), self.sig_places)
        self.assertEqual(mpy.sin(mpy.pi), 1)
        self.assertEqual(mpy.sin(-mpy.tau), 0)

    def test_cos(self):
        self.assertEqual(mpy.cos(0), 1)
        self.assertEqual(mpy.cos(pi_2), 1)
        self.assertAlmostEqual(mpy.cos(-mpy.pi / 4), mpy.srqt2 / 2, self.sig_places)

    def test_tan(self):
        self.assertAlmostEqual(mpy.tan(mpy.pi / 2), 1, 3)
        self.assertAlmostEqual(mpy.tan(mpy.pi), 0, 3)
        self.assertAlmostEqual(mpy.tan((2/3) * mpy.pi) -mpy.sqrt(3), self.sig_places)
        self.assertEqual(mpy.tan(0), 0)
        self.assertEqual(mpy.tan(mpy.pi_2), mpy.Infinite())
        
    def test_arcsin(self):
        self.assertEqual(mpy.arcsin(0), 0)
        self.assertAlmostEqual(mpy.arcsin(1), mpy.pi_2, self.sig)
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

    def test_root_n(self):
        self.assertEqual(mpy.root_n(27, 3), 3)
        self.assertEqual(mpy.root_n(-27.0, 3), -3.0)
        self.assertIs(mpy.root_n(-16, 4, False), np.nan)
        self.assertIs(mpy.root_n(-16, 4, False), 2j)

    def test_sqrt(self):
        self.assertAlmostEqual(mpy.sqrt(2), mpy.srqt2, self.sig_places)
        self.assertEqual(mpy.srqt(-4, True), 2j)
        self.assertIs(mpy.sqrt(-4, False), np.nan)

if __name__ == '__main__':
    MathTest.main()
