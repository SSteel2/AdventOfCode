import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _distance(a, b, empty_rows, empty_cols, multiplier):
	distance = abs(a[0] - b[0]) + abs(a[1] - b[1])
	longs = len([i for i in empty_rows if i > min(a[0], b[0]) and i < max(a[0], b[0])]) + len([i for i in empty_cols if i > min(a[1], b[1]) and i < max(a[1], b[1])])
	return longs * (multiplier - 1) + distance

def _findStarDistances(galaxy, expansion_multiplier):
	empty_cols = []
	for i in range(len(galaxy[0])):
		if all(galaxy[j][i] == '.' for j in range(len(galaxy[0]))):
			empty_cols.append(i)
	empty_rows = []
	for i, values in enumerate(galaxy):
		if all(j == '.' for j in values):
			empty_rows.append(i)

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
