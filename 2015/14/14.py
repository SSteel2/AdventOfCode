import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parseLine(line):
	split_line = line.split(' ')
	return {'name': split_line[0], 'speed': int(split_line[3]), 'duration': int(split_line[6]), 'rest': int(split_line[-2])}

def _distance_traveled(reindeer, time):
	cycle_time = reindeer['duration'] + reindeer['rest']
	full_cycles = time // cycle_time
	remaining_time = time % cycle_time
	cycle_distance = reindeer['duration'] * reindeer['speed']
	additional_time = min(remaining_time, reindeer['duration'])
	additional_distance = additional_time * reindeer['speed']
	return cycle_distance * full_cycles + additional_distance

def silver(input_lines):
	reindeers = Util.input.ParseInputLines(input_lines, _parseLine)
	max_distance = 0
	for i in reindeers:
		distance = _distance_traveled(i, 2503)
		if distance > max_distance:
			max_distance = distance
	return max_distance

def gold(input_lines):
	reindeers = Util.input.ParseInputLines(input_lines, _parseLine)
	points = {}
	for i in reindeers:
		points[i['name']] = 0
	for time in range(1, 2504):
		winning_distance = -1
		winners = []
		for reindeer in reindeers:
			distance = _distance_traveled(reindeer, time)
			if distance > winning_distance:
				winning_distance = distance
				winners = [reindeer['name']]
			elif distance == winning_distance:
				winners.append(reindeer['name'])
		for winner in winners:
			points[winner] += 1
	max_points = 0
	for i in points:
		if points[i] > max_points:
			max_points = points[i]
	return max_points
