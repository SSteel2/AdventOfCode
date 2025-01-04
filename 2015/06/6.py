import Util.input
import Util.directions

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(input_lines):
	instructions = []
	for line in input_lines:
		split_line = line.split(' ')
		if split_line[0] == 'turn':
			offset = 1
			command = split_line[1]
		else:
			offset = 0
			command = split_line[0]
		x1, y1 = [int(i) for i in split_line[1 + offset].split(',')]
		x2, y2 = [int(i) for i in split_line[3 + offset].split(',')]
		instructions.append({'command': command, 'x1': x1, 'x2': x2, 'y1': y1, 'y2': y2})
	return instructions

def _apply(grid, x1, x2, y1, y2, command):
	for x in range(x1, x2 + 1):
		for y in range(y1, y2 + 1):
			grid[x][y] = command(grid[x][y])

def silver(input_lines):
	instructions = _parse(input_lines)
	grid = [[False for _ in range(1000)] for _ in range(1000)]
	for instruction in instructions:
		if instruction['command'] == 'on':
			_apply(grid, instruction['x1'], instruction['x2'], instruction['y1'], instruction['y2'], lambda x: True)
		elif instruction['command'] == 'off':
			_apply(grid, instruction['x1'], instruction['x2'], instruction['y1'], instruction['y2'], lambda x: False)
		elif instruction['command'] == 'toggle':
			_apply(grid, instruction['x1'], instruction['x2'], instruction['y1'], instruction['y2'], lambda x: not x)
	return Util.directions.Count(grid, True)

def gold(input_lines):
	instructions = _parse(input_lines)
	grid = [[0 for _ in range(1000)] for _ in range(1000)]
	for instruction in instructions:
		if instruction['command'] == 'on':
			_apply(grid, instruction['x1'], instruction['x2'], instruction['y1'], instruction['y2'], lambda x: x + 1)
		elif instruction['command'] == 'off':
			_apply(grid, instruction['x1'], instruction['x2'], instruction['y1'], instruction['y2'], lambda x: x + 1 if x > 0 else 0)
		elif instruction['command'] == 'toggle':
			_apply(grid, instruction['x1'], instruction['x2'], instruction['y1'], instruction['y2'], lambda x: x + 2)
	return sum([sum(i) for i in grid])
