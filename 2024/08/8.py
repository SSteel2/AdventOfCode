import Util.input
import Util.directions

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(input_lines):
	antennae = {}
	for line_num, line in enumerate(input_lines):
		for col_num, col in enumerate(line):
			if col != '.':
				if col in antennae:
					antennae[col].append((line_num, col_num))
				else:
					antennae[col] = [(line_num, col_num)]
	return antennae

def _count_antinodes(grid):
	count = 0
	for line in grid:
		for col in line:
			if col == 'X':
				count += 1
	return count

def _place_antinode_silver(grid, antenna, vector):
	antinode = (antenna[0] + vector[0], antenna[1] + vector[1])
	if not Util.directions.IsOutOfBounds(grid, antinode):
		Util.directions.Set(grid, antinode, 'X')

def _place_antinode_gold(grid, antenna, vector):
	while not Util.directions.IsOutOfBounds(grid, antenna):
		Util.directions.Set(grid, antenna, 'X')
		antenna = (antenna[0] + vector[0], antenna[1] + vector[1])

def _place_antinodes(grid, antenna1, antenna2, placement_function):
	difference = (antenna2[0] - antenna1[0], antenna2[1] - antenna1[1])
	placement_function(grid, antenna1, (-difference[0], -difference[1]))
	placement_function(grid, antenna2, difference)

def _solution(input_lines, placement_function):
	antennae = _parse(input_lines)
	antinodes_grid = [['.' for i in range(len(input_lines[0]))] for j in range(len(input_lines))]
	for antenna in antennae:
		for index1 in range(len(antennae[antenna])):
			for index2 in range(index1 + 1, len(antennae[antenna])):
				placement_function(antinodes_grid, antennae[antenna][index1], antennae[antenna][index2])
	return _count_antinodes(antinodes_grid)

def silver(input_lines):
	return _solution(input_lines, lambda grid, antenna1, antenna2: _place_antinodes(grid, antenna1, antenna2, _place_antinode_silver))

def gold(input_lines):
	return _solution(input_lines, lambda grid, antenna1, antenna2: _place_antinodes(grid, antenna1, antenna2, _place_antinode_gold))
