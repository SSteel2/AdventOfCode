import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(line):
	return int(line[1:]) if line[0] == 'R' else -int(line[1:])

def silver(input_lines):
	numbers = Util.input.ParseInputLines(input_lines, _parse)
	result = 0
	pointer = 50
	for number in numbers:
		pointer = (pointer + number) % 100
		if pointer == 0:
			result += 1
	return result

def gold(input_lines):
	numbers = Util.input.ParseInputLines(input_lines, _parse)
	result = 0
	pointer = 50
	for number in numbers:
		if pointer == 0 and number < 0:
			result -= 1
		pointer += number
		result += abs(pointer // 100)
		if pointer % 100 == 0 and pointer <= 0:
			result += 1
		pointer %= 100
	return result
