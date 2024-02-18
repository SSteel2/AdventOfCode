import Util.input
import Util.period

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

Shapes = [
	[['#', '#', '#', '#']],
	[['.', '#', '.'], ['#', '#', '#'], ['.', '#', '.']],
	[['#', '#', '#'], ['.', '.', '#'], ['.', '.', '#']],
	[['#'], ['#'], ['#'], ['#']],
	[['#', '#'], ['#', '#']]
]

BoardWidth = 7

def _findHighestRock(field):
	for i, line in enumerate(field[::-1]):
		if '#' in line:
			break
	return len(field) - i - 1

def _move(position, instruction):
	if instruction == '>':
		return (position[0], position[1] + 1)
	elif instruction == '<':
		return (position[0], position[1] - 1)
	elif instruction == 'v':
		return (position[0] - 1, position[1])	

def _isValidMove(shape, position, instruction, field):
	if instruction == '>':
		if position[1] + len(shape[0]) >= BoardWidth:
			return False
		new_position = (position[0], position[1] + 1)
	elif instruction == '<':
		if position[1] <= 0:
			return False
		new_position = (position[0], position[1] - 1)
	elif instruction == 'v':
		if position[0] == 0:
			return False
		new_position = (position[0] - 1, position[1])

	for i, line in enumerate(shape):
		for j, piece in enumerate(line):
			if piece != '.' and field[new_position[0] + i][new_position[1] + j] != '.':
				return False
	return True

def _placeShape(shape, position, field):
	for i, line in enumerate(shape):
		for j, piece in enumerate(line):
			if piece != '.':
				field[position[0] + i][position[1] + j] = piece

def _towerHeight(field):
	empty_rows = 0
	for i in field[::-1]:
		if '#' in i:
			break
		empty_rows += 1
	return len(field) - empty_rows

def _dropShape(shape, field, instructions, instruction_number):
	sapwn_vertical = _towerHeight(field) + 3
	shape_height = len(shape)
	shape_width = len(shape[0])
	height_needed = sapwn_vertical + shape_height - len(field)
	for _ in range(height_needed):
		field.append(['.' for _ in range(BoardWidth)])
	current_position = (sapwn_vertical, 2)
	is_moving = True
	lines_dropped = 0
	vertical_move = 0
	while is_moving:
		instruction = instructions[instruction_number % len(instructions)]
		if lines_dropped < 3:
			if instruction == '>':
				if current_position[1] + vertical_move + shape_width < BoardWidth:
					vertical_move += 1
			elif instruction == '<':
				if current_position[1] + vertical_move > 0:
					vertical_move -= 1
		elif lines_dropped == 3:
			current_position = (current_position[0] - 3, current_position[1] + vertical_move)
		if lines_dropped >= 3:
			if _isValidMove(shape, current_position, instruction, field):
				current_position = _move(current_position, instruction)
			if _isValidMove(shape, current_position, 'v', field):
				current_position = _move(current_position, 'v')
			else:
				is_moving = False
				_placeShape(shape, current_position, field)

		lines_dropped += 1
		instruction_number += 1
	return instruction_number


def silver(input_lines):
	instructions = input_lines[0]
	instruction_number = 0
	field = [['.' for _ in range(BoardWidth)] for _ in range(5)]
	shape_count = 0
	total_shapes = 2022
	while shape_count < total_shapes:
		shape = Shapes[shape_count % len(Shapes)]
		instruction_number = _dropShape(shape, field, instructions, instruction_number)
		shape_count += 1
	return _towerHeight(field)

def gold(input_lines):
	instructions = input_lines[0]
	instruction_length = len(instructions)
	instruction_number = 0
	field = [['.' for _ in range(BoardWidth)] for _ in range(5)]
	shape_count = 0
	target_shapes = 1000000000000
	history_instruction_remainder = []
	history_tower_height = [0]
	initial_slack = 1200
	period_counts = 0
	
	while instruction_number < instruction_length * 10 or instruction_number < 10000:
		shape = Shapes[shape_count % len(Shapes)]
		instruction_number = _dropShape(shape, field, instructions, instruction_number)
		shape_count += 1
		if shape_count % 5 == 0:
			current_height = _towerHeight(field)
			current_instruction_remainder = instruction_number % instruction_length
			history_instruction_remainder.append(current_instruction_remainder)
			history_tower_height.append(current_height)
			if instruction_number > instruction_length * 5 // 3 and shape_count % 100 == 0:
				initial_slack += 10
				period = Util.period.CalculatePeriod(history_instruction_remainder[initial_slack // 5:])
				period_counts += 1
				if period != None:
					break

	increments = (target_shapes - initial_slack) // (period * 5)
	increment_height = history_tower_height[-1] - history_tower_height[-1 - period]
	target_height = history_tower_height[(initial_slack + (target_shapes - initial_slack) % (period * 5)) // 5] + increments * increment_height

	return target_height
