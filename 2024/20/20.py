import Util.input
import Util.directions
import Util.PriorityQueue
import Util.Frequency

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(input_lines):
	return [[{'block': i, 'steps': -1} for i in line] for line in input_lines]

def _find_shortest_path(grid, start, end):
	temp_grid = [[i['block'] for i in j] for j in grid]
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
			if (block := Util.directions.Get(temp_grid, new_location)) != '#' and block != 'X':
				queue.append(len(current[1]) + 1, (new_location, current[1] + [new_location]))
	return None

def _find(grid, marker):
	for line_num, line in enumerate(grid):
		for col_num, col in enumerate(line):
			if col['block'] == marker:
				return (line_num, col_num)

def _get_all_locations_at_distance(location, distance):
	result = ['.' for i in range(distance * 4)]
	for i in range(distance):
		result[i * 4] = (location[0] + distance - i, location[1] + i)
		result[i * 4 + 1] = (location[0] - i, location[1] + distance - i)
		result[i * 4 + 2] = (location[0] - distance + i, location[1] - i)
		result[i * 4 + 3] = (location[0] + i, location[1] - distance + i)
	return result

def _find_cheats(grid, location, max_distance):
	cheats = 0
	location_value = Util.directions.Get(grid, location)
	for distance in range(2, max_distance + 1):
		possible_skips = _get_all_locations_at_distance(location, distance)
		for skip in possible_skips:
			if Util.directions.IsOutOfBounds(grid, skip):
				continue
			skip_value = Util.directions.Get(grid, skip)
			if skip_value['block'] != '#' and skip_value['steps'] - location_value['steps'] - distance >= 100:
				cheats += 1
	return cheats

def _solution(input_lines, max_distance):
	grid = _parse(input_lines)
	start = _find(grid, 'S')
	end = _find(grid, 'E')
	path = _find_shortest_path(grid, start, end)
	path = [start] + path
	for index, step in enumerate(path):
		Util.directions.Get(grid, step)['steps'] = index
	cheats = 0
	for step in path:
		cheats += _find_cheats(grid, step, max_distance)
	return cheats

def silver(input_lines):
	return _solution(input_lines, 2)

def gold(input_lines):
	return _solution(input_lines, 20)
