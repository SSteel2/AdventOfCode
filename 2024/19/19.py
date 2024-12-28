import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(input_lines):
	first_part = True
	supply = []
	patterns = []
	for line in input_lines:
		if line == "":
			first_part = False
			continue
		if first_part:
			supply = line.split(', ')
		else:
			patterns.append(line)
	return supply, patterns

arrangable_patterns = {}
def _is_arrangable(supply, pattern):
	if len(pattern) == 0:
		return 1
	if pattern in arrangable_patterns:
		return arrangable_patterns[pattern]
	for i in supply:
		if pattern.startswith(i):
			if _is_arrangable(supply, pattern[len(i):]):
				arrangable_patterns[pattern] = 1
				return 1
	arrangable_patterns[pattern] = 0
	return 0

arrangement_counts = {}
def _arrangement_count(supply, pattern):
	if len(pattern) == 0:
		return 1
	if pattern in arrangement_counts:
		return arrangement_counts[pattern]
	arrangement_count = 0
	for i in supply:
		if pattern.startswith(i):
			arrangement_count += _arrangement_count(supply, pattern[len(i):])
	arrangement_counts[pattern] = arrangement_count
	return arrangement_count

def _solution(input_lines, count_function):
	supply, patterns = _parse(input_lines)
	count = 0
	for pattern in patterns:
		count += count_function(supply, pattern)
	return count

def silver(input_lines):
	return _solution(input_lines, _is_arrangable)

def gold(input_lines):
	return _solution(input_lines, _arrangement_count)
