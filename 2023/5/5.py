input_lines = []
with open('input.txt', 'r') as input_file:
	for line in input_file:
		input_lines.append(line.removesuffix('\n'))

class Range:
	def __init__(self, start, length):
		self.start = start
		self.length = length

	def __str__(self):
		return f"Range({self.start}, {self.length})"

	def __repr__(self):
		return self.__str__()

	def __lt__(self, other):
		return self.start < other.start

	def intersection(self, span):
		# self |----|............|--|
		# span ........|------|......
		if span.start + span.length <= self.start or self.start + self.length <= span.start:
			return []
		# self |----...........
		# span .....|------|...
		if self.start < span.start:
			# self |-----xx|.......
			# span .....|------|...
			if self.start + self.length <= span.start + span.length:
				return [Range(span.start, self.start + self.length - span.start)]
			# self |-----xxxxxx--|.
			# span .....|------|...
			if self.start + self.length > span.start + span.length:
				return [Range(span.start, span.length)]
		# self ......|--.....
		# span ...|------|...
		if self.start >= span.start and self.start < span.start + span.length:
			# self ......|xx|....
			# span ...|------|...
			if self.start + self.length <= span.start + span.length:
				return [Range(self.start, self.length)]
			# self ......|xxx----|....
			# span ...|------|........
			if self.start + self.length > span.start + span.length:
				return [Range(self.start, span.start - self.start + span.length)]

	def isIntersecting(self, span):
		return not (span.start + span.length < self.start or self.start + self.length <= span.start)

	def difference(self, span):
		# self |xxxx|............|xx|
		# span ........|------|......
		if span.start + span.length <= self.start or self.start + self.length < span.start:
			return [Range(self.start, self.length)]
		# self |----...........
		# span .....|------|...
		if self.start < span.start:
			# self |xxxx---|.......
			# span .....|------|...
			if self.start + self.length <= span.start + span.length:
				return [Range(self.start, span.start - self.start)]
			# self |xxxx--------x|.
			# span .....|------|...
			if self.start + self.length > span.start + span.length:
				return [Range(self.start, span.start - self.start), Range(span.start + span.length, self.length - span.start + self.start - span.length)]
		# self ......|--.....
		# span ...|------|...
		if self.start >= span.start and self.start < span.start + span.length:
			# self ......|--|....
			# span ...|------|...
			if self.start + self.length <= span.start + span.length:
				return []
			# self ......|----xxx|....
			# span ...|------|........
			if self.start + self.length > span.start + span.length:
				return [Range(span.start + span.length, self.start - span.start + self.length - span.length)]

	def move(self, offset):
		self.start += offset

class Ranges:
	def __init__(self, span):
		self.ranges = [span]

	def __str__(self):
		return str(self.ranges)

	def __repr__(self):
		return self.__str__()

	def intersection(self, span):
		result = []
		for r in self.ranges:
			if r.isIntersecting(span):
				result.extend(r.intersection(span))
		return result

	def difference(self, span):
		result = []
		for r in self.ranges:
			#debug rr
			rr = r.difference(span)
			for i in rr:
				if i.length == 0:
					print(r, span, rr)
					break
			result.extend(rr)
		self.ranges = result


# Parse input
seeds = [int(i) for i in input_lines[0].split(': ')[1].split(' ')]

# Silver star
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
print('Silver answer: ' + str(current_locations[0]))

# Gold star
seed_ranges = [Range(i[0], i[1]) for i in zip(seeds[::2], seeds[1::2])]  # [(start, length), ...]

current_location_ranges = seed_ranges[:]
for current_map in maps:
	next_location_ranges = []
	for location_range in current_location_ranges:
		remaining_location_range = Ranges(location_range)
		for map_range in current_map['map']:
			current_map_range = Range(map_range['source'], map_range['length'])
			intersecting_ranges = remaining_location_range.intersection(current_map_range)
			for i in intersecting_ranges:
				i.move(map_range['dest'] - map_range['source'])
			next_location_ranges.extend(intersecting_ranges)
			remaining_location_range.difference(current_map_range)
		for i in remaining_location_range.ranges:
			next_location_ranges.append(i)
	current_location_ranges = next_location_ranges[:]

current_location_ranges.sort()
print('Gold answer: ' + str(current_location_ranges[0].start))
