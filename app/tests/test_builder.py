from types import FunctionType as _FunctionType


from ..blocks import (
	base_blocks as base_blocks,
	Engine as _Engine,
)




class Tests_group:
	name: str = None
	description: str = None
	tests: list = None

	def __init__(self, /, name, description=None):
		self.name = name
		self.description = description
		self.tests = []


	def __call__(self, func: _FunctionType = None, /, name: str = None, description: str = None) -> _FunctionType:
		def wrapper(func):
			func.name = name if name else func.__name__
			func.description = description
			self.tests.append(func)

			return func

		return wrapper(func) if func else wrapper

	def run_tests(self, /):
		for test in self.tests:
			test()


class _Tests:
	name: str = None
	description: str = None
	tests_groups: dict = None


	def __init__(self, /, name=None, description=None):
		self.name = name
		self.description = description
		self.tests = []


	def __getitem__(self, value):
		return self.tests_groups[value]


	def create_group(self, /, name, description=None) -> Tests_group:
		new_tests_group = Tests_group(name, description)

		self.tests_groups[name] = new_tests_group

		return new_tests_group.run_tests()


	def start_testing(self, /):
		for tests_group in self.tests_groups:
			tests_group.


secure_eval_tests_group = _Tests()

@secure_eval_tests_group
def test_1():
	print(1)


@secure_eval_tests_group
def test_3():
	print(3)


@secure_eval_tests_group
def test_2():
	print(2)


async def start_testing():
	secure_eval_tests_group.start_testing()

