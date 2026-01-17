import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(line):
	return tuple(int(i) for i in line.split(','))

def _solve(input_lines, predicate):
	positions = Util.input.ParseInputLines(input_lines, _parse)
	max_area = 0
	for i in range(len(positions)):
		for j in range(i, len(positions)):
			area = (abs(positions[i][0] - positions[j][0]) + 1) * (abs(positions[i][1] - positions[j][1]) + 1)
			if area > max_area and predicate((positions[i], positions[j]), positions):
				max_area = area
	return max_area

def silver(input_lines):
	return _solve(input_lines, lambda point, points: True)

def _is_positions_in_rectangle(rectangle, positions):
	rectangle_min_x = min(rectangle[0][0], rectangle[1][0])
	rectangle_max_x = max(rectangle[0][0], rectangle[1][0])
	rectangle_min_y = min(rectangle[0][1], rectangle[1][1])
	rectangle_max_y = max(rectangle[0][1], rectangle[1][1])
	for position in positions:
		if position[0] > rectangle_min_x and position[0] < rectangle_max_x and position[1] > rectangle_min_y and position[1] < rectangle_max_y:
			return False
	return True

def _is_point_in_positions(point, positions, coordinate):
	# calculating winding number by assuming a line in x+ axis
	# coordinate is either 0 - x or 1 - y
	opposite_coordinate = (coordinate + 1) % 2
	if positions[0][coordinate] == positions[1][coordinate]:
		paired_range = range(0, len(positions), 2)
	else:
		paired_range = range(-1, len(positions) - 1, 2)
	border_reached = False
	winding_number = 0
	for i in paired_range:
		if positions[i][coordinate] <= point[coordinate]:
			continue
		elif positions[i][opposite_coordinate] > point[opposite_coordinate] and positions[i + 1][opposite_coordinate] < point[opposite_coordinate]:
			winding_number += 2
		elif positions[i][opposite_coordinate] < point[opposite_coordinate] and positions[i + 1][opposite_coordinate] > point[opposite_coordinate]:
			winding_number -= 2
		elif positions[i][opposite_coordinate] > point[opposite_coordinate] and positions[i + 1][opposite_coordinate] == point[opposite_coordinate] \
				or positions[i][opposite_coordinate] == point[opposite_coordinate] and positions[i + 1][opposite_coordinate] < point[opposite_coordinate]:
			winding_number += 1
		elif positions[i][opposite_coordinate] < point[opposite_coordinate] and positions[i + 1][opposite_coordinate] == point[opposite_coordinate] \
				or positions[i][opposite_coordinate] == point[opposite_coordinate] and positions[i + 1][opposite_coordinate] > point[opposite_coordinate]:
			winding_number -= 1
		if winding_number == 2 or winding_number == -2:
			border_reached = True
		elif winding_number == 0 and border_reached:
			return False
	return winding_number != 0

def _is_rectangle_in_positions(rectangle, positions):
	top_left = (min(rectangle[0][0], rectangle[1][0]), min(rectangle[0][1], rectangle[1][1]))
	bottom_left = (min(rectangle[0][0], rectangle[1][0]), max(rectangle[0][1], rectangle[1][1]))
	top_right = (max(rectangle[0][0], rectangle[1][0]), min(rectangle[0][1], rectangle[1][1]))
	return _is_point_in_positions(top_left, positions, 0) and _is_point_in_positions(bottom_left, positions, 0) \
		and _is_point_in_positions(top_left, positions, 1) and _is_point_in_positions(top_right, positions, 1)

def gold(input_lines):
	return _solve(input_lines, lambda point, points: _is_positions_in_rectangle(point, points) and _is_rectangle_in_positions(point, points))
