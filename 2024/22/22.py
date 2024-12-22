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

def _change_to_bananas_dict(number, max_iteration):
	change_to_bananas = {}
	current = 0
	last_price = number % 10
	differences = [last_price]
	for i in range(max_iteration):
		number = _next_secret(number)
		price = number % 10
		differences.append(price - last_price)
		last_price = price
		if len(differences) < 4:
			continue
		key = tuple(differences[-4:])
		if key not in change_to_bananas:
			change_to_bananas[key] = price
	return change_to_bananas

def silver(input_lines):
	numbers = Util.input.ParseInputLines(input_lines, _parseLine)
	score = 0
	for number in numbers:
		score += _secret(number, 2000)
	return score

def _possible_answer_generator():
	for i in range(-9, 10):
		for j in range(-9, 10):
			for k in range(-9, 10):
				for l in range(-9, 10):
					yield (i, j, k, l)

def gold(input_lines):
	numbers = Util.input.ParseInputLines(input_lines, _parseLine)
	change_to_bananas = []
	for number in numbers:
		change_to_bananas.append(_change_to_bananas_dict(number, 2000))
	max_score = -1
	possible_answer = _possible_answer_generator()
	for answer in possible_answer:
		score = 0
		for i in change_to_bananas:
			if answer in i:
				score += i[answer]
		if score > max_score:
			max_score = score
	return max_score

