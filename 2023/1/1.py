import re

input_lines = []
with open('input.txt', 'r') as input_file:
	for line in input_file:
		input_lines.append(line)

# Silver star
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

print('Silver answer: ' + str(numbers_sum))

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

def matchToDigit(match):
	if match in numbers_dict.keys():
		return numbers_dict[match]
	return match

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
	number = int(matchToDigit(first_match[0]) + matchToDigit(last_match[0]))
	numbers_sum_gold += number

print('Gold answer: ' + str(numbers_sum_gold))
