import Util.input
import math

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(input_lines):
	return [int(i) for i in input_lines[0].split(' ')]

def _digits_count(number):
	return math.floor(math.log10(number)) + 1

meomized_blinks = {}
def _blink_recursive(number, blinks):
	if blinks == 0:
		return 1

	if (number, blinks) in meomized_blinks:
		return meomized_blinks[(number, blinks)]

	count = 0
	if number == 0:
		count = _blink_recursive(1, blinks - 1)
	elif (digits := _digits_count(number)) % 2 == 0:
		str_number = str(number)
		count = _blink_recursive(int(str_number[:digits // 2]), blinks - 1) + _blink_recursive(int(str_number[digits // 2:]), blinks - 1)
	else:
		count = _blink_recursive(number * 2024, blinks - 1)
	meomized_blinks[(number, blinks)] = count
	return count

def _solution(input_lines, blink_count):
	arrangement = _parse(input_lines)
	count = 0
	for i in arrangement:
		count += _blink_recursive(i, blink_count)
	return count

def silver(input_lines):
	return _solution(input_lines, 25)

def gold(input_lines):
	return _solution(input_lines, 75)
