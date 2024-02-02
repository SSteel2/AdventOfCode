import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _distance1D(a, b, empty_locations, multiplier):
	small = min(a, b)
	big = max(a, b)
	distance = big - small
	longs = empty_locations[big] - empty_locations[small]
	return longs * multiplier + distance

def _findStarDistances(galaxy, expansion_multiplier):
	stars_rows = {}
	stars_cols = {}
	for i, line in enumerate(galaxy):
		for j, val in enumerate(line):
			if val == '#':
				if i not in stars_rows:
					stars_rows[i] = 1
				else:
					stars_rows[i] += 1
				if j not in stars_cols:
					stars_cols[j] = 1
				else:
					stars_cols[j] += 1
	stars_rows_keys = list(stars_rows.keys())
	stars_cols_keys = list(stars_cols.keys())

	empty_cols = []
	current_value = 0
	for i in range(len(galaxy[0])):
		if i not in stars_cols_keys:
			current_value += 1
		empty_cols.append(current_value)

	empty_rows = []
	current_value = 0
	for i, values in enumerate(galaxy):
		if i not in stars_rows_keys:
			current_value += 1
		empty_rows.append(current_value)

	distance_sum = 0
	multiplier = expansion_multiplier - 1
	for i in range(len(stars_rows_keys)):
		for j in range(i + 1, len(stars_rows_keys)):
			distance_sum += (_distance1D(stars_rows_keys[i], stars_rows_keys[j], empty_rows, multiplier) * stars_rows[stars_rows_keys[i]] * stars_rows[stars_rows_keys[j]])
	for i in range(len(stars_cols_keys)):
		for j in range(i + 1, len(stars_cols_keys)):
			distance_sum += (_distance1D(stars_cols_keys[i], stars_cols_keys[j], empty_cols, multiplier) * stars_cols[stars_cols_keys[i]] * stars_cols[stars_cols_keys[j]])
	return distance_sum

def silver(input_lines):
	return _findStarDistances(input_lines, 2)

def gold(input_lines):
	return _findStarDistances(input_lines, 1000000)
