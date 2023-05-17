"""
Module for local app exceptions.

The class hierarchy for local app exceptions is:
Base_app_exception
└──Method_is_undefined_error
"""


class Base_app_exception(Exception):
	"""
	Parent exclusion of all app exceptions
	"""
	pass


class Method_is_undefined_error(Base_app_exception):
	"""
	An exception that must be thrown when calling a method or function
	that is not defined to explicitly specify it
	"""
	pass