import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parseSilver(line):
	return {'direction': line.split(' ')[0], 'length': int(line.split(' ')[1])}

number_direction_map = {
	'0': 'R',
	'1': 'D',
	'2': 'L',
	'3': 'U'
}

def _parseGold(line):
	return {'direction': number_direction_map[line.split(' ')[2][7]], 'length': int(line.split(' ')[2][2:7], base=16)}

def CalculateArea(instructions):
	area = 0
	perimeter = 0
	current_x = 0
	for instruction in instructions:
		if instruction['direction'] == 'U':
			area -= (instruction['length'] * current_x)
		elif instruction['direction'] == 'D':
			area += (instruction['length'] * current_x)
		elif instruction['direction'] == 'R':
			current_x += instruction['length']
		elif instruction['direction'] == 'L':
			current_x -= instruction['length']
		perimeter += instruction['length']
	return area + perimeter // 2 + 1

def silver(input_lines):
	instructions = Util.input.ParseInputLines(input_lines, _parseSilver)
	return CalculateArea(instructions)

def gold(input_lines):
	instructions = Util.input.ParseInputLines(input_lines, _parseGold)
	return CalculateArea(instructions)
