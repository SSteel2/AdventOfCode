import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _distance1D(a, b, empty_locations, multiplier):
	small = min(a, b)
	big = max(a, b)
	distance = big - small
	longs = empty_locations[big] - empty_locations[small]
	return longs * multiplier + distance

def _distances1D(location_frequencies, locations, empty_locations, multiplier):
	distance_sum = 0
	for i in range(len(locations)):
		for j in range(i + 1, len(locations)):
			distance_sum += (_distance1D(locations[i], locations[j], empty_locations, multiplier) * location_frequencies[locations[i]] * location_frequencies[locations[j]])
	return distance_sum

def _findEmptyLocations(locations, size):
	empty_locations = []
	current_value = 0
	for i in range(size):
		if i not in locations:
			current_value += 1
		empty_locations.append(current_value)
	return empty_locations

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

	empty_cols = _findEmptyLocations(stars_cols_keys, len(galaxy[0]))
	empty_rows = _findEmptyLocations(stars_rows_keys, len(galaxy))

	multiplier = expansion_multiplier - 1
	return _distances1D(stars_rows, stars_rows_keys, empty_rows, multiplier) + _distances1D(stars_cols, stars_cols_keys, empty_cols, multiplier)

def silver(input_lines):
	return _findStarDistances(input_lines, 2)

def gold(input_lines):
	return _findStarDistances(input_lines, 1000000)
