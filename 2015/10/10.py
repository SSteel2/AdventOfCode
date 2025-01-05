import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _look_and_say(line):
	result = []
	current_digit = line[0]
	current_count = 1
	for i in line[1:]:
		if i == current_digit:
			current_count += 1
		else:
			result.extend([str(current_count), current_digit])
			current_digit = i
			current_count = 1
	result.extend([str(current_count), current_digit])
	return result

def _solve(input_lines, repetitions):
	current = input_lines[0]
	for i in range(repetitions):
		current = _look_and_say(current)
	return len(current)	

def silver(input_lines):
	return _solve(input_lines, 40)

def gold(input_lines):
	return _solve(input_lines, 50)
