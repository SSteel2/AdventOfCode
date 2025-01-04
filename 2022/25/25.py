import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

SnafuIntTable = {
	'=': -2,
	'-': -1,
	'0': 0,
	'1': 1,
	'2': 2
}

IntSnafuTable = {
	0: '0',
	1: '1',
	2: '2',
	3: '=',
	4: '-'
}

def _snafu_to_decimal(number):
	total = 0
	value = 1
	for i in number[::-1]:
		total += SnafuIntTable[i] * value
		value *= 5
	return total

def _decimal_to_snafu(number):
	inverse_quinary = []
	while number > 0:
		inverse_quinary.append(number % 5)
		number //= 5
	inverse_snafu = []
	carry_forward = 0
	for i in inverse_quinary:
		current = i + carry_forward
		if current >= 3:
			carry_forward = 1
		else:
			carry_forward = 0
		if current == 5:
			current = 0
		inverse_snafu.append(IntSnafuTable[current])
	if carry_forward == 1:
		inverse_snafu.append('1')
	return ''.join(inverse_snafu[::-1])

def silver(input_lines):
	total = 0
	for line in input_lines:
		total += _snafu_to_decimal(line)
	return _decimal_to_snafu(total)

def gold(input_lines):
	pass
