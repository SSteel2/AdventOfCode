import Util.input
from functools import cmp_to_key

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(input_lines):
	lines = []
	for line in input_lines:
		if line == '':
			continue
		lines.append(eval(line, {'__builtins__': None}, {}))
	return lines

def _compare(left, right):
	left_length = len(left)
	right_length = len(right)
	for i in range(min(left_length, right_length)):
		is_left_int = isinstance(left[i], int)
		is_right_int = isinstance(right[i], int)
		if is_left_int and is_right_int:
			comparison = left[i] - right[i]
		elif not is_left_int and not is_right_int:
			comparison = _compare(left[i], right[i])
		elif is_left_int:
			comparison = _compare([left[i]], right[i])
		elif is_right_int:
			comparison = _compare(left[i], [right[i]])
		if comparison != 0:
			return comparison
	return left_length - right_length

def silver(input_lines):
	lines = _parse(input_lines)
	parsed_pairs = []
	for i in range(0, len(lines), 2):
		pair = {}
		pair['left'] = lines[i]
		pair['right'] = lines[i + 1]
		parsed_pairs.append(pair)

	solution = 0
	for i, pair in enumerate(parsed_pairs):
		if _compare(pair['left'], pair['right']) < 0:
			solution += i + 1
	return solution

def gold(input_lines):
	lines = _parse(input_lines)
	special2 = [[2]]
	special6 = [[6]]
	lines.append(special2)
	lines.append(special6)
	lines.sort(key=cmp_to_key(_compare))
	return (lines.index(special2) + 1) * (lines.index(special6) + 1)
