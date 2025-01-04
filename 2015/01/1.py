import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def silver(input_lines):
	opening = input_lines[0].count('(')
	closing = input_lines[0].count(')')
	return opening - closing

def gold(input_lines):
	current_floor = 0
	for i, instruction in enumerate(input_lines[0]):
		if instruction == '(':
			current_floor += 1
		elif instruction == ')':
			current_floor -= 1
		if current_floor == -1:
			return i + 1
