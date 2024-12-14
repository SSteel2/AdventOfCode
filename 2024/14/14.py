import Util.input
import Util.directions
import Util.Frequency

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parseLine(line):
	coordinates = [i[2:] for i in line.split(' ')]
	return {'position': tuple(int(i) for i in coordinates[0].split(',')), 'velocity': tuple(int(i) for i in coordinates[1].split(','))}

def _move_robot(robot, moves_count):
	new_position = Util.directions.MoveMultipleCustom(robot['position'], robot['velocity'], moves_count)
	robot['position'] = (new_position[0] % 101, new_position[1] % 103)

def _quadrant_score(robots):
	quadrants = [0 for i in range(4)]
	for robot in robots:
		quadrant = 0
		if robot['position'][0] == 50 or robot['position'][1] == 51:
			continue
		if robot['position'][0] > 50:
			quadrant += 2
		if robot['position'][1] > 51:
			quadrant += 1
		quadrants[quadrant] += 1
	return quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]

def silver(input_lines):
	robots = Util.input.ParseInputLines(input_lines, _parseLine)
	for robot in robots:
		_move_robot(robot, 100)
	return _quadrant_score(robots)

def _calculate_neigbours(positions):
	neighbours = 0
	for position in positions:
		for direction in Util.directions.DirectionsTable:
			possible_neighbour_location = Util.directions.Move(position, direction)
			if possible_neighbour_location in positions:
				neighbours += 1
	return neighbours

def _draw_robots(robots):
	grid = [['.' for i in range(103)] for j in range(101)]
	for robot in robots:
		Util.directions.Set(grid, robot['position'], '#')
	Util.directions.PrintTable(grid)

def gold(input_lines):
	robots = Util.input.ParseInputLines(input_lines, _parseLine)
	# total_neighbours = Util.Frequency.Frequency()
	for i in range(10000):	
		positions = set()
		for robot in robots:
			_move_robot(robot, 1)
			positions.add(robot['position'])
		current_neighbours = _calculate_neigbours(positions)
		if current_neighbours > 500: # high neighbourlieness means something is cooking
			return i + 1
			# _draw_robots(robots)
		# total_neighbours.add(current_neighbours)
	# print(sorted(total_neighbours.keys()))
