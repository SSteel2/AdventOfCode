import Util.input
import hashlib

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _solve(input_lines, search_string):
	for i in range(1000000000):
		hash_string = hashlib.md5((input_lines[0] + str(i)).encode('utf-8')).hexdigest()
		if hash_string.startswith(search_string):
			return i

def silver(input_lines):
	return _solve(input_lines, '00000')

def gold(input_lines):
	return _solve(input_lines, '000000')
