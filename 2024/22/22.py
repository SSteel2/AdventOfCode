import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parseLine(line):
	return int(line)

def _next_secret(number):
	step_1 = ((number << 6) ^ number) & 16777215
	step_2 = ((step_1 >> 5) ^ step_1) & 16777215
	return ((step_2 << 11) ^ step_2) & 16777215

def _secret(number, max_iteration):
	for i in range(max_iteration):
		number = _next_secret(number)
	return number

def _change_to_bananas_dict(number, max_iteration, current_dict):
	current = 0
	last_price = number % 10
	visited_keys = set()
	differences = [last_price]
	for i in range(max_iteration):
		number = _next_secret(number)
		price = number % 10
		differences.append(price - last_price)
		last_price = price
		if len(differences) < 4:
			continue
		key = tuple(differences[-4:])
		if key not in visited_keys:
			if key not in current_dict:
				current_dict[key] = price
			else:
				current_dict[key] += price
		visited_keys.add(key)

def silver(input_lines):
	numbers = Util.input.ParseInputLines(input_lines, _parseLine)
	score = 0
	for number in numbers:
		score += _secret(number, 2000)
	return score

def gold(input_lines):
	numbers = Util.input.ParseInputLines(input_lines, _parseLine)
	change_to_bananas = {}
	for number in numbers:
		_change_to_bananas_dict(number, 2000, change_to_bananas)
	return max(change_to_bananas.values())
