import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(input_lines):
	equations = []
	parameters = {}
	current = 0
	for line in input_lines:
		if line == '':
			continue
		x, y = [int(i[2:]) for i in line.split(': ')[1].split(', ')]
		parameters["p" + str((current * 2) + 1)] = x
		parameters["p" + str((current * 2) + 2)] = y
		current += 1
		if current == 3:
			equations.append(parameters)
			parameters = {}
			current = 0
	return equations

def _solve(equation):
	p1 = equation['p1']
	p2 = equation['p2']
	p3 = equation['p3']
	p4 = equation['p4']
	p5 = equation['p5']
	p6 = equation['p6']
	b = (p5 * p2 - p6 * p1) // (p3 * p2 - p4 * p1)
	a = (p6 - b * p4) // p2
	if a * p1 + b * p3 == p5 and a * p2 + b * p4 == p6:
		return a * 3 + b
	return 0

def _offset_parameters(equation):
	equation['p5'] += 10000000000000
	equation['p6'] += 10000000000000

def _solution(input_lines, offset_parameters):
	equations = _parse(input_lines)
	score = 0
	for equation in equations:
		if offset_parameters:
			_offset_parameters(equation)
		score += _solve(equation)
	return score	

def silver(input_lines):
	return _solution(input_lines, False)

def gold(input_lines):
	return _solution(input_lines, True)
