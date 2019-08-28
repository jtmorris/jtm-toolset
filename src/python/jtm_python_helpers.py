"""Python Tools & Helpers

This script contains a collection of tools and helper functions/classes
for using Python. It is intended for use with Python 3, but should be
fairly sub-version agnostic.
"""

import time

def init_list_with_values(list_length: int, init_value):
	"""Return a pre-initialized list.

	Returns a list of length list_length with each element equal to
	init_value. init_value must be immutable (e.g. an int is okay; a
	dictionary is not), or the resulting list will be a list of
	references to same object (e.g. retlist[0] and retlist[1] would
	point to the same object and manipulating
	one would change it for the other).

	Args:
		list_length (int):	The number of elements in the resulting
						list.
		init_value:		A immutable value to initialize each list
						element to.

	Returns:
		list:	A list of length list_length with each element
				initialized to init_value

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

	Outputs the content of the passed variable to the console. This is
	effectively an alias for pprint() from the pprint module. Useful
	for dirty debugging to see what is in a variable.

	Note that you would be better served, performance wise, to put
	'from pprint import pprint as var_dump' in your code, rather than
	use this function as it imports pprint each time (a small
	performance hit, with Python's caching, but a hit nonetheless).
	This function simply makes one off debug checks easier if this
	module is already loaded, as another import statement isn't needed
	first.

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


class Performance_Monitor:
	"""A simple execution time performance monitor.

	Used to record the execution time of a block of code.
	When instantiated, time is recorded. When code you
	wish to profile is complete, call the stop member
	function. Execution time can be retrieved in various
	units, with or without a readable string accompaniement.

	Examples:
		>>> # Start measuring
		>>> P = Performance_Monitor()
		>>> # Execute code you want measured here.
		>>> t_in_nanoseconds = P.stop()
		>>> # Measuring has stopped
		>>> isinstance(t_in_nanoseconds, int)
		True
		>>>
		>>> # Time can also be retrieved with get_time()
		>>> t = P.get_time("seconds")
		>>> isinstance(t, float)
		True
		>>> # A human readable version can be retrieved with
		>>> # get_readable_time()
		>>> P.get_readable_time("seconds").split()[-1] == "seconds"
		True
	"""

	def __init__(self):
		"""Initalizes an object and starts a timer."""
		self.start()

	def start(self):
		"""Start and or reset the timer.

		Starts the timer by clearing out stop_time and putting current
		time in start_time. Only one timer is tracked at a time, per
		object, so calling start more than once resets the timer each
		time. The timer is automatically started at instantiation, so
		this function need not be manually called in most situations.
		Just instantiate an object at the desired time instead.
		"""
		self.start_time = time.perf_counter_ns()
		self.stop_time = None
	def quiet_stop(self):
		"""Stores the current time as stop time for later processing.

		Stores the time, in nanoseconds, to the object's stop_time
		member property for later processing and retrieval. Only
		one stop time is stored, so if called multiple times, only
		the latest will be stored for processing.

		Examples:
			>>> P = Performance_Monitor()
			>>> # Execute code you want measured here.
			>>> P.quiet_stop()
			>>> P.get_readable_time("seconds").split()[-1] == "seconds"
			True
		"""
		self.stop_time = time.perf_counter_ns()
	def stop(self, units: str = "nanoseconds"):
		"""Stores current time as stop time and returns elapsed time.

		Same as quiet_stop(), except afterwards it returns the time
		elapsed in the specified units.

		Args:
			units (str):	The units of time of return value. Will be
						passed directly to get_time(), and must
						conform to its units rules.
		Returns:
			int or float:	The elapsed time in the specified units.

		Examples:
			>>> P = Performance_Monitor()
			>>> # Execute code you want to measure here.
			>>> t_in_nanoseconds = P.stop()
			>>> isinstance(t_in_nanoseconds, int)
			True
		"""

		self.quiet_stop()

		return self.get_time(units)


	def stop_and_spit(self, units: str = "milliseconds",
				   context: str = None, prefix: str = "[PERF] ",
				   postfix: str = ""):
		"""Stores current time as stop time and prints elapsed time.

		Same as quiet_stop(), except afterwards it prints the time
		elapsed with an optional prefix and function name prepended,
		and an optional postfix appended. If calling function is None,
		the function in which stop_and_spit() is called will be
		automatically determined and used. If you want no function,
		specify an empty string.

		Args:
			units (str):	The units of time of return value. Will be
						passed directly to get_time(), and must
						conform to its units rules.
			context (str):	A string to follow the prefix.
						Intended to hold contextual information
						explaining what is being measured.
						Default is None. If None, calling
						function will be auto determined.
			prefix (str):	A string to prepend to the output. Default
						is "[PERF] ".
			postfix (str):	A string to append to the output. Default
						is empty string "".

		Examples:
			>>> P = Performance_Monitor()
			>>> # Execute code you want to measure here.
			>>> P.stop_and_spit() # doctest: +ELLIPSIS
			[PERF] [<module>] ... milliseconds

			>>> def sastest():
			... 	P = Performance_Monitor()
			...	# Execute code you want to measure here.
			... 	P.stop_and_spit("nanoseconds")
			>>> sastest() # doctest: +ELLIPSIS
			[PERF] [sastest()] ... nanoseconds
		"""
		# If no function string was provided, get one.
		if context == None:
			try:
				import inspect
				context = str(inspect.stack()[1].function)
				if context != "<module>":
					context = context + "()"
				context = "[" + context + "] "
			except:
				context = ""

		self.quiet_stop()

		print(prefix + context + self.get_readable_time(units, 1) +
		      postfix)



	def get_time(self, units: str = "microseconds"):
		"""Gets the time between start and stop.

		Calculated the time between clock start, triggered by class
		instantiation, or by calling the start() member function, and
		the clock end, triggered automatically, if clock hasn't been
		stopped yet, or manually by calling the stop() member function
		first.

		Time is recorded in nanoseconds. If requested units are
		nanoseconds, an integer is returned. Otherwise, a float is
		returned.

		Args:
			units (str):	The units of time of return value. Default
						is microseconds. Options are "minutes",
						"seconds", "milliseconds", "microseconds",
						and "nanoseconds".

		Returns:
			int or float:	If units are nanoseconds, the maximum
						available precision, an int is returned.
						Otherwise, a float is returned.

		Raises:
			ValueError: 	If 'units' argument does not contain a
						string with one of the acceptable unit
						formats (minutes, seconds, milliseconds,
						microseconds, or nanoseconds)

		Examples:
			>>> P = Performance_Monitor()
			>>> # Execute code you want to measure here.
			>>> t_in_ns	= P.stop()
			>>> t_in_min	= P.get_time("minutes")
			>>> t_in_s	= P.get_time("seconds")
			>>> t_in_ms	= P.get_time("milliseconds")
			>>> t_in_mus	= P.get_time("microseconds")
			>>> t_in_ns	= P.get_time("nanoseconds")
			>>> t_in_prs	= P.get_time("parsecs")
			Traceback (most recent call last):
			 ...
			ValueError: Invalid units type requested (parsecs).
		"""

		if not self.stop_time:
			self.stop()

		# Implement a rough approximation of switch/case statement
		# Define cases
		cases = {
			"minutes": 		lambda ns : ns / 60000000000.0,
			"seconds": 		lambda ns : ns / 1000000000.0,
			"milliseconds":	lambda ns : ns / 1000000.0,
			"microseconds":	lambda ns : ns / 1000.0,
			"nanoseconds":		lambda ns : ns
		}
		# Pose switch
		if units in cases:
			# Choose correct case
			return cases[units]((self.stop_time - self.start_time))
		# Default
		else:
			raise ValueError("Invalid units type requested (" +
			                 units + ").")

	def get_readable_time(self, units: str = "microseconds",
		                 precision: int = None):
		"""Gets the time between start and stop, with units included.

		A wrapper around the get_time() member function that returns
		a string with the units appended, for readability, rather than
		just the number. The number is rounded and truncated to the
		number of decimal places specified in 'precision'.

		Args:
			units (str):	The units of time of return value. Default
						is microseconds. Options are "minutes",
						"seconds", "milliseconds", "microseconds",
						and "nanoseconds".
			precision (int):	The number of decimal places to show,
							if applicable.

		Returns:
			str:	A readable representation of the time, with units.

		Raises:
			ValueError: 		If 'units' argument does not contain
							a string with one of the acceptable
							unit formats (minutes, seconds,
							milliseconds, microseconds, or
							nanoseconds)

		Examples:
			>>> P = Performance_Monitor()
			>>> # Execute code you want to measure here.
			>>> t_in_ns_fs	= P.stop()
			>>> (P.get_readable_time("minutes").split()[-1] ==
			... "minutes")
			True
			>>> (P.get_readable_time("seconds").split()[-1] ==
			... "seconds")
			True
			>>> (P.get_readable_time("milliseconds").split()[-1] ==
			... "milliseconds")
			True
			>>> (P.get_readable_time("microseconds").split()[-1] ==
			... "microseconds")
			True
			>>> (P.get_readable_time("nanoseconds").split()[-1] ==
			... "nanoseconds")
			True
			>>> (P.get_readable_time("parsecs").split()[-1] ==
			... "parsecs")
			Traceback (most recent call last):
			 ...
			ValueError: Invalid units type requested (parsecs).
			>>>
			>>> # Now let's examine decimal point handling. Let's
			>>> # get a two decimal readable time and verify.
			>>> t_in_min = P.get_readable_time("minutes", 2)
			>>> #	Split at decimal, keep what's after it
			>>> adp = t_in_min.split(".")[1]
			>>> #	Split at space, to seperate fraction and units
			>>> frac = adp.split()[0]
			>>> unts = adp.split()[-1]
			>>> # Fraction should be two decimal places.
			>>> len(frac) == 2
			True
			>>> # Units should be minutes
			>>> unts == "minutes"
			True
		"""
		if precision != None:
			t = round(self.get_time(units), precision)
			return ("{0:.{prec}f}".format(t, prec=precision) + " " +
			        units)
		else:
			return str(self.get_time(units)) + " " + units






# Activate doctests for when this file is run.
if __name__ == "__main__":
    import doctest
    doctest.testmod()