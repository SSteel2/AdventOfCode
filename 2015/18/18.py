import Util.input
import Util.directions

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(input_lines):
	grid = [[0 for _ in input_lines[0]] for _ in input_lines]
	for line_num, line in enumerate(input_lines):
		for col_num, col in enumerate(line):
			if col == '#':
				grid[line_num][col_num] = 1
	return grid

direction_rose = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]

def _is_live(grid, position):
	neighbours = 0
	for direction in direction_rose:
		neighbours += Util.directions.Get(grid, Util.directions.MoveCustom(position, direction))
	current = Util.directions.Get(grid, position)
	if neighbours == 3 or neighbours == 2 and current == 1:
		return 1
	return 0

def _next_position(grid):
	new_grid = [[0 for _ in grid[0]] for _ in grid]
	padded_grid = Util.directions.PadTable(grid, 1, 0)
	for line_num in range(len(grid)):
		for col_num in range(len(grid[line_num])):
			new_grid[line_num][col_num] = _is_live(padded_grid, (line_num + 1, col_num + 1))
	return new_grid

def silver(input_lines):
	grid = _parse(input_lines)
	for i in range(100):
		grid = _next_position(grid)
	return Util.directions.Count(grid, 1)

def gold(input_lines):
	grid = _parse(input_lines)
	for i in range(100):
		grid = _next_position(grid)
		grid[0][0] = 1
		grid[0][-1] = 1
		grid[-1][-1] = 1
		grid[-1][0] = 1
	return Util.directions.Count(grid, 1)
