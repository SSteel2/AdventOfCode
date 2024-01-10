import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parseInputLine(line):
	first_colon = line.index(':')
	game_id = int(line[5:first_colon])
	games_string = line[first_colon + 2:].split('; ')
	games_string[-1] = games_string[-1].removesuffix('\n')
	games = []
	for game in games_string:
		color_strings = game.split(', ')
		game_dict = {}
		for color_string in color_strings:
			count, color = color_string.split(' ')
			game_dict[color] = int(count)
		games.append(game_dict)
	return {'game_id': game_id, 'games': games}

def _parseInputLines(input_lines):
	parsed = []
	for line in input_lines:
		parsed.append(_parseInputLine(line))
	return parsed

# Silver star
def silver(input_lines):
	parsed = _parseInputLines(input_lines)

	# Sum of ID's which are possible games 12 red, 13 green, 14 blue
	id_sum = 0
	for game in parsed:
		passing = True
		for draw in game['games']:
			if 'red' in draw and draw['red'] > 12 or 'green' in draw and draw['green'] > 13 or 'blue' in draw and draw['blue'] > 14:
				passing = False
				break
		if passing:
			id_sum += game['game_id']
	return id_sum

# print('Silver answer: ' + str(id_sum))

# Gold star
def gold(input_lines):
	parsed = _parseInputLines(input_lines)
	
	# Power of minimum sets
	power_sum = 0
	for game in parsed:
		minimums = {'red': 0, 'blue': 0, 'green': 0}
		for draw in game['games']:
			if 'red' in draw:
				if draw['red'] > minimums['red']:
					minimums['red'] = draw['red']
			if 'blue' in draw:
				if draw['blue'] > minimums['blue']:
					minimums['blue'] = draw['blue']
			if 'green' in draw:
				if draw['green'] > minimums['green']:
					minimums['green'] = draw['green']
		power_sum += (minimums['red'] * minimums['blue'] * minimums['green'])
	return power_sum

# print('Gold answer: ' + str(power_sum))
