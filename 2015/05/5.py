import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _is_nice_string_silver(line):
	if 'ab' in line or 'cd' in line or 'pq' in line or 'xy' in line:
		return False
	vowels = {'a', 'e', 'i', 'o', 'u'}
	vowel_count = 0
	double_letter = False
	last_col = ''
	for col in line:
		if col in vowels:
			vowel_count += 1
		if last_col == col:
			double_letter = True
		last_col = col
	return double_letter and vowel_count >= 3

def _is_nice_string_gold(line):
	is_repeating_letter_pair = False
	is_close_same_letter = False
	for i in range(len(line) - 2):
		if line[i:i + 2] in line[i + 2:]:
			is_repeating_letter_pair = True
		if line[i] == line[i + 2]:
			is_close_same_letter = True
	return is_repeating_letter_pair and is_close_same_letter

def _solve(input_lines, predicate):
	total = 0
	for line in input_lines:
		if predicate(line):
			total += 1
	return total	

def silver(input_lines):
	return _solve(input_lines, _is_nice_string_silver)

def gold(input_lines):
	return _solve(input_lines, _is_nice_string_gold)
