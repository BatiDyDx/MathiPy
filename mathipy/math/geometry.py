from collections import namedtuple
import numpy as np
from mathipy.math.linalg import Vector
from ..config import Real


# Point is an abstract class, from where N dimensional points
# subclasses can be instantiated.

# Point2D and Point3D are NamedTuples, inheriting from the abstract base class
Point_2D = namedtuple("Point2D", ["x", "y"])
Point_3D = namedtuple("Point3D", ["x", "y", "z"])


class Line:
	def __init__(self, a: Real, b: Real, c: Real) -> None:
		self.a = a
		self.b = b
		self.c = c

	def get_normal_equation(self) -> 'Line':
		pass

	@staticmethod
	def line_from_vector_eq(P: Point_2D, u: Vector):
		"""Get a line from its vector equation"""
		pass

	@staticmethod
	def line_from_parametric_eq(x_0: Real, y_0: Real, u_0: Real, u_1: Real):
		"""Get a line from its parametric equation"""
		pass

	@staticmethod
	def line_from_explicit_eq(m: Real, h: Real):
		"""Get a line from its explicit equation"""
		pass

	@staticmethod
	def line_from_segmentary_eq():
		"""Get a line from its segmentary equation"""
		pass

class Plane:
	def __init__(self, a: Real, b: Real, c: Real, d: Real) -> None:
		self.a = a
		self.b = b
		self.c = c
		self.d = d

