import string as _string




good_operations_symbols = '()*/+-.<>=%'
good_letters = _string.ascii_letters + _string.digits + good_operations_symbols + '_'
good_letters_without_letters = _string.digits + good_operations_symbols


def secure_eval(line, run_time_data=None):
	'''
	Safe and secure eval
	'''

	if run_time_data is None:
		run_time_data = {}


	# breaks syntax, but not expressions
	line = line.replace(' ', '')
	line = line.replace('\n', '')


	# breaks if there are bad characters that are not in the expressions. For example, '['
	for letter in line:
		if letter not in good_letters:
			raise Exception


	# breaks function calls, for example, func()
	splited_opening_parenthesis = line.split('(')
	if len(splited_opening_parenthesis) != 1:
		for piece in splited_opening_parenthesis:
			if piece != '' and piece[-1] not in good_operations_symbols:
				raise Exception


	# breaks access to an object attribute
	splited_point = line.split('.')
	if len(splited_point) != 1:
		for piece in splited_point[:-1]:
			if piece[-1] not in _string.digits:
				raise Exception

		if splited_point[-1][0] not in _string.digits:
			raise Exception


	# breaks the use of any local variable except strictly defined ones
	condition = False
	word = ''
	for letter in line:
		if not condition and word:
			if word not in run_time_data:
				raise Exception

			word = ''

		if letter not in good_letters_without_letters:
			condition = True
			word += letter

		else:
			condition = False

	else:
		if word and word not in run_time_data:
			raise Exception


	# breaks direct access to built-in objects
	return eval(line, {"__builtins__": None}, run_time_data)



print(secure_eval('5 > a', {'a': 2}))