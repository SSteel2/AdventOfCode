input_lines = []
with open('input.txt', 'r') as input_file:
	for line in input_file:
		input_lines.append(line.removesuffix('\n'))

# Parse input
instructions = [{'direction': i.split(' ')[0], 'length': int(i.split(' ')[1])} for i in input_lines]

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

# Silver star
print('Silver answer: ' + str(CalculateArea(instructions)))

# Gold star
number_to_direction = {
	'0': 'R',
	'1': 'D',
	'2': 'L',
	'3': 'U'
}

instructions_gold = [{'direction': number_to_direction[i.split(' ')[2][7]], 'length': int(i.split(' ')[2][2:7], base=16)} for i in input_lines]

print('Gold answer: ' + str(CalculateArea(instructions_gold)))
