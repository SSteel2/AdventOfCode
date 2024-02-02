import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _solve(line, marker_length):
	for i in range(len(line)):
		unique = set()
		for j in range(marker_length):
			unique.add(line[i + j])
		if len(unique) == marker_length:
			return i + marker_length

def silver(input_lines):
	return _solve(input_lines[0], 4)

def gold(input_lines):
	return _solve(input_lines[0], 14)
