import os

def LoadInput(filename):
	input_lines = []
	with open(filename, 'r') as input_file:
		for line in input_file:
			input_lines.append(line)
	return input_lines

def GetInputFile(current_file, input_filename):
	return os.path.join(os.path.dirname(current_file), input_filename)