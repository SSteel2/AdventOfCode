import math
import Util.input
import Util.PriorityQueue
import Util.directions

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(input_lines):
	heightmap = [[0 for _ in range(len(input_lines[0]))] for _ in range(len(input_lines))]
	for l, line in enumerate(input_lines):
		for c, col in enumerate(line):
			if col == 'S':
				start = (l, c)
				heightmap[l][c] = ord('a')
			elif col == 'E':
				end = (l, c)
				heightmap[l][c] = ord('z')
			else:
				heightmap[l][c] = ord(col)
	return heightmap, start, end

def _get(matrix, location):
	return matrix[location[0]][location[1]]

def _set(matrix, location, value):
	matrix[location[0]][location[1]] = value

def _manhattanDistance(point1, point2):
	return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

def _isOutOfBounds(location, input_lines):
	return location[0] >= len(input_lines) or location[0] < 0 or location[1] >= len(input_lines[0]) or location[1] < 0

def _isClimbPossible(heightmap, current, new_location):
	return _get(heightmap, current) + 1 >= _get(heightmap, new_location)

def _isClimbPossibleReverse(heightmap, current, new_location):
	return _get(heightmap, current) <= _get(heightmap, new_location) + 1

def _findDistances(input_lines, start, end, climbFunction):
	distance = [[math.inf for _ in range(len(input_lines[0]))] for _ in range(len(input_lines))]
	_set(distance, start, 0)
	queue = Util.PriorityQueue.PriorityQueue()
	queue.append(_manhattanDistance(start, end), start)
	while len(queue) > 0:
		current = queue.pop()
		for direction in Util.directions.DirectionsTable:
			new_location = Util.directions.Move(current, direction)
			if _isOutOfBounds(new_location, input_lines) or not climbFunction(input_lines, current, new_location):
				continue
			new_distance = _get(distance, current) + 1
			if new_distance >= _get(distance, new_location):
				continue
			_set(distance, new_location, new_distance)
			estimate = _manhattanDistance(new_location, end)
			queue.append(new_distance + estimate, new_location)
	return distance

def silver(input_lines):
	heightmap, start, end = _parse(input_lines)
	distances = _findDistances(heightmap, start, end, _isClimbPossible)
	return _get(distances, end)

def gold(input_lines):
	heightmap, start, end = _parse(input_lines)
	distances = _findDistances(heightmap, end, start, _isClimbPossibleReverse)
	min_distance = math.inf
	for i in range(len(heightmap)):
		distance = _get(distances, (i, 0))
		if distance < min_distance:
			min_distance = distance
	return min_distance
