import Util.input
import Util.directions

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(input_lines):
	is_map_phase = True
	grid = []
	commands = []
	for line in input_lines:
		if line == "":
			is_map_phase = False
			continue
		if is_map_phase:
			grid.append(line)
		else:
			position = 0
			for x, char in enumerate(line):
				if not char.isnumeric():
					commands.append(('move', int(line[position:x])))
					commands.append(('rotate', char))
					position = x + 1
			commands.append(('move', int(line[position:])))
	return grid, commands

facings = ['U', 'R', 'D', 'L']
cell_size = 50

def _getStart(grid):
	for i, char in enumerate(grid[0]):
		if char != ' ':
			return (0, i)

def _rotate(rotation, current_direction):
	adjustment = 1 if rotation == 'R' else -1
	return facings[(facings.index(current_direction) + adjustment) % len(facings)]

def _isOutOfBounds(position, grid):
	return position[0] < 0 or position[0] >= len(grid) or position[1] < 0 or position[1] >= len(grid[position[0]]) or grid[position[0]][position[1]] == ' '

def _wrapPosition(position, direction, grid):
	position = Util.directions.Move(position, direction)
	inverse_direction = Util.directions.Inverse(direction)
	wrapped_position = Util.directions.MoveMultiple(position, inverse_direction, cell_size)
	new_position = wrapped_position
	while not _isOutOfBounds(new_position, grid):
		wrapped_position = new_position
		new_position = Util.directions.MoveMultiple(wrapped_position, inverse_direction, cell_size)
	return wrapped_position, direction

def _answer(position, direction):
	return (position[0] + 1) * 1000 + (position[1] + 1) * 4 + ((facings.index(direction) - 1) % 4)

def _move(distance, current_direction, current_position, grid, wrap_function):
	direction = current_direction
	position = current_position
	for i in range(distance):
		old_position = position
		old_direction = direction
		position = Util.directions.Move(position, direction)
		if _isOutOfBounds(position, grid):
			position, direction = wrap_function(old_position, old_direction, grid)
		if Util.directions.Get(grid, position) == '#':
			return old_position, old_direction
	return position, direction

def _solve(grid, commands, wrap_function):
	current_position = _getStart(grid)
	current_direction = 'R'
	for command in commands:
		if command[0] == 'move':
			current_position, current_direction = _move(command[1], current_direction, current_position, grid, wrap_function)
		elif command[0] == 'rotate':
			current_direction = _rotate(command[1], current_direction)
	return _answer(current_position, current_direction)

def silver(input_lines):
	grid, commands = _parse(input_lines)
	return _solve(grid, commands, _wrapPosition)

Cube = {
	'z_plus': {'name': 'top', 'inverse': False, 'axis': 'z'},
	'z_minus': {'name': 'bottom', 'inverse': True, 'axis': 'z'},
	'x_plus': {'name': 'right', 'inverse': False, 'axis': 'x'},
	'x_minus': {'name': 'left', 'inverse': True, 'axis': 'x'},
	'y_minus': {'name': 'front', 'inverse': True, 'axis': 'y'},
	'y_plus': {'name': 'back', 'inverse': False, 'axis': 'y'}
}

Rotations = {
	'z': ['y_plus', 'x_plus', 'y_minus', 'x_minus'],
	'x': ['z_plus', 'y_plus', 'z_minus', 'y_minus'],
	'y': ['x_plus', 'z_plus', 'x_minus', 'z_minus'],
}

InverseNormal = {
	'z_plus': 'z_minus',
	'z_minus': 'z_plus',
	'y_plus': 'y_minus',
	'y_minus': 'y_plus',
	'x_plus': 'x_minus',
	'x_minus': 'x_plus'
}

def _rotate90deg(vector, normal):
	rotations = Rotations[Cube[normal]['axis']]
	adjustment = -1 if Cube[normal]['inverse'] else 1
	if vector not in rotations:
		return vector
	return rotations[(rotations.index(vector) + adjustment) % 4]

def _getSides(normal):
	sides = Rotations[Cube[normal]['axis']]
	if Cube[normal]['inverse']:
		sides = sides[::-1]
	return sides

def _walkCube(current_position, grid, current_normal):
	global_up = Cube[current_normal]['global_up']
	sides = _getSides(current_normal)
	rotation_index = sides.index(global_up)

	for facing_index in range(len(facings)):
		new_position = Util.directions.MoveMultiple(current_position, facings[facing_index], cell_size)
		if not _isOutOfBounds(new_position, grid):
			new_normal = sides[(rotation_index + facing_index) % 4]
			if 'global_up' not in Cube[new_normal]:
				rotational_axis = sides[(rotation_index + facing_index + 1) % 4]
				Cube[new_normal]['global_up'] = _rotate90deg(Cube[current_normal]['global_up'], rotational_axis)
				Cube[new_normal]['start'] = new_position
				_walkCube(new_position, grid, new_normal)

def _constructCube(grid, cell_size):
	start = _getStart(grid)
	Cube['z_plus']['global_up'] = 'y_plus'
	Cube['z_plus']['start'] = start
	_walkCube(start, grid, 'z_plus')

def _findCube(position):
	for cube_normal in Cube:
		cube_start = Cube[cube_normal]['start']
		if cube_start[0] <= position[0] < cube_start[0] + cell_size and cube_start[1] <= position[1] < cube_start[1] + cell_size:
			return cube_normal

def _getGlobalDirection(local_direction, cube_normal):
	facing_index = facings.index(local_direction)
	sides = _getSides(cube_normal)
	return sides[(sides.index(Cube[cube_normal]['global_up']) + facing_index) % 4]

def _wrapPositionCube(old_position, direction, grid):
	old_cube_normal = _findCube(old_position)
	global_direction = _getGlobalDirection(direction, old_cube_normal)
	new_cube_normal = global_direction
	if direction == 'L' or direction == 'R':
		exit_coordinate = old_position[0] - Cube[old_cube_normal]['start'][0]
	else:
		exit_coordinate = old_position[1] - Cube[old_cube_normal]['start'][1]
	if direction == 'D' or direction == 'L':
		exit_coordinate = cell_size - 1 - exit_coordinate
	sides = _getSides(new_cube_normal)
	new_global_direction = InverseNormal[old_cube_normal]
	new_cube_global_up = Cube[new_cube_normal]['global_up']
	rotational_difference = (sides.index(new_global_direction) - sides.index(new_cube_global_up)) % 4
	if rotational_difference == 0:
		new_position = (cell_size - 1, exit_coordinate)
	elif rotational_difference == 1:
		new_position = (exit_coordinate, 0)
	elif rotational_difference == 2:
		new_position = (0, cell_size - 1 - exit_coordinate)
	elif rotational_difference == 3:
		new_position = (cell_size - 1 - exit_coordinate, cell_size - 1)
	return (new_position[0] + Cube[new_cube_normal]['start'][0], new_position[1] + Cube[new_cube_normal]['start'][1]), facings[rotational_difference]

def gold(input_lines):
	grid, commands = _parse(input_lines)
	_constructCube(grid, cell_size)
	return _solve(grid, commands, _wrapPositionCube)
