import Util.input
from itertools import permutations
from math import inf

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(input_lines):
	happiness_map = {}
	for line in input_lines:
		split_line = line.split(' ')
		happiness = int(split_line[3])
		if split_line[2] == 'lose':
			happiness *= -1
		name = split_line[0]
		if name in happiness_map:
			happiness_map[name][split_line[-1][:-1]] = happiness
		else:
			happiness_map[name] = {split_line[-1][:-1]: happiness}
	return happiness_map

def _calculate_happiness(seating_arrangement, happiness_map):
	total = 0
	for index in range(len(seating_arrangement) - 1):
		total += happiness_map[seating_arrangement[index]][seating_arrangement[index + 1]]
		total += happiness_map[seating_arrangement[index + 1]][seating_arrangement[index]]
	total += happiness_map[seating_arrangement[0]][seating_arrangement[-1]]
	total += happiness_map[seating_arrangement[-1]][seating_arrangement[0]]
	return total

def _add_me(happiness_map):
	names = happiness_map.keys()
	happiness_map['me'] = {}
	for i in names:
		happiness_map[i]['me'] = 0
		happiness_map['me'][i] = 0

def _find_max_happiness(happiness_map):
	max_happiness = -inf
	for i in permutations(happiness_map.keys()):
		happiness = _calculate_happiness(i, happiness_map)
		max_happiness = max(max_happiness, happiness)
	return max_happiness

def silver(input_lines):
	happiness_map = _parse(input_lines)
	return _find_max_happiness(happiness_map)

def gold(input_lines):
	happiness_map = _parse(input_lines)
	_add_me(happiness_map)
	return _find_max_happiness(happiness_map)
