import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parseLine(line):
	split_line = line.split(' ')
	return {'opponent': split_line[0], 'response': split_line[1]}

rock_paper_scissors = ['A', 'B', 'C']

def _getResponse(opponent, result):
	# result: -1 - lose, 0 - draw, 1 - win
	return rock_paper_scissors[(rock_paper_scissors.index(opponent) + result) % len(rock_paper_scissors)]

silver_conversion = {
	'X': 'A',
	'Y': 'B',
	'Z': 'C',
}

score_table = {
	'A': 1,
	'B': 2,
	'C': 3
}

def silver(input_lines):
	games = Util.input.ParseInputLines(input_lines, _parseLine)
	# A - rock, B - paper, C - scissors
	# X - rock, Y - paper, Z - scissors
	score = 0
	for game in games:
		result = 0
		if game['opponent'] == _getResponse(silver_conversion[game['response']], -1):
			result = 6
		elif game['opponent'] == _getResponse(silver_conversion[game['response']], 0):
			result = 3
		score += result + score_table[silver_conversion[game['response']]]
	return score

result_table = {
	'X': -1,
	'Y': 0,
	'Z': 1
}

def gold(input_lines):
	games = Util.input.ParseInputLines(input_lines, _parseLine)
	# X - lose, Y - draw, Z - win
	score = 0
	for game in games:
		score += score_table[_getResponse(game['opponent'], result_table[game['response']])] + (result_table[game['response']] + 1) * 3
	return score