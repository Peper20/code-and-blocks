'''
Module for basic block classes.

The class hierarchy for blocks is:
Base_block
└──Start_block
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

	@_wraps(Base_block.signal)
	async def signal(self, /, graph: dict, from_block: str, run_time_data: dict) -> str | tuple[str, ...] | None:
		return Base_block.signal(self, graph, from_block, run_time_data)


class Decimal_variable_block(Base_block):
	'''
	Block for creating or updating the value of a variable

	Block number 102
	'''

	from decimal import Decimal as _Decimal # limiting the availability area

	@_wraps(Base_block.signal)
	async def signal(self, /, graph: dict, from_block: str, run_time_data: dict) -> str | tuple[str, ...] | None:
		run_time_data[self.payload['variable_name']] = self._Decimal(self.payload['variable_value'])

		return Base_block.signal(self, graph, from_block, run_time_data)
