import Util.input
import pprint

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _getStart(grid):
	for i, char in enumerate(grid[0]):
		if char == 'S':
			return (0, i)

def silver(input_lines):
	start = _getStart(input_lines)
	beams = set([start[1]])
	split_count = 0
	for line in input_lines:
		next_beams = set()
		for beam in beams:
			if line[beam] == '^':
				split_count += 1
				next_beams.add(beam - 1)
				next_beams.add(beam + 1)
			else:
				next_beams.add(beam)
		beams = next_beams
	return split_count

def gold(input_lines):
	start = _getStart(input_lines)
	beams = {start[1]: 1}
	for line in input_lines:
		next_beams = {}
		for beam in beams:
			if line[beam] == '^':
				if beam - 1 in next_beams:
					next_beams[beam - 1] += beams[beam]
				else:
					next_beams[beam - 1] = beams[beam]
				if beam + 1 in next_beams:
					next_beams[beam + 1] += beams[beam]
				else:
					next_beams[beam + 1] = beams[beam]
			else:
				if beam in next_beams:
					next_beams[beam] += beams[beam]
				else:
					next_beams[beam] = beams[beam]
		# print(next_beams.values())
		beams = next_beams
	total_count = 0
	for beam in beams:
		total_count += beams[beam]
	return total_count