'''
Block Execution Engine
'''

# declaring headlines {

class _Executor: pass # Both classes store references to each other (the definition of the header is necessary for the use of annotations)
class Engine: pass

# }


class _Executor:
	_engine: Engine = None
	_current_block: str = None
	_last_block: str = None
	_run_time_data: dict = None


	def __init__(self, engine) -> None:
		self._engine = engine
		self._current_block = 'start_block'
		self._last_block = None
		self._run_time_data = {}


	def __next__(self) -> tuple[str, ...]:
		block = self._engine.graph[self._current_block]

		result = block.signal(self._engine.graph, self._last_block, self._run_time_data)

		if not any(result):
			raise StopIteration

		if not type(result) == int:
			self._current_block = result

		return result


class Engine:
	_graph: dict = None


	@property
	def graph(self) -> dict:
		return self._graph


	def __init__(self, graph: dict) -> None:
		self._graph = graph


	def __iter__(self) -> _Executor:
		return _Executor(self)


