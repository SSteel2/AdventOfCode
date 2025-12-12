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

def _debug_equation_print(equations, joltages):
	for i in range(len(joltages)):
		print(equations[i])

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
	# print("makeZero", line_int, line_zero, col)
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

# dabartine problema: kas nutinka, jei nei6eina pasirinkti keyline, nes yra 2 pilni ne=inomieji
def _find_best_solution(equations, current_solution):
	# debug
	print('_find_best_solution', current_solution)
	# pprint.pprint(equations)

	# find line with 2 non-zero positive integers (last one doesn't count)
	print('looking for keyline')
	key_line = -1
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
		if count == 2:
			key_line = index
			break
	if key_line == -1:
		print('Cannot find key_line. TODO Figure out solution')
		return None
	print('keyline found', key_line)

	# this line will be iterated through all possible solutions while remaining lines should be calculated
	first_non_zero_index = -1
	second_non_zero_index = -1
	for i in range(len(equations[key_line])):
		if equations[key_line][i] != 0:
			if first_non_zero_index == -1:
				first_non_zero_index = i
			elif second_non_zero_index == -1:
				second_non_zero_index = i
				break
	print('non zero indexes', first_non_zero_index, second_non_zero_index)

	min_button_presses = math.inf
	best_solution = None
	# Determine max iteration range
	# print('#debug: key line', key_line)
	remainder = equations[key_line][-1]
	for i, col in enumerate(equations[key_line][:-1]):
		if current_solution[i] != None and col != 0:
			remainder -= col * current_solution[i]
	first_param_max = remainder // equations[key_line][first_non_zero_index]
	print('first_param_max', first_param_max, current_solution)
	for first_param_solution in range(first_param_max + 1):
		print('key_line', key_line, 'first_non_zero_index', first_non_zero_index, 'first_param_solution', first_param_solution)
		solution = [i for i in current_solution]
		solution[first_non_zero_index] = first_param_solution
		remainder = equations[key_line][-1]
		for i, col in enumerate(equations[key_line][:-1]):
			if solution[i] != None and col != 0:
				remainder -= col * solution[i]
		if remainder % equations[key_line][second_non_zero_index] != 0:
			continue  # invalid parameter combination
		solution[second_non_zero_index] = remainder // equations[key_line][second_non_zero_index]
		if solution[second_non_zero_index] < 0:
			print('huh')
			# solution is wrong, retry at next first_param_solution
			continue

		# Starting parameters are set up, now we need to find the rest of the solution
		is_correct = True
		# print('Starting parameters solution:', solution)
		for index, equation in enumerate(equations):
			if index == key_line:
				continue
			# there should be 1 unknown per equation left (TODO if there are more)
			remainder = equation[-1]
			unknown_col_index = -1
			# print('Going through each equation. Index', index)
			for i, col in enumerate(equation[:-1]):
				if col == 0:
					continue
				elif solution[i] != None:
					remainder -= col * solution[i]
				elif unknown_col_index == -1:
					unknown_col_index = i
				else:
					# Multiple unknowns in this equation, move on to next one
					unknown_col_index = -2

			if unknown_col_index == -1:
				if remainder == 0:
				  	# move on to next equation, this doesnt provide additional information and everything is correct
					continue
				else:
					# solution is wrong, retry at next first_param_solution
					is_correct = False
					break
			elif unknown_col_index == -2:
				continue
			else:
				if remainder % equations[index][unknown_col_index] != 0:
					# solution is wrong, retry at next first_param_solution
					is_correct = False
					break
				solution[unknown_col_index] = remainder // equations[index][unknown_col_index]
				if solution[unknown_col_index] < 0:
					# solution is wrong, retry at next first_param_solution
					is_correct = False
					break
		if not is_correct:
			continue

		# Go deeper if there are holes in the solution
		if any(i == None for i in solution):
			full_solution = _find_best_solution(equations, solution)
			if full_solution == None:
				continue
			solution = full_solution
			# print('Sanity check failed, something wrong')
			# print('current solution:', solution)
			# print('Equations:')
			# pprint.pprint(equations)
			# return None

		# Calculate button presses
		button_presses = sum(solution)
		if button_presses < min_button_presses:
			min_button_presses = button_presses
			best_solution = solution

	print('best solution:', best_solution)
	return best_solution

def gold(input_lines):
	problems = Util.input.ParseInputLines(input_lines, _parse)
	total_result = 0
	solved_count = 0
	for index, problem in enumerate(problems):  # debug enumerate
		_, buttons, joltages = problem
		# f = Util.Frequency.Frequency()
		# for button in buttons:
		# 	for i in button:
		# 		f.add(i)
		# print(joltage)
		# print(buttons)
		# print(f)
		# print(f'{index}: {len(joltage) - len(buttons)} {len(joltage)}, {len(buttons)}')
		equations = [[0 for _ in range(len(buttons) + 1)] for _ in range(len(joltages))]
		# each button corresponds to number of times a point is added, so a single number corresponds to a equation
		for button_index, button in enumerate(buttons):
			for light in button:
				equations[light][button_index] = 1
		for i, joltage in enumerate(joltages):
			equations[i][-1] = joltage
		# pprint.pprint(equations)
		# print('-------------------------------------------')
		# _debug_equation_print(equations, joltages)
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
		# pprint.pprint(equations)

		if _is_solved(equations):
			for equation in equations:
				total_result += equation[-1]
			solved_count += 1
		else:
			# print('Solving _find_best_solution for', index)
			_debug_equation_print(equations, joltages)
			best_solution = _find_best_solution(equations, [None for _ in range(len(buttons))])
			if best_solution == None:
				print('--------------------------------------------------- Couldnt find answer', index)
			else:
				# print('Solved with _find_best_solution', index)
				solved_count += 1
				total_result += sum(best_solution)
	print(solved_count)
	# Current best with old algorithm 146/163 - 14394
	return total_result
