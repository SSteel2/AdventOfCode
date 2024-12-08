import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parseLine(line):
	numbers = [int(i) for i in line.split(' ')[1:]]
	goal = int(line.split(': ')[0])
	return goal, numbers

def _remove_concatennation(goal, number):
	while number > 0:
		if goal % 10 == number % 10:
			goal //= 10
			number //= 10
		else:
			return None
	return goal

def _is_number_matching_goal(goal, numbers, different_operations):
	if len(numbers) == 0 and goal == 0:
		return True
	elif (len(numbers) > 0 and goal <= 0) or (len(numbers) == 0 and goal != 0):
		return False

	if different_operations == 3:
		if (result := _remove_concatennation(goal, numbers[-1])) != None:
			if _is_number_matching_goal(result, numbers[:-1], different_operations):
				return True
	if goal % numbers[-1] == 0:
		if _is_number_matching_goal(goal // numbers[-1], numbers[:-1], different_operations):
			return True
	return _is_number_matching_goal(goal - numbers[-1], numbers[:-1], different_operations)

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
