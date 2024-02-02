import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _distance(a, b, empty_rows, empty_cols, multiplier):
	min_rows = min(a[0], b[0])
	max_rows = max(a[0], b[0])
	min_cols = min(a[1], b[1])
	max_cols = max(a[1], b[1])

	distance = max_rows - min_rows + max_cols - min_cols
	longs = empty_rows[max_rows] - empty_rows[min_rows] + empty_cols[max_cols] - empty_cols[min_cols]
	return longs * (multiplier - 1) + distance

def _findStarDistances(galaxy, expansion_multiplier):
	empty_cols = []
	current_value = 0
	for i in range(len(galaxy[0])):
		if all(galaxy[j][i] == '.' for j in range(len(galaxy[0]))):
			current_value += 1
		empty_cols.append(current_value)

	empty_rows = []
	current_value = 0
	for i, values in enumerate(galaxy):
		if all(j == '.' for j in values):
			current_value += 1
		empty_rows.append(current_value)

	stars = []
	for i, line in enumerate(galaxy):
		for j, val in enumerate(line):
			if val == '#':
				stars.append((i, j))

	distance_sum = 0
	for i in range(len(stars)):
		for j in range(i + 1, len(stars)):
			distance_sum += _distance(stars[i], stars[j], empty_rows, empty_cols, expansion_multiplier)
	return distance_sum

def silver(input_lines):
	return _findStarDistances(input_lines, 2)

def gold(input_lines):
	return _findStarDistances(input_lines, 1000000)
