import Util.input
import itertools
import math
import Util.Frequency
import pprint
import Util.math

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(line):
	parts = line.split(' ')
	target = [1 if i == '#' else 0 for i in parts[0][1:-1]]
	buttons = [[int(j) for j in i[1:-1].split(',')] for i in parts[1:-1]]
	joltages = [int(i) for i in parts[-1][1:-1].split(',')]
	return target, buttons, joltages

def silver(input_lines):
	problems = Util.input.ParseInputLines(input_lines, _parse)
	total_result = 0
	for problem in problems:
		target, buttons, _ = problem
		min_presses = math.inf
		is_correct = False
		for presses in range(len(buttons)):
			for combination in itertools.combinations(buttons, presses):
				result = [i for i in target]
				for button in combination:
					for position in button:
						result[position] += 1
				is_correct = all(i % 2 == 0 for i in result)
				if is_correct:
					break
			if is_correct:
				min_presses = presses
				break
		total_result += min_presses
	return total_result

def _subtract(matrix, line_a, line_b, multiplier):
	for i in range(len(matrix[line_a])):
		matrix[line_b][i] = matrix[line_b][i] - matrix[line_a][i] * multiplier

def _multiply(matrix, line, multiplier):
	for i in range(len(matrix[line])):
		matrix[line][i] *= multiplier

def _divide(matrix, line, divisor):
	for i in range(len(matrix[line])):
		matrix[line][i] //= divisor

def _makeZero(matrix, line_int, line_zero, col):
	if matrix[line_zero][col] % matrix[line_int][col] == 0:
		_subtract(matrix, line_int, line_zero, matrix[line_zero][col] // matrix[line_int][col])
	else:
		mult = Util.math.lcm(abs(matrix[line_zero][col]), abs(matrix[line_int][col]))
		mult_zero = mult // matrix[line_zero][col]
		mult_int = mult // matrix[line_int][col]
		_multiply(matrix, line_zero, mult_zero)
		_multiply(matrix, line_int, mult_int)
		_subtract(matrix, line_int, line_zero, matrix[line_zero][col] // matrix[line_int][col])
		_divide(matrix, line_int, mult_int)

def _simplify(matrix):
	for line_int in range(len(matrix)):
		divisor = 1
		non_zero_elements = [i for i in matrix[line_int] if i != 0]
		if all(i < 0 for i in non_zero_elements):
			divisor = -1
		if len(non_zero_elements) > 0:
			current_gcd = abs(non_zero_elements[0])
			for element in non_zero_elements[1:]:
				current_gcd = Util.math.gcd(current_gcd, abs(element))
				if current_gcd == 1:
					break
			divisor *= current_gcd
		_divide(matrix, line_int, divisor)

def _is_solved(matrix):
	# does the matrix[][:-1] contain only a single "1" per line/column
	lines = [0 for _ in range(len(matrix))]
	columns = [0 for _ in range(len(matrix[0]) - 1)]
	for i, line in enumerate(matrix):
		for j, col in enumerate(line[:-1]):
			if col == 1:
				lines[i] += 1
				columns[j] += 1
			elif col != 0:
				return False
	return all(i in [0, 1] for i in lines) and all(i in [0, 1] for i in columns)

def _calculate_solution(equations, solution):
	# go through all lines and fill in the empty solution spots if they can be determined without guessing
	# returns None, if solution is wrong
	is_changed = True
	while is_changed:
		is_changed = False
		for index, equation in enumerate(equations):
			# Check if line only has a single unknown
			remainder = equation[-1]
			unknown_col_index = -1
			for i, col in enumerate(equation[:-1]):
				if col == 0:
					continue
				elif solution[i] != None:
					remainder -= col * solution[i]
				elif unknown_col_index == -1:
					unknown_col_index = i
				else:
					unknown_col_index = -2
			# No unknowns
			if unknown_col_index == -1:
				if remainder == 0:
				  	# move on to next equation, this doesnt provide additional information and everything is correct
					continue
				else:
					return None
			# Multiple unknowns
			elif unknown_col_index == -2:
				continue
			else:
				if remainder % equations[index][unknown_col_index] != 0:
					return None
				solution[unknown_col_index] = remainder // equations[index][unknown_col_index]
				if solution[unknown_col_index] < 0:
					return None
				is_changed = True
	return solution

def _find_best_solution(equations, current_solution):
	# find line with 2 non-zero positive integers (last one doesn't count) for prefered way of solving
	column_candidates = {}
	for index, line in enumerate(equations):
		count = 0
		for i, col in enumerate(line[:-1]):
			if current_solution[i] != None:
				continue
			if col > 0:
				count += 1
			elif col < 0:
				count = -1
				break
		column_candidates[index] = count
	key_line = -1
	min_unknowns = math.inf
	for index in column_candidates:
		if column_candidates[index] >= 2 and column_candidates[index] < min_unknowns:
			min_unknowns = column_candidates[index]
			key_line = index
	# if nothing preferable is found, pick first one
	if key_line == -1:
		column = -1
		for i, val in enumerate(current_solution):
			if val == None:
				column = i
				break
		for i, equation in enumerate(equations):
			if equation[column] != 0:
				key_line = i
				break

	# this line will be iterated through all possible solutions while remaining lines should be calculated
	first_non_zero_index = -1
	for i in range(len(equations[key_line])):
		if equations[key_line][i] != 0:
			if first_non_zero_index == -1 and (i >= len(current_solution) or current_solution[i] == None):
				first_non_zero_index = i
				break

	min_button_presses = math.inf
	best_solution = None
	# Determine max iteration range
	remainder = equations[key_line][-1]
	for i, col in enumerate(equations[key_line][:-1]):
		if current_solution[i] != None and col != 0:
			remainder -= col * current_solution[i]
	first_param_max = remainder // equations[key_line][first_non_zero_index]
	for first_param_solution in range(first_param_max + 1):
		solution = [i for i in current_solution]
		solution[first_non_zero_index] = first_param_solution
		solution = _calculate_solution(equations, solution)
		if solution == None:
			continue

		# Go deeper (recursively) if there are holes in the solution
		if any(i == None for i in solution):
			full_solution = _find_best_solution(equations, solution)
			if full_solution == None:
				continue
			solution = full_solution

		# Calculate button presses
		button_presses = sum(solution)
		if button_presses < min_button_presses:
			min_button_presses = button_presses
			best_solution = solution

	return best_solution

def gold(input_lines):
	problems = Util.input.ParseInputLines(input_lines, _parse)
	total_result = 0
	for problem in problems:
		_, buttons, joltages = problem
		equations = [[0 for _ in range(len(buttons) + 1)] for _ in range(len(joltages))]
		# each button corresponds to number of times a point is added, so a single number corresponds to a equation
		for button_index, button in enumerate(buttons):
			for light in button:
				equations[light][button_index] = 1
		for i, joltage in enumerate(joltages):
			equations[i][-1] = joltage
		used_lines = set()
		for i in range(len(buttons)):
			non_zero_index = -1
			for j in range(len(joltages)):
				if equations[j][i] == 0 or j in used_lines:
					continue
				if non_zero_index == -1:
					non_zero_index = j
					used_lines.add(j)
					break
			if non_zero_index == -1:
				continue
			
			if equations[non_zero_index][i] != 1:
				all_divisible = all(j % equations[non_zero_index][i] == 0 for j in equations[non_zero_index])
				if all_divisible:
					_divide(equations, non_zero_index, equations[non_zero_index][i])
			
			for j in range(len(joltages)):
				if non_zero_index == j:
					continue
				_makeZero(equations, non_zero_index, j, i)

		_simplify(equations)

		if _is_solved(equations):
			for equation in equations:
				total_result += equation[-1]
		else:
			best_solution = _find_best_solution(equations, [None for _ in range(len(buttons))])
			total_result += sum(best_solution)
	return total_result
