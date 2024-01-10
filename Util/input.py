import os

def LoadInput(filename):
	input_lines = []
	with open(filename, 'r') as input_file:
		for line in input_file:
			input_lines.append(line.removesuffix('\n'))
	return input_lines

def GetInputFile(current_file, input_filename):
	return os.path.join(os.path.dirname(current_file), input_filename)

def ParseInputLines(input_lines, parse_function):
	parsed = []
	for line in input_lines:
		parsed.append(parse_function(line))
	return parsed
