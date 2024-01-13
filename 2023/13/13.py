import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parseLines(input_lines):
	patterns = []
	pattern = []
	for i in input_lines:
		if i == '':
			patterns.append(pattern)
			pattern = []
		else:
			pattern.append(i)
	patterns.append(pattern)
	return patterns

def _isVerticalSplit(pattern, vertical_split, smudge_count):
	mirror_length = min(len(pattern[0]) - vertical_split, vertical_split)
	differences = 0
	for line in pattern:
		left = [char for char in line[vertical_split - mirror_length : vertical_split][::-1]]
		right = [char for char in line[vertical_split : vertical_split + mirror_length]]
		differences += sum([pair[0] != pair[1] for pair in zip(left, right)])
	return differences == smudge_count

def _isHorizontalSplit(pattern, horizontal_split, smudge_count):
	mirror_length = min(len(pattern) - horizontal_split, horizontal_split)
	differences = 0
	for index in range(mirror_length):
		left = [char for char in pattern[horizontal_split - 1 - index]]
		right = [char for char in pattern[horizontal_split + index]]
		differences += sum([pair[0] != pair[1] for pair in zip(left, right)])
	return differences == smudge_count

def _calculatePatternScore(input_lines, smudge_count):
	patterns = _parseLines(input_lines)
	score = 0
	for pattern in patterns:
		pattern_score = 0
		for vertical_split in range(1, len(pattern[0])):
			if _isVerticalSplit(pattern, vertical_split, smudge_count):
				pattern_score += vertical_split
		for horizontal_split in range(1, len(pattern)):
			if _isHorizontalSplit(pattern, horizontal_split, smudge_count):
				pattern_score += (100 * horizontal_split)
		score += pattern_score
	return score

def silver(input_lines):
	return _calculatePatternScore(input_lines, 0)

def gold(input_lines):
	return _calculatePatternScore(input_lines, 1)
