import math
import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def silver(input_lines):
	times = [i for i in input_lines[0].split(' ') if i != ''][1:]
	distances = [i for i in input_lines[1].split(' ') if i != ''][1:]
	games = [{'time': int(i[0]), 'distance': int(i[1])} for i in zip(times, distances)]

	answers = []
	for game in games:
		answer = 0
		for i in range(game['time']):
			if i * (game['time'] - i) > game['distance']:
				answer += 1
		answers.append(answer)
	return math.prod(answers)

def gold(input_lines):
	time = int(''.join([i for i in input_lines[0].split(' ') if i != ''][1:]))
	distance = int(''.join([i for i in input_lines[1].split(' ') if i != ''][1:]))

	start = (time - math.sqrt(time ** 2 - 4 * distance)) / 2
	end = (time + math.sqrt(time ** 2 - 4 * distance)) / 2
	return math.floor(end) - math.floor(start)
