import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _getScore(item):
	if item.islower():
		return ord(item) - ord('a') + 1
	else:
		return ord(item) - ord('A') + 27

def silver(input_lines):
	score = 0
	for line in input_lines:
		first_part = line[:len(line) // 2]
		second_part = line[len(line) // 2:]
		for i in first_part:
			if i in second_part:
				score += _getScore(i)
				break
	return score

def gold(input_lines):
	score = 0
	for triplet in [input_lines[i:i + 3] for i in range(0, len(input_lines), 3)]:
		for i in triplet[0]:
			if i in triplet[1] and i in triplet[2]:
				score += _getScore(i)
				break
	return score
