import Util.input
import Util.directions
from collections import deque

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def bfs(start, grid, check_visited):
	count = 0
	next_locations = deque([start])
	visited = set()
	while len(next_locations) != 0:
		current_location = next_locations.pop()
		if check_visited:
			if current_location in visited:
				continue
			visited.add(current_location)
		current_value = int(Util.directions.Get(grid, current_location))
		if current_value == 9:
			count += 1
			continue
		for direction in Util.directions.DirectionsTable:
			new_location = Util.directions.Move(current_location, direction)
			if Util.directions.IsOutOfBounds(grid, new_location):
				continue
			if int(Util.directions.Get(grid, new_location)) != current_value + 1:
				continue
			next_locations.appendleft(new_location)
	return count

def _solution(input_lines, check_visited):
	count = 0
	for line_num, line in enumerate(input_lines):
		for col_num, col in enumerate(line):
			if col == '0':
				current = bfs((line_num, col_num), input_lines, check_visited)
				count += current
	return count	

def silver(input_lines):
	return _solution(input_lines, True)

def gold(input_lines):
	return _solution(input_lines, False)
