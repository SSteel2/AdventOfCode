import math
import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _quadraticSolve(time, distance):
	start = (time - math.sqrt(time ** 2 - 4 * distance)) / 2
	end = (time + math.sqrt(time ** 2 - 4 * distance)) / 2
	return math.floor(end) - math.floor(start) - end.is_integer()

def silver(input_lines):
	times = [i for i in input_lines[0].split(' ') if i != ''][1:]
	distances = [i for i in input_lines[1].split(' ') if i != ''][1:]
	games = [{'time': int(i[0]), 'distance': int(i[1])} for i in zip(times, distances)]
	return math.prod(_quadraticSolve(game['time'], game['distance']) for game in games)

def gold(input_lines):
	time = int(''.join([i for i in input_lines[0].split(' ') if i != ''][1:]))
	distance = int(''.join([i for i in input_lines[1].split(' ') if i != ''][1:]))
	return _quadraticSolve(time, distance)
