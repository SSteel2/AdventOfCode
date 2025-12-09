import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(line):
	return tuple(int(i) for i in line.split(','))

def silver(input_lines):
	positions = Util.input.ParseInputLines(input_lines, _parse)
	max_area = 0
	for a in positions:
		for b in positions:
			area = (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)
			if area > max_area:
				max_area = area
	return max_area

def _is_positions_in_rectangle(rectangle, positions):
	rectangle_min_x = min(rectangle[0][0], rectangle[1][0])
	rectangle_max_x = max(rectangle[0][0], rectangle[1][0])
	rectangle_min_y = min(rectangle[0][1], rectangle[1][1])
	rectangle_max_y = max(rectangle[0][1], rectangle[1][1])
	for position in positions:
		if position[0] > rectangle_min_x and position[0] < rectangle_max_x and position[1] > rectangle_min_y and position[1] < rectangle_max_y:
			return False
	return True

def _is_point_in_positions_x(point, positions):
	# calculating winding number by assuming a line in x+ axis
	if positions[0][0] == positions[1][0]:
		paired_range = range(0, len(positions), 2)
	else:
		paired_range = range(-1, len(positions) - 1, 2)
	border_reached = False
	winding_number = 0
	for i in paired_range:
		if positions[i][0] <= point[0]:
			continue
		elif positions[i][1] > point[1] and positions[i + 1][1] < point[1]:
			winding_number += 2
		elif positions[i][1] < point[1] and positions[i + 1][1] > point[1]:
			winding_number -= 2
		elif positions[i][1] > point[1] and positions[i + 1][1] == point[1] or positions[i][1] == point[1] and positions[i + 1][1] < point[1]:
			winding_number += 1
		elif positions[i][1] < point[1] and positions[i + 1][1] == point[1] or positions[i][1] == point[1] and positions[i + 1][1] > point[1]:
			winding_number -= 1
		if winding_number == 2 or winding_number == -2:
			border_reached = True
		elif winding_number == 0 and border_reached:
			return False
	return winding_number != 0

def _is_point_in_positions_y(point, positions):
	# calculating winding number by assuming a line in y+ axis
	if positions[0][1] == positions[1][1]:
		paired_range = range(0, len(positions), 2)
	else:
		paired_range = range(-1, len(positions) - 1, 2)
	border_reached = False
	winding_number = 0
	for i in paired_range:
		if positions[i][1] <= point[1]:
			continue
		elif positions[i][0] > point[0] and positions[i + 1][0] < point[0]:
			winding_number += 2
		elif positions[i][0] < point[0] and positions[i + 1][0] > point[0]:
			winding_number -= 2
		elif positions[i][0] > point[0] and positions[i + 1][0] == point[0] or positions[i][0] == point[0] and positions[i + 1][0] < point[0]:
			winding_number += 1
		elif positions[i][1] < point[1] and positions[i + 1][0] == point[0] or positions[i][0] == point[0] and positions[i + 1][0] > point[0]:
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
	return _is_point_in_positions_x(top_left, positions) and _is_point_in_positions_x(bottom_left, positions) and _is_point_in_positions_y(top_left, positions) and _is_point_in_positions_y(top_right, positions)


def gold(input_lines):
	positions = Util.input.ParseInputLines(input_lines, _parse)
	max_area = 0
	for a in positions:
		for b in positions:
			area = (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)
			if area > max_area:
				if _is_positions_in_rectangle((a, b), positions) and _is_rectangle_in_positions((a, b), positions):
					max_area = area
	return max_area
