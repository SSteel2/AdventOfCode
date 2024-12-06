import Util.input
import Util.directions

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _find_start(input_lines):
	for line_num, line in enumerate(input_lines):
		for col_num, col in enumerate(line):
			if col == '^':
				return (line_num, col_num), 'U'

def _get_next(position, direction, grid):
	next_position = Util.directions.Move(position, direction)
	if Util.directions.IsOutOfBounds(grid, next_position):
		return None, None
	while Util.directions.Get(grid, next_position) == '#':
		direction = Util.directions.RotateClockwise(direction)
		next_position = Util.directions.Move(position, direction)
		if Util.directions.IsOutOfBounds(grid, next_position):
			return None, None
	return next_position, direction

def _count_visited(grid):
	count = 0
	for line in grid:
		for col in line:
			if col == 'X':
				count += 1
	return count

def silver(input_lines):
	position, direction = _find_start(input_lines)
	grid = [[col for col in line] for line in input_lines]
	Util.directions.Set(grid, position, 'X')
	position, direction = _get_next(position, direction, grid)
	while position != None:
		Util.directions.Set(grid, position, 'X')
		position, direction = _get_next(position, direction, grid)
	return _count_visited(grid)

def gold(input_lines):
	# man reikia trackinti visited cells
	pass
