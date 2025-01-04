import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parseLine(line):
	return [int(i) for i in line.split('x')]

def _solve(input_lines, calculation_function):
	dimension_list = Util.input.ParseInputLines(input_lines, _parseLine)
	total = 0
	for dimensions in dimension_list:
		dimensions.sort()
		total += calculation_function(dimensions)
	return total	

def silver(input_lines):
	return _solve(input_lines, lambda x: x[0] * x[1] * 3 + x[0] * x[2] * 2 + x[1] * x[2] * 2)

def gold(input_lines):
	return _solve(input_lines, lambda x: x[0] * 2 + x[1] * 2 + x[0] * x[1] * x[2])
