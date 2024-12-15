import Util.input
import Util.directions

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(input_lines):
	grid = []
	instructions = []
	first_stage = True
	for line in input_lines:
		if line == "":
			first_stage = False
			continue
		if first_stage:
			grid.append([i for i in line])
		else:
			instructions.append([i for i in line])
	instructions = Util.directions.Convert(instructions, {'^': 'U', '<': 'L', 'v': 'D', '>': 'R'})
	instructions = [i for j in instructions for i in j]
	return grid, instructions

def _find_start(grid):
	for line_num, line in enumerate(grid):
		for col_num, col in enumerate(line):
			if col == '@':
				return (line_num, col_num)

def _move_robot(grid, current, instruction):
	last_position = Util.directions.Move(current, instruction)
	next_position = last_position
	while (last_value := Util.directions.Get(grid, last_position)) == 'O':
		last_position = Util.directions.Move(last_position, instruction)
	if last_value == '#':
		return current
	if next_position != last_position:
		Util.directions.Set(grid, last_position, 'O')
		Util.directions.Set(grid, next_position, '.')
	return next_position

def _calculate_gps(grid, marker):
	score = 0
	for line_num, line in enumerate(grid):
		for col_num, col in enumerate(line):
			if col == marker:
				score += (line_num * 100 + col_num)
	return score

def silver(input_lines):
	grid, instructions = _parse(input_lines)
	current = _find_start(grid)
	Util.directions.Set(grid, current, '.')
	for instruction in instructions:
		current = _move_robot(grid, current, instruction)
	return _calculate_gps(grid, 'O')

def _scale_map(grid):
	scaled_grid = [[] for i in grid]
	for line_num, line in enumerate(grid):
		for col in line:
			if col == '#':
				scaled_grid[line_num].extend(['#', '#'])
			elif col == 'O':
				scaled_grid[line_num].extend(['[', ']'])
			elif col == '.':
				scaled_grid[line_num].extend(['.', '.'])
			elif col == '@':
				scaled_grid[line_num].extend(['@', '.'])
	return scaled_grid

def _move_horizontal(grid, current, instruction):
	last_position = Util.directions.Move(current, instruction)
	next_position = last_position
	while (last_value := Util.directions.Get(grid, last_position)) == '[' or last_value == ']':
		last_position = Util.directions.Move(last_position, instruction)
	if last_value == '#':
		return current
	while last_position != next_position:
		prev_position = Util.directions.Move(last_position, Util.directions.Inverse(instruction))
		prev_value = Util.directions.Get(grid, prev_position)
		Util.directions.Set(grid, last_position, prev_value)
		last_position = prev_position
	Util.directions.Set(grid, next_position, '.')
	return next_position

def _can_move_vertical(grid, current, instruction):
	next_position = Util.directions.Move(current, instruction)
	next_value = Util.directions.Get(grid, next_position)
	if next_value == '.':
		return True
	if next_value == '[':
		right_position = Util.directions.Move(next_position, 'R')
		return _can_move_vertical(grid, next_position, instruction) and _can_move_vertical(grid, right_position, instruction)
	if next_value == ']':
		left_position = Util.directions.Move(next_position, 'L')
		return _can_move_vertical(grid, next_position, instruction) and _can_move_vertical(grid, left_position, instruction)
	return False

def _move_box_vertical(grid, current, instruction):
	current_value = Util.directions.Get(grid, current)
	next_position = Util.directions.Move(current, instruction)
	if current_value == '[':
		side_current_position = Util.directions.Move(current, 'R')
		side_next_position = Util.directions.Move(side_current_position, instruction)
		_move_box_vertical(grid, next_position, instruction)
		_move_box_vertical(grid, side_next_position, instruction)
		Util.directions.Set(grid, next_position, '[')
		Util.directions.Set(grid, current, '.')
		Util.directions.Set(grid, side_next_position, ']')
		Util.directions.Set(grid, side_current_position, '.')
	elif current_value == ']':
		side_current_position = Util.directions.Move(current, 'L')
		side_next_position = Util.directions.Move(side_current_position, instruction)
		_move_box_vertical(grid, next_position, instruction)
		_move_box_vertical(grid, side_next_position, instruction)
		Util.directions.Set(grid, next_position, ']')
		Util.directions.Set(grid, current, '.')
		Util.directions.Set(grid, side_next_position, '[')
		Util.directions.Set(grid, side_current_position, '.')

def _move_vertical(grid, current, instruction):
	if _can_move_vertical(grid, current, instruction):
		next_position = Util.directions.Move(current, instruction)
		_move_box_vertical(grid, next_position, instruction)
		return next_position
	return current

def _move_robot_gold(grid, current, instruction):
	if instruction == 'R' or instruction == 'L':
		return _move_horizontal(grid, current, instruction)
	if instruction == 'D' or instruction == 'U':
		return _move_vertical(grid, current, instruction)

def gold(input_lines):
	grid, instructions = _parse(input_lines)
	grid = _scale_map(grid)
	current = _find_start(grid)
	Util.directions.Set(grid, current, '.')
	for instruction in instructions:
		current = _move_robot_gold(grid, current, instruction)
	return _calculate_gps(grid, '[')
