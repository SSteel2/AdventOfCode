import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _count_literals(line):
	count = 0
	escape = False
	escaped_hex = 0
	for i in line[1:-1]:
		if escaped_hex > 0:
			escaped_hex -= 1
			continue
		if escape:
			if i == 'x':
				escaped_hex = 2
			escape = False
			continue
		if i == '\\':
			escape = True
		count += 1
	return count

def _count_encoded(line):
	count = 2
	for i in line:
		count += 1
		if i == '\"' or i == '\\':
			count += 1
	return count

def silver(input_lines):
	total_chars = 0
	total_literals = 0
	for line in input_lines:
		total_literals += _count_literals(line)
		total_chars += len(line)
	return total_chars - total_literals

def gold(input_lines):
	total_chars = 0
	total_encoded = 0
	for line in input_lines:
		total_encoded += _count_encoded(line)
		total_chars += len(line)
	return total_encoded - total_chars
