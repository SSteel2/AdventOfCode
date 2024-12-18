import Util.input
import Util.Frequency

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(input_lines):
	register = {}
	program = []
	for line in input_lines:
		split_line = line.split(' ')
		if split_line[0] == 'Register':
			register[split_line[1][:1]] = int(split_line[2])
		elif split_line[0] == 'Program:':
			program = [int(i) for i in split_line[1].split(',')]
	return register, program

def _combo_operand(operand, register):
	if operand <= 3:
		return operand
	elif operand == 4:
		return register['A']
	elif operand == 5:
		return register['B']
	elif operand == 6:
		return register['C']

def _do_instruction(opcode, operand, register, output, instruction_pointer):
	if opcode == 0:  # adv
		register['A'] = register['A'] // 2 ** _combo_operand(operand, register)
	elif opcode == 1:  # bxl
		register['B'] = register['B'] ^ operand
	elif opcode == 2:  # bst
		register['B'] = _combo_operand(operand, register) % 8
	elif opcode == 3:  # jnz
		if register['A'] != 0:
			return operand
	elif opcode == 4:  # bxc
		register['B'] = register['B'] ^ register['C']
	elif opcode == 5:  # out
		output.append(_combo_operand(operand, register) % 8)
	elif opcode == 6:  # bdv
		register['B'] = register['A'] // 2 ** _combo_operand(operand, register)
	elif opcode == 7:  # cdv
		register['C'] = register['A'] // 2 ** _combo_operand(operand, register)
	return instruction_pointer + 2

def _launch_program(register, program):
	instruction_pointer = 0
	output = []
	while instruction_pointer < len(program):
		instruction_pointer = _do_instruction(program[instruction_pointer], program[instruction_pointer + 1], register, output, instruction_pointer)
	return output	

def silver(input_lines):
	register, program = _parse(input_lines)
	output = _launch_program(register, program)
	return ','.join([str(i) for i in output])

def _solution_to_binary_string(solution, replace_empty):
	max_key = max(solution.keys())
	stringified = []
	for i in range(max_key, -1, -1):
		if i in solution:
			stringified.append(str(solution[i]))
		else:
			if replace_empty:
				stringified.append('0')
			else:
				stringified.append('_')
	return ''.join(stringified)

def _is_solutions_compatible(a, b):
	for key in a:
		if key in b and b[key] != a[key]:
			return False
	return True

def _join_solutions(a, b):
	result = {}
	for key in a:
		result[key] = a[key]
	for key in b:
		result[key] = b[key]
	return result

def gold(input_lines):
	register, program = _parse(input_lines)
	global_solutions = []
	for index, operand in enumerate(program):
		new_global_solutions = []
		for i in range(8):
			shift = 7 - i
			far_number = operand ^ i
			solution = {index * 3 + 0: i % 2, index * 3 + 1: i // 2 % 2, index * 3 + 2: i // 4}
			possible_solution = True
			for j in range(3):
				new_position = index * 3 + shift + j
				new_number = far_number // (2 ** j) % 2
				if new_position in solution and solution[new_position] != new_number:
					possible_solution = False
					break
				solution[new_position] = new_number
			if not possible_solution:
				continue
			if index == 0:
				new_global_solutions.append(solution)
			else:
				for global_solution in global_solutions:
					if _is_solutions_compatible(global_solution, solution):
						new_global_solutions.append(_join_solutions(global_solution, solution))
		global_solutions = new_global_solutions

	numbers = []
	for solution in global_solutions:
		numbers.append(int(_solution_to_binary_string(solution, True), 2))
	return min(numbers)
