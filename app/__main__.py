"""
The application startup file must be executed from the entry point

Allows you to run the project in all possible modes:
-t test_mode
-r run_mode
"""


import argparse as _argparse


from asyncio import run as _run
from datetime import datetime as _datetime



parser = _argparse.ArgumentParser()

parser.add_argument('-t', action='store_true')
parser.add_argument('-r', action='store_true')


async def run_tests():
	from .tests import start_testing

	await start_testing()


async def run_host():
	pass


async def main():
	start_time = _datetime.now()


	args = vars(parser.parse_args())

	if args['t']:
		await run_tests()

	elif args['r']:
		await run_host()

	else:
		print('You did not specify any 1 argument')

	end_time = _datetime.now()

	print(f'The program has finished its work in {end_time - start_time}')


_run(main())