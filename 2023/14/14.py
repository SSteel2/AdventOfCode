import Util.input
import Util.period

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _findEmpty(l, c, chart, direction):
	check_range = {
		'N': range(l - 1, -1, -1),
		'S': range(l + 1, len(chart)),
		'E': range(c + 1, len(chart[0])),
		'W': range(c - 1, -1, -1)
	}
	if direction == 'N' or direction == 'S':
		get_chart_value = lambda x: chart[x][c]
		result = l
	else:
		get_chart_value = lambda x: chart[l][x]
		result = c
	for i in check_range[direction]:
		if get_chart_value(i) == '.':
			result = i
		else:
			break
	return result

def _move(l, c, chart, direction):
	condition = {
		'N': l == 0,
		'S': l == len(chart) - 1,
		'E': c == len(chart[0]),
		'W': c == 0
	}
	if condition[direction]:
		return
	new_param = _findEmpty(l, c, chart, direction)
	chart[l][c] = '.'
	if direction == 'N' or direction == 'S':
		chart[new_param][c] = 'O'
	else:
		chart[l][new_param] = 'O'

def _moveAll(chart, direction):
	enumeration_direction_line = 1
	enumeration_direction_col = 1
	if direction == 'S':
		enumeration_direction_line = -1
	if direction == 'E':
		enumeration_direction_col = -1
	for i, line in list(enumerate(chart))[::enumeration_direction_line]:
		for j, char in list(enumerate(line))[::enumeration_direction_col]:
			if char == 'O':
				_move(i, j, chart, direction)	

def _countScore(chart):
	current_line_score = len(chart)
	total_score = 0
	for line in chart:
		for char in line:
			if char == 'O':
				total_score += current_line_score
		current_line_score -= 1
	return total_score

def silver(input_lines):
	chart = [[char for char in line] for line in input_lines]
	_moveAll(chart, 'N')
	return _countScore(chart)

def gold(input_lines):
	chart = [[char for char in line] for line in input_lines]
	scores = []
	elapsed_cycles = 368
	period_calc_start = elapsed_cycles - 150
	for i in range(elapsed_cycles):
		_moveAll(chart, 'N')
		_moveAll(chart, 'W')
		_moveAll(chart, 'S')
		_moveAll(chart, 'E')
		scores.append(_countScore(chart))
	period = Util.period.CalculatePeriod(scores[period_calc_start:])
	target_cycles = 1000000000
	remainder = (target_cycles - period_calc_start) % period
	return scores[period_calc_start + remainder - 1]