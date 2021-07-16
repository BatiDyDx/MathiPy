from functools import wraps
from typing import Annotated, Any, Iterable, Union, Callable, FrozenSet, TypeVar

T = TypeVar('T', bound=Any)

def check_bool_input(f: Callable[..., bool]) -> Callable[..., bool]:
	"""
	Decorates a function, and checks when called if the
	inputs are of type bool. If there is any element
	such that is not a boolean, it raises a TypeError.
	"""
	@wraps(f)
	def type_checking_wrapper(*args: bool):
		type_is_bool = lambda x: type(x) is bool
		# Detemine if each input has type bool
		cit = map(type_is_bool, args) # cit stands for correct input type
		# Then, determine if all inputs have type bool
		correct_type = all(cit)
		
		if not correct_type:
			raise TypeError(f'Inputs must be of boolean type, received as input {args}')
		return f(*args)

	return type_checking_wrapper


@check_bool_input
def AND(p: bool, q: bool) -> bool:
	"""
	Conjunction operator used in propositional logic
	"""
	return bool(p and q)


@check_bool_input
def OR(p: bool, q: bool) -> bool:
	"""
	Disjunction operator used in propositional logic
	"""
	return bool(p or q)


@check_bool_input
def NAND(p: bool, q: bool) -> bool:
	"""
	NAND operation is equaivalent to the logic negation
	of an AND operation
	"""
	return not AND(p, q)


@check_bool_input
def XOR(p: bool, q: bool) -> bool:
	"""
	XOR is the exclusive OR operation. Evaluates to
	True if both p and q have different values
	"""
	return p is not q 


@check_bool_input
def imply(p: bool, q: bool) -> bool:
	"""
	Implication logic operation.
	p --> q <==> not p or q	
	If p, the hypothesis, is False, the
	implication is True. If the hypothesis is True, 
	then the implication is True only if the 
	conclusion, q, is True
	"""
	return OR(not p, q)


@check_bool_input
def iff(p: bool, q: bool) -> bool:
	"""
	If and only if operation.
	p <--> q <==> (p --> q) and (q --> p)

	The biconditional or iff is true
	when p and q are both True or False.
	This is, if the hypothesis is True,
	then the conclusion is True, meanwhile if
	the hypothesis is False the conclusion is False
	"""
	return p is q


def exists(U: FrozenSet[T], prop: Callable[[T], bool], *vals) -> bool:
	"""
	Given an Universe set, checks if there is an
	element in it such that prop evaluates to True.
	This is, it checks if there exists some value in
	the Universe that satisfies the proposition
	"""
	for x in U:
		if prop(x, *vals): 
			return True	
	return False


def forall(U: FrozenSet[T], prop: Callable[[T], bool], *vals) -> bool:
	"""
	Given an Universe set, checks if all elements
	in it satisfy the proposition
	"""
	for x in U:
		if not prop(x, *vals):
			return False
	return True


def set_is_contained(set1: FrozenSet[T], set2: FrozenSet[T], strict: bool = False) -> bool:    
	"""
	Checks whether set1 is contained in set2.
	:param strict: If True (defaults to False), a strict contention
	is done. This means that set1 must be contained in set2 while being
	different from set2 to evaluate to True

	Mathematically, the operation done is:
	A ⊆ B if strict is False, else A ⊂ B
	"""
	
	result: bool = bool(set1 & set2 == set1)
	if strict:
		unequal_sets: bool = bool(set1 != set2)
		return result and unequal_sets
	return result


def set_contains(set1: FrozenSet[T], set2: FrozenSet[T], strict: bool = False) -> bool:
	"""
	Evaluates to True if the first set contains the second one.
	Equivalent to set_is_contained(set2, set1)
	:param strict: If True (defaults to False), a strict contention
	is done. This means that set1 must contain set2 while being
	different from set2 to evaluate to True

	Mathematically, the operation done is:
	A ⊇ B if strict is False, else A ⊃ B
	"""
	return set_is_contained(set2, set1, strict)


def simetric_diff(set1: FrozenSet[T], set2: FrozenSet[T]) -> FrozenSet[T]:
	"""
	Simetric difference operation between sets.
	Simetric difference is defined as:
	- (A - B) ∪ (B - A)
	- (A ∪ B) - (A ∩ B)

	The simmetric difference between two sets is
	the set of elements that belong to either of them,
	but not both
	"""
	return (set1 | set2) - (set1 & set2)


def test_proposition(P: Callable[..., bool], n: int) -> None:
	"""
	Given a function that acts as a logical proposition,
	it prints all possible combinations of inputs.
	Number of possible inputs is determined by 2^n, where
	n is the number of atomic propositions P depends on.
	The number of inputs n must be provided.
	>>> test_proposition(AND, 2)
	None

	Prints on terminal:
	(False, False): False
	(False, True): False
	(True, False): False
	(True, True): True
	"""
	if n < 1:
		raise ValueError(f'n must be greater or equal to 1, received {n}')

	def test_prop_wrapper(P, n, *args):
		if n == 1:
			for i in range(2):
				truth_vals : tuple[bool] = (*args, bool(i))
				print(truth_vals, ': ', P(*truth_vals))
			return

		for i in range(2):
			test_prop_wrapper(P, n - 1, *args, bool(i))

	test_prop_wrapper(P, n)

