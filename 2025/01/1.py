import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(line):
	return int(line[1:]) if line[0] == 'R' else -int(line[1:])

def _solve(numbers, score_func):
	result = 0
	pointer = 50
	for number in numbers:
		if pointer == 0 and number < 0:
			pointer += 100
		pointer += number
		result += score_func(pointer)
		pointer %= 100
	return result

def _silver_score(pointer):
	return 1 if pointer % 100 == 0 else 0

def _gold_score(pointer):
	result = abs(pointer // 100)
	if pointer % 100 == 0 and pointer <= 0:
		result += 1
	return result

def silver(input_lines):
	numbers = Util.input.ParseInputLines(input_lines, _parse)
	return _solve(numbers, _silver_score)

def gold(input_lines):
	numbers = Util.input.ParseInputLines(input_lines, _parse)
	return _solve(numbers, _gold_score)
