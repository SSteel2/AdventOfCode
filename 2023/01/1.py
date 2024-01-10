import re
import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

# Silver star
def silver(input_lines):
	numbers_sum = 0
	for line in input_lines:
		first_digit = None
		last_digit = None
		for char in line:
			if char.isdigit():
				if first_digit is None:
					first_digit = char
				last_digit = char
		numbers_sum += int(first_digit + last_digit)
	return numbers_sum

# Gold star
numbers_dict = {
	'one': '1',
	'two': '2',
	'three': '3',
	'four': '4',
	'five': '5',
	'six': '6',
	'seven': '7',
	'eight': '8',
	'nine': '9'
}

def _matchToDigit(match):
	if match in numbers_dict.keys():
		return numbers_dict[match]
	return match

def gold(input_lines):
	numbers_strings = list(numbers_dict.keys())
	numbers_sum_gold = 0
	pattern = '|'.join(numbers_strings) + '|[0-9]'
	for line in input_lines:
		iterator = re.finditer(pattern, line)
		first_match = None
		last_match = None
		for item in iterator:
			if first_match is None:
				first_match = item
			last_match = item
		# try to look for overlapping matches
		overlapping_match = re.search(pattern, line[last_match.start() + 1:])
		if overlapping_match:
			last_match = overlapping_match
		number = int(_matchToDigit(first_match[0]) + _matchToDigit(last_match[0]))
		numbers_sum_gold += number
	return numbers_sum_gold