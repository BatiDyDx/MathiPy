import unittest
import numpy as np
from mathipy.quaternion import Quaternion


class QuaternionTest(unittest.TestCase):

    def setUp(self) -> None:
        self.p = Quaternion(*np.random.randint(100, size=4))
        self.q = Quaternion(*np.random.randint(100, size=4))

    def test_addition(self):
        r = (a + b for a,b in zip(self.p.ordered_pair(), self.p.ordered_pair()))
        self.assertEqual(self.p + self.q, Quaternion(*r))

    def test_product(self):
        self.assertNotEqual(self.p * self.q, self.q * self.p)
        self.assertEqual(Quaternion(1, -1, 3.5, 5.3) * 2, Quaternion(2, -2, 7.0, 10.6))
        p, q = Quaternion(2, 3, 1, -6), Quaternion(4, 3, -5, 1)
        self.assertEqual(p * q, Quaternion(3, 49, 9, -4))

    def test_equal(self):
        self.assertEqual(self.p, self.p)
        self.assertNotEqual(self.p, self.p + Quaternion(1, -3, 2, 1))
        self.assertEqual(Quaternion(1, 0, 0, 0), 1)

if __name__ == '__main__':
    QuaternionTest.main()