import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _findEmptyLocations(locations, size):
	empty_locations = []
	current_value = 0
	for i in range(size):
		if i not in locations:
			current_value += 1
		empty_locations.append(current_value)
	return empty_locations

def _makeStarClusters(location_keys, empty_locations, star_frequncies):
	star_clusters = {}
	for i in location_keys:
		if empty_locations[i] not in star_clusters:
			star_clusters[empty_locations[i]] = star_frequncies[i]
		else:
			star_clusters[empty_locations[i]] += star_frequncies[i]
	return star_clusters

def _calculateClusterDistances(star_clusters):
	star_clusters_keys = list(star_clusters.keys())
	distance = 0
	for i in range(len(star_clusters_keys)):
		for j in range(i + 1, len(star_clusters_keys)):
			distance += ((star_clusters_keys[j] - star_clusters_keys[i]) * star_clusters[star_clusters_keys[i]] * star_clusters[star_clusters_keys[j]])
	return distance

def _calculateDistances(stars, star_keys):
	distance = 0
	for i in range(len(star_keys)):
		for j in range(i + 1, len(star_keys)):
			distance += ((star_keys[j] - star_keys[i]) * stars[star_keys[i]] * stars[star_keys[j]])
	return distance

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
	stars_cols_keys = sorted(list(stars_cols.keys()))

	empty_rows = _findEmptyLocations(stars_rows_keys, len(galaxy))
	empty_cols = _findEmptyLocations(stars_cols_keys, len(galaxy[0]))

	stars_rows_clusters = _makeStarClusters(stars_rows_keys, empty_rows, stars_rows)
	stars_cols_clusters = _makeStarClusters(stars_cols_keys, empty_cols, stars_cols)

	total_distance = (_calculateClusterDistances(stars_rows_clusters) + _calculateClusterDistances(stars_cols_clusters)) * (expansion_multiplier - 1)
	total_distance += _calculateDistances(stars_rows, stars_rows_keys) + _calculateDistances(stars_cols, stars_cols_keys)
	return total_distance

def silver(input_lines):
	return _findStarDistances(input_lines, 2)

def gold(input_lines):
	return _findStarDistances(input_lines, 1000000)
