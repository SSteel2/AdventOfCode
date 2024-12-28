import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def encode_pattern(pattern, locks, keys):
	combination = [line.count('#') for line in pattern]
	symbol = pattern[0][0]
	if symbol == '.':
		keys.append(tuple(combination))
	else:
		locks.append(tuple(combination))

def _parse(input_lines):
	pattern = [[] for _ in range(5)]
	locks = []
	keys = []
	for line in input_lines:
		if line == '':
			encode_pattern(pattern, locks, keys)
			pattern = [[] for _ in range(5)]
			continue
		for col_num, col in enumerate(line):
			pattern[col_num].append(col)
	encode_pattern(pattern, locks, keys)	
	return locks, keys

def silver(input_lines):
	locks, keys = _parse(input_lines)
	count = 0
	for lock in locks:
		for key in keys:
			count += all([sum(i) <= 7 for i in zip(lock, key)])
	return count

def gold(input_lines):
	pass
