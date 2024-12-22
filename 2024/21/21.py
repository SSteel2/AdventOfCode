import Util.input
import Util.directions
import math

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

NUMPAD = {'7': (0, 0), '8': (0, 1), '9': (0, 2),
	'4': (1, 0), '5': (1, 1), '6': (1, 2),
	'1': (2, 0), '2': (2, 1), '3': (2, 2),
	'0': (3, 1), 'A': (3, 2)}

ARROWS = {'^': (0, 1), 'A': (0, 2), '<': (1, 0), 'v': (1, 1), '>': (1, 2)}

def _movement(keyboard, current_location, instruction, is_vertical):
	if is_vertical:
		index = 0
		direction_low = ('^', 'U')
		direction_high = ('v', 'D')
	else:
		index = 1
		direction_low = ('<', 'L')
		direction_high = ('>', 'R')
	moves = []
	if current_location[index] > keyboard[instruction][index]:
		for i in range(current_location[index] - keyboard[instruction][index]):
			moves.append(direction_low[0])
			current_location = Util.directions.Move(current_location, direction_low[1])
			if current_location not in keyboard.values():
				return None
	elif current_location[index] < keyboard[instruction][index]:
		for i in range(keyboard[instruction][index] - current_location[index]):
			moves.append(direction_high[0])
			current_location = Util.directions.Move(current_location, direction_high[1])
			if current_location not in keyboard.values():
				return None
	return moves, current_location

def _map_instructions(instructions, keyboard):
	mapped_instructions = [[]]
	current_location = 'A'
	for instruction in instructions:
		# horizontal first
		horizontal = None
		result1 = _movement(keyboard, keyboard[current_location], instruction, False)
		if result1 != None:
			result2 = _movement(keyboard, result1[1], instruction, True)
			horizontal = result1[0] + result2[0] + ['A']

		# vertical first
		vertical = None
		result1 = _movement(keyboard, keyboard[current_location], instruction, True)
		if result1 != None:
			result2 = _movement(keyboard, result1[1], instruction, False)
			vertical = result1[0] + result2[0] + ['A']

		valid_options = []
		if horizontal != None:
			valid_options.append(horizontal)
		if vertical != None and vertical != horizontal:
			valid_options.append(vertical)
		new_mapped_instructions = []
		for mapped_instruction in mapped_instructions:
			for option in valid_options:
				new_mapped_instructions.append(mapped_instruction + option)
		mapped_instructions = new_mapped_instructions

		current_location = instruction
	return mapped_instructions

memoization = {}
def _recursive_move_count(instruction_chunk, iterations):
	'''Calculates how many moves will need to be made in order to fufill instructions after iteration number of inception levels'''
	string_instruction_chunk = ''.join(instruction_chunk)
	if (string_instruction_chunk, iterations) in memoization:
		return memoization[(string_instruction_chunk, iterations)]
	if iterations == 0:
		return len(instruction_chunk)
	possible_instructions = _map_instructions(instruction_chunk, ARROWS)
	min_instruction_count = math.inf
	for instructions in possible_instructions:
		move_count = 0
		for instruction_chunk in _split_chunks(instructions):
			move_count += _recursive_move_count(instruction_chunk, iterations - 1)
		if move_count < min_instruction_count:
			min_instruction_count = move_count
	memoization[(string_instruction_chunk, iterations)] = min_instruction_count
	return min_instruction_count

def _split_chunks(instructions):
	'''Splits instruction string/list into strings/lists ending with "A"'''
	accept_indices = [-1] + [i for i, x in enumerate(instructions) if x == 'A']
	chunks = []
	for i in range(1, len(accept_indices)):
		chunks.append(instructions[accept_indices[i - 1] + 1:accept_indices[i] + 1])
	return chunks

def _solve_instruction_line(line, iterations):
	initial_robot_instructions = _map_instructions(line, NUMPAD)
	global_move_count = math.inf
	for initial_robot_instruction in initial_robot_instructions:
		move_count = 0
		for instruction_chunk in _split_chunks(initial_robot_instruction):
			move_count += _recursive_move_count(instruction_chunk, iterations)
		if move_count < global_move_count:
			global_move_count = move_count
	return global_move_count

def _solution(input_lines, iteration_count):
	score = 0
	for line in input_lines:
		solution = _solve_instruction_line(line, iteration_count)
		score += solution * int(line[:-1])
	return score	

def silver(input_lines):
	return _solution(input_lines, 2)

def gold(input_lines):
	return _solution(input_lines, 25)
