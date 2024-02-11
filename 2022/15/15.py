import Util.input
import Util.ranges
import math

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(line):
	split_line = line.split('=')
	sensor_x = int(split_line[1].split(',')[0])
	sensor_y = int(split_line[2].split(':')[0])
	beacon_x = int(split_line[3].split(',')[0])
	beacon_y = int(split_line[4])
	return {'sensor': (sensor_y, sensor_x), 'beacon': (beacon_y, beacon_x)}

def _manhattanDistance(point1, point2):
	return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

def silver(input_lines):
	sensors = Util.input.ParseInputLines(input_lines, _parse)
	test_location_y = 2000000
	beacons_at_test_location = set()
	impossible_locations = Util.ranges.Spans()
	for sensor in sensors:
		if sensor['beacon'][0] == test_location_y:
			beacons_at_test_location.add(sensor['beacon'])
		distance = _manhattanDistance(sensor['sensor'], sensor['beacon'])
		distance_to_test_location = abs(sensor['sensor'][0] - test_location_y)
		remaining_distance = distance - distance_to_test_location
		if remaining_distance < 0:
			continue
		width_at_test_location = 2 * (distance - distance_to_test_location) + 1
		impossible_locations.union(Util.ranges.Spans(Util.ranges.Span(sensor['sensor'][1] - remaining_distance, sensor['sensor'][1] + remaining_distance + 1)))
	return len(impossible_locations) - len(beacons_at_test_location)

def gold(input_lines):
	sensors = Util.input.ParseInputLines(input_lines, _parse)
	for sensor in sensors:
		sensor['beacon_distance'] = _manhattanDistance(sensor['sensor'], sensor['beacon'])
	critical_sensors = []
	for i in range(len(sensors)):
		for j in range(i + 1, len(sensors)):
			distance = _manhattanDistance(sensors[i]['sensor'], sensors[j]['sensor'])
			if distance - sensors[i]['beacon_distance'] - sensors[j]['beacon_distance'] == 2:
				critical_sensors.append(sensors[i])
				critical_sensors.append(sensors[j])

	lowest_y = math.inf
	lowest_index = -1
	for i, sensor in enumerate(critical_sensors):
		if sensor['sensor'][0] < lowest_y:
			lowest_y = sensor['sensor'][0]
			lowest_index = i
	if lowest_index % 2 == 0:
		highest_index = lowest_index + 1
	else:
		highest_index = lowest_index - 1

	if lowest_index // 2 == 0:
		if critical_sensors[2]['sensor'][1] < critical_sensors[3]['sensor'][1]:
			left_index = 2
			right_index = 3
		else:
			left_index = 3
			right_index = 2
	else:
		if critical_sensors[0]['sensor'][1] < critical_sensors[1]['sensor'][1]:
			left_index = 0
			right_index = 1
		else:
			left_index = 1
			right_index = 0

	left_leaning = critical_sensors[lowest_index]['sensor'][1] > critical_sensors[highest_index]['sensor'][1]
	missing_beacon = (critical_sensors[lowest_index]['sensor'][0] + critical_sensors[lowest_index]['beacon_distance'] + 1, critical_sensors[lowest_index]['sensor'][1])
	distance_missing = (_manhattanDistance(missing_beacon, critical_sensors[left_index]['sensor']) - critical_sensors[left_index]['beacon_distance'] - 1) // 2
	missing_beacon = (missing_beacon[0] - distance_missing, missing_beacon[1] - distance_missing * (1 if left_leaning else -1))
	return missing_beacon[1] * 4000000 + missing_beacon[0]
