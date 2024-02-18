import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

Shapes = [
	[['#', '#', '#', '#']],
	[['.', '#', '.'], ['#', '#', '#'], ['.', '#', '.']],
	[['#', '#', '#'], ['.', '.', '#'], ['.', '.', '#']],
	[['#'], ['#'], ['#'], ['#']],
	[['#', '#'], ['#', '#']]
]

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
		if position[1] + len(shape[0]) >= len(field[0]):
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

def _debugPrintField(field):
	for i, line in enumerate(field[::-1]):
		print(f'{len(field) - i - 1:>3} {"".join(line)}')

def silver(input_lines):
	board_width = 7
	instructions = input_lines[0]
	instruction_number = 0
	field = [['.' for _ in range(board_width)] for _ in range(5)]
	shape_count = 0
	total_shapes = 2022
	while shape_count < total_shapes:
		sapwn_vertical = _findHighestRock(field) + 4
		if shape_count == 0:
			sapwn_vertical = 3
		shape = Shapes[shape_count % len(Shapes)]
		shape_height = len(shape)
		shape_width = len(shape[0])
		height_needed = sapwn_vertical + shape_height - len(field)
		for _ in range(height_needed):
			field.append(['.' for _ in range(board_width)])
		current_position = (sapwn_vertical, 2)
		is_moving = True
		lines_dropped = 0
		vertical_move = 0
		while is_moving:
			instruction = instructions[instruction_number % len(instructions)]
			if lines_dropped < 3:
				if instruction == '>':
					if current_position[1] + vertical_move + shape_width < board_width:
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

		shape_count += 1

	# _debugPrintField(field)
	return _towerHeight(field)

def gold(input_lines):
	pass
