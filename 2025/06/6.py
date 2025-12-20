import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse_silver(input_lines):
	parsed = []
	for line in input_lines:
		parsed.append([i for i in line.split(' ') if i != ''])
	numbers = []
	for i in range(len(parsed[0])):
		numbers.append([int(line[i]) for line in parsed[:-1]])
	signs = parsed[-1]
	return numbers, signs

def _solve(numbers, signs):
	total_result = 0
	for index, problem_numbers in enumerate(numbers):
		if signs[index] == '+':
			result = 0
			for n in problem_numbers:
				result += n
		if signs[index] == '*':
			result = 1
			for n in problem_numbers:
				result *= n
		total_result += result
	return total_result

def silver(input_lines):
	numbers, signs = _parse_silver(input_lines)
	return _solve(numbers, signs)

def _parse_gold(input_lines):
	transposed = []
	for i in range(len(input_lines[0])):
		transposed.append(''.join([input_lines[j][i] for j in range(len(input_lines) - 1)]))
	numbers = []
	current = []
	for column in transposed:
		if column.isspace():
			numbers.append(current)
			current = []
		else:
			current.append(int(column))
	numbers.append(current)
	signs = [i for i in input_lines[-1].split(' ') if i != '']
	return numbers, signs

def gold(input_lines):
	numbers, signs = _parse_gold(input_lines)
	return _solve(numbers, signs)
