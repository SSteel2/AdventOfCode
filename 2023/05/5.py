import Util.input
import Util.ranges

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parseMaps(input_lines):
	maps = []
	current_map = {}
	for line in input_lines[2:]:
		if line == '':
			maps.append(current_map)
			continue
		if 'map' in line:
			current_map = {'id': line.split(' ')[0], 'map': []}
			continue
		split_line = line.split(' ')
		current_map['map'].append({'source': int(split_line[1]), 'dest': int(split_line[0]), 'length': int(split_line[2])})
	return maps

def silver(input_lines):
	seeds = [int(i) for i in input_lines[0].split(': ')[1].split(' ')]
	maps = _parseMaps(input_lines)

	current_locations = seeds[:]
	next_locations = []
	for current_map in maps:
		for location in current_locations:
			location_found = False
			for map_range in current_map['map']:
				if location >= map_range['source'] and location < map_range['source'] + map_range['length']:
					next_locations.append(location - map_range['source'] + map_range['dest'])
					location_found = True
					break
			if not location_found:
				next_locations.append(location)
		current_locations = next_locations[:]
		next_locations = []

	current_locations.sort()
	return current_locations[0]

def gold(input_lines):
	seeds = [int(i) for i in input_lines[0].split(': ')[1].split(' ')]
	seed_ranges = [Util.ranges.Span(i[0], i[0] + i[1]) for i in zip(seeds[::2], seeds[1::2])]
	maps = _parseMaps(input_lines)

	current_location_ranges = seed_ranges[:]
	for current_map in maps:
		next_location_ranges = []
		for location_range in current_location_ranges:
			remaining_location_range = Util.ranges.Spans(location_range)
			for map_range in current_map['map']:
				current_map_range = Util.ranges.Span(map_range['source'], map_range['source'] + map_range['length'])
				intersecting_ranges = remaining_location_range.intersection(current_map_range)
				for i in intersecting_ranges:
					i.move(map_range['dest'] - map_range['source'])
				next_location_ranges.extend(intersecting_ranges)
				remaining_location_range.subtract(current_map_range)
			for i in remaining_location_range.spans:
				next_location_ranges.append(i)
		current_location_ranges = next_location_ranges[:]

	current_location_ranges.sort()
	return current_location_ranges[0].start
