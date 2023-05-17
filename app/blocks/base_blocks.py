'''
Module for basic block classes.

The class hierarchy for blocks is:
Base_block
 ├── Start_block
 └── Variable_block
      ├── Decimal_variable_block
      └── Bool_variable_block

'''

# requirements imports begin {

import typing as _typing


from abc import (
	ABC as _ABC,
	abstractmethod as _abstractmethod,
)
from functools import (
	wraps as _wraps
)

# } requirements imports end


# relative imports begin {

from ..different_modules import (
	exceptions as _exceptions,
)

# } relative imports end



class Base_block(_ABC):
	'''
	The basic abstract class for all blocks

	Block number 100
	'''

	__block_number = 100

	@property
	def block_number(self):
		return self.__block_number


	block_id: str = None
	'id of the block to get it from the graph'

	block_type: str = None
	'block type'

	adjacents: list = None
	'the list of edges in the graph for this block (the graph is unidirectional, but can be cyclic)'

	payload: _typing.Any = None
	'the payload required for the operation of the unit'


	def __init__(
			self, /, block_id: str, block_type: str,
			adjacents: list, payload: _typing.Any,
			*args: _typing.Any, **kwargs: _typing.Any,
		) -> None:
		'''
		:block_id str: id of the block to get it from the graph
		:block_type str: block type
		:adjacents list: the list of edges in the graph for this block (the graph is unidirectional, but can be cyclic)
		:payload _typing.Any: the payload required for the operation of the unit
		:args _typing.Any: arguments for the boot_up method
		:kwargs _typing.Any: arguments for the boot_up method
		'''

		self.block_id = block_id
		self.block_type = block_type
		self.adjacents = adjacents
		self.payload = payload

		if self.boot_up is not super().boot_up:
			self.boot_up(*args, **kwargs)


	@_abstractmethod
	async def signal(self, /, graph: dict, from_block: str, run_time_data: dict) -> str | tuple[str, ...] | None:
		'''
		A special method for a block that receives a signal is obliged to send a signal to another block
		(return the id of this block) or return None if the signal on this block ends

		In case of an error, returns the error code (int)
		'''

		length = len(self.adjacents)
		
		if length == 1:
			return self.adjacents[0]

		elif length != 0:
			return tuple(self.adjacents)


	async def boot_up(self, /, *args: _typing.Any, **kwargs: _typing.Any) -> None:
		'''
		A special method for boot up a block where it is required.
		Here you can insert additional code to initialize the block, for example, to process the payload.
		Called if overridden.

		All extraneous arguments from __init__ will be passed here.
		'''

		raise _exceptions.Method_is_undefined_error('boot_up method cannot be called unless overridden')


class Start_block(Base_block):
	'''
	The block of the beginning, there is in each graph, and only 1

	Block number 101
	'''

	__block_number = 101


	@_wraps(Base_block.signal)
	async def signal(self, /, graph: dict, from_block: str, run_time_data: dict) -> str | tuple[str, ...] | None:
		return Base_block.signal(self, graph, from_block, run_time_data)


class Variable_block(Base_block):
	'''
	Base block, for all variable blocks

	Block number 102
	'''

	__block_number = 102

	variable_type: _typing.Any = None

	def get_variable_value(self, /) -> _typing.Any | int: # Returns int if it raises NameError
		return self.variable_type(self.payload['variable_value'])


	def compatibility_of_variable_name(self, /, run_time_data) -> bool | int: # Returns int if it raises NameError
		'''
		Checking the variable name for type compatibility

		If the variable already exists and its type does not match the new one, there will be an error
		'''

		get_variable = run_time_data.get(self.payload['variable_name'])

		if not get_variable and type(get_variable) != self.variable_type:
			raise NameError

		return True

	def set_variable(self, /, run_time_data, variable_value) -> bool | int: # Returns int if it raises Exception
		run_time_data.update({self.payload['variable_name']: variable_value})

		return True


	@_wraps(Base_block.signal)
	async def signal(self, /, graph: dict, from_block: str, run_time_data: dict) -> str | tuple[str, ...] | None:
		if type(variable_value := self.get_variable_value()) == int: # check: error code or variable value returned
			return variable_value

		if (compatibility := self.compatibility_of_variable_name(run_time_data)) is not True: #check: error code returned or verification was successful
			return compatibility


		if (set_variable_result := self.set_variable(run_time_data, variable_value) is not True):
			return set_variable_result

		return Base_block.signal(self, graph, from_block, run_time_data)


class Decimal_variable_block(Variable_block):
	'''
	A block for a decimal number variable

	Block number 103
	'''

	__block_number = 103


	from decimal import Decimal as _Decimal # limiting the availability area

	variable_type = _Decimal


class Bool_variable_block(Variable_block):
	'''
	A block for a bool value variable

	Block number 103
	'''

	__block_number = 104

	variable_type = bool



