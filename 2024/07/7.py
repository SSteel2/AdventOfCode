import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parseLine(line):
	numbers = [int(i) for i in line.split(' ')[1:]]
	goal = int(line.split(': ')[0])
	return goal, numbers

def __product(numbers):
	prod = 1
	for i in numbers:
		prod *= i
	return prod

def _is_number_matching_goal(goal, numbers, different_operations):
	if different_operations == 2:
		max_value = __product(numbers)
		if max_value < goal:
			return False

	max_permutations = different_operations ** (len(numbers) - 1)
	for operation_permutation in range(max_permutations):
		actual_sum = numbers[0]
		current_operation_permutation = operation_permutation
		for index, number in enumerate(numbers[1:]):
			current_operation = current_operation_permutation % different_operations
			current_operation_permutation //= different_operations
			if current_operation == 0:
				actual_sum *= number
			elif current_operation == 1:
				actual_sum += number
			elif current_operation == 2:
				actual_sum = int(str(actual_sum) + str(number))
			if actual_sum > goal:
				break
		if actual_sum == goal:
			return True
	return False

def _solution(input_lines, different_operations):
	tasks = Util.input.ParseInputLines(input_lines, _parseLine)
	score = 0
	for task in tasks:
		if _is_number_matching_goal(task[0], task[1], different_operations):
			score += task[0]
	return score

def silver(input_lines):
	return _solution(input_lines, 2)

def gold(input_lines):
	return _solution(input_lines, 3)
