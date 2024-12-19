import Util.input
import Util.directions
import Util.PriorityQueue

MAP_SIZE = 71
INITIAL_COORDINATES = 1024

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parseLine(line):
	split_line = line.split(',')
	return (int(split_line[0]), int(split_line[1]))

def _manhattan_distance(a, b):
	return abs(a[0] - b[0]) + abs(a[1] - b[1])

def _find_shortest_path(grid, start, end):
	temp_grid = [[i for i in j] for j in grid]
	queue = Util.PriorityQueue.PriorityQueue()
	queue.append(0, (start, []))
	while len(queue) > 0:
		current = queue.pop()
		Util.directions.Set(temp_grid, current[0], 'X')
		if current[0] == end:
			return current[1]
		for direction in Util.directions.DirectionsTable:
			new_location = Util.directions.Move(current[0], direction)
			if Util.directions.IsOutOfBounds(temp_grid, new_location):
				continue
			if Util.directions.Get(temp_grid, new_location) == '.':
				queue.append(len(current[1]) + 1 + _manhattan_distance(new_location, end), (new_location, current[1] + [new_location]))
	return None

def silver(input_lines):
	coordinates = Util.input.ParseInputLines(input_lines, _parseLine)
	grid = [['.' for i in range(MAP_SIZE)] for j in range(MAP_SIZE)]
	for coordinate in coordinates[:INITIAL_COORDINATES]:
		Util.directions.Set(grid, coordinate, '#')
	return len(_find_shortest_path(grid, (0, 0), (MAP_SIZE - 1, MAP_SIZE - 1)))

def gold(input_lines):
	coordinates = Util.input.ParseInputLines(input_lines, _parseLine)
	grid = [['.' for i in range(MAP_SIZE)] for j in range(MAP_SIZE)]
	for coordinate in coordinates[:INITIAL_COORDINATES]:
		Util.directions.Set(grid, coordinate, '#')

	shortest_path = _find_shortest_path(grid, (0, 0), (MAP_SIZE - 1, MAP_SIZE - 1))
	for coordinate in coordinates[INITIAL_COORDINATES:]:
		Util.directions.Set(grid, coordinate, '#')
		if coordinate in shortest_path:
			shortest_path = _find_shortest_path(grid, (0, 0), (MAP_SIZE - 1, MAP_SIZE - 1))
			if shortest_path == None:
				return ','.join([str(i) for i in coordinate])
