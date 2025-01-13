import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(input_lines):
	aunts = {}
	for line in input_lines:
		split_line = line.split(' ')
		aunt_number = int(split_line[1][:-1])
		aunts[aunt_number] = {}
		for i in range(3):
			aunts[aunt_number][split_line[i * 2  + 2][:-1]] = int(split_line[i * 2 + 3].strip(','))
	return aunts

def _is_aunt_match(aunt, target_aunt):
	for parameter in aunt:
		if aunt[parameter] != target_aunt[parameter]:
			return False
	return True

def _is_aunt_match_gold(aunt, target_aunt):
	for parameter in aunt:
		if parameter == 'trees' or parameter == 'cats':
			if aunt[parameter] <= target_aunt[parameter]:
				return False
		elif parameter == 'pomeranians' or parameter == 'goldfish':
			if aunt[parameter] >= target_aunt[parameter]:
				return False
		elif aunt[parameter] != target_aunt[parameter]:
			return False
	return True

def _solve(input_lines, match_function):
	aunts = _parse(input_lines)
	target_aunt = {
		'children': 3,
		'cats': 7,
		'samoyeds': 2,
		'pomeranians': 3,
		'akitas': 0,
		'vizslas': 0,
		'goldfish': 5,
		'trees': 3,
		'cars': 2,
		'perfumes': 1
	}
	for i in aunts:
		if match_function(aunts[i], target_aunt):
			return i
	return -1


def silver(input_lines):
	return _solve(input_lines, _is_aunt_match)
	
def gold(input_lines):
	return _solve(input_lines, _is_aunt_match_gold)
