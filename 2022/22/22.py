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

facings = ['R', 'D', 'L', 'U']
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
	inverse_direction = Util.directions.Inverse(direction)
	wrapped_position = Util.directions.MoveMultiple(position, inverse_direction, cell_size)
	new_position = wrapped_position
	while not _isOutOfBounds(new_position, grid):
		wrapped_position = new_position
		new_position = Util.directions.MoveMultiple(wrapped_position, inverse_direction, cell_size)
	return wrapped_position

def _move(distance, current_direction, current_position, grid):
	position = current_position
	for i in range(distance):
		old_position = position
		position = Util.directions.Move(position, current_direction)
		if _isOutOfBounds(position, grid):
			position = _wrapPosition(position, current_direction, grid)
		if Util.directions.Get(grid, position) == '#':
			return old_position
	return position

def _answer(position, direction):
	return (position[0] + 1) * 1000 + (position[1] + 1) * 4 + facings.index(direction)

def silver(input_lines):
	grid, commands = _parse(input_lines)
	current_position = _getStart(grid)
	current_direction = 'R'
	for command in commands:
		if command[0] == 'move':
			current_position = _move(command[1], current_direction, current_position, grid)
		elif command[0] == 'rotate':
			current_direction = _rotate(command[1], current_direction)
	return _answer(current_position, current_direction)

def gold(input_lines):
	pass
