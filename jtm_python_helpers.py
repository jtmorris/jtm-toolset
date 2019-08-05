def init_list_with_values(list_length: int, init_value):
	"""Return a pre-initialized list.

	Returns a list of length list_length with each element equal to init_value.
	init_value must be immutable (e.g. an int is okay; a dictionary is not),
	or the resulting list will be a list of references to same object (e.g. 
	retlist[0] and retlist[1] would point to the same object and manipulating
	one would change it for the other).

	Args:
		list_length (int):	The number of elements in the resulting list.
		init_value:		A immutable value to initialize each list element to.

	Returns:
		list: A list of length list_length with each element initialized to init_value

	Examples:
		>>> init_list_with_values(3, 0) 
		[0, 0, 0]
		>>> init_list_with_values(5, "Cookies")
		['Cookies', 'Cookies', 'Cookies', 'Cookies', 'Cookies']
		>>> init_list_with_values(2, (1, 2, 3))
		[(1, 2, 3), (1, 2, 3)]
		>>> init_list_with_values(2, {"foo": "bar"})
		[{'foo': 'bar'}, {'foo': 'bar'}]
	"""
	
	return [init_value] * list_length

def var_dump(the_var):
	"""Rough equivalent to PHP's var_dump() function.

	Outputs the content of the passed variable to the console. This is effectively an
	alias for pprint() from the pprint module. Useful for dirty debugging to see what is in
	a variable. 
	
	Note that you would be better served, performance wise, to put 'from pprint import pprint as var_dump' 
	in your code, rather than use this function as it imports pprint each time (a small performance hit, 
	with Python's caching, but a hit nonetheless). This function simply makes one off debug checks easier
	if this module is already loaded, as another import statement isn't needed first.

	Args:
		the_var:	A variable to "dump" to the console.

	Examples:
		>>> var_dump(5)
		5
		>>> var_dump("Cookies")
		'Cookies'
		>>> var_dump({"foo": "bar", "bar": "foo"})
		{'bar': 'foo', 'foo': 'bar'}
		>>> var_dump(('a', 'b'))
		('a', 'b')
	"""

	from pprint import pprint
	
	pprint(the_var)



if __name__ == "__main__":
    import doctest
    doctest.testmod()