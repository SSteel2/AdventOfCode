import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(line):
	split_line = line.split(' ')
	if split_line[0] == 'noop':
		return {'operation': split_line[0]}
	else:
		return {'operation': split_line[0], 'value': int(split_line[1])}

def silver(input_lines):
	instructions = Util.input.ParseInputLines(input_lines, _parse)
	special_cycles = [20, 60, 100, 140, 180, 220]
	current_cycle = 0
	current_value = 1
	solution = 0
	for instruction in instructions:
		update_value = 0
		if instruction['operation'] == 'noop':
			current_cycle += 1
		if instruction['operation'] == 'addx':
			current_cycle += 2
			update_value = instruction['value']
		if len(special_cycles) > 0 and current_cycle >= special_cycles[0]:
			solution += special_cycles[0] * current_value
			special_cycles = special_cycles[1:]
		current_value += update_value
	return solution

def _draw(cycle, value, output):
	if value <= cycle % 40 <= value + 2:
		output[(cycle - 1) // 40][(cycle - 1) % 40] = '#'

def gold(input_lines):
	instructions = Util.input.ParseInputLines(input_lines, _parse)
	output = [['.' for i in range(40)] for j in range(6)]
	current_cycle = 0
	current_value = 1
	for instruction in instructions:
		if instruction['operation'] == 'noop':
			current_cycle += 1
			_draw(current_cycle, current_value, output)
		if instruction['operation'] == 'addx':
			current_cycle += 2
			_draw(current_cycle - 1, current_value, output)
			_draw(current_cycle, current_value, output)
			current_value += instruction['value']
	return '\n' + '\n'.join([''.join(line) for line in output])
