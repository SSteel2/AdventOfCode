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
	while True:
		next_position = Util.directions.Move(position, direction)
		if (symbol := Util.directions.Get(grid, next_position)) == '%':
			return None, None
		if symbol != '#':
			return next_position, direction
		direction = Util.directions.RotateClockwise(direction)

def silver(input_lines):
	grid = Util.directions.PadTable(input_lines, 1, '%')
	position, direction = _find_start(grid)
	Util.directions.Set(grid, position, 'X')
	position, direction = _get_next(position, direction, grid)
	while position != None:
		Util.directions.Set(grid, position, 'X')
		position, direction = _get_next(position, direction, grid)
	return Util.directions.Count(grid, 'X')

def _is_loop_ahead(position, direction, grid, global_visited):
	position, direction = _get_next(position, direction, grid)
	local_visited = set()
	while position != None:
		current_vector = (position, direction)
		if current_vector in global_visited or current_vector in local_visited:
			return True
		local_visited.add(current_vector)
		position, direction = _get_next(position, direction, grid)
	return False

def gold(input_lines):
	grid = Util.directions.PadTable(input_lines, 1, '%')
	position, direction = _find_start(grid)
	possible_loops = 0
	global_visited = set()

	while True:
		global_visited.add((position, direction))
		Util.directions.Set(grid, position, 'X')
		next_position, next_direction = _get_next(position, direction, grid)
		if next_position == None:
			break
		if Util.directions.Get(grid, next_position) != 'X':
			Util.directions.Set(grid, next_position, '#')
			if _is_loop_ahead(position, direction, grid, global_visited):
				possible_loops += 1
			Util.directions.Set(grid, next_position, '.')
		position, direction = next_position, next_direction

	return possible_loops