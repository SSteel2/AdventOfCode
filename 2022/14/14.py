import math
import Util.input
import Util.directions

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(input_lines):
	rocks = []
	max_x, min_x, max_y, min_y = 0, math.inf, 0, math.inf
	for line in input_lines:
		rock = []
		split_line = line.split(' -> ')
		for split in split_line:
			x, y = [int(i) for i in split.split(',')]
			if x > max_x:
				max_x = x
			elif x < min_x:
				min_x = x
			if y > max_y:
				max_y = y
			elif y < min_y:
				min_y = y
			rock.append((x, y))
		rocks.append(rock)

	cave = [['.' for _ in range(max_x - min_x + 3)] for _ in range(max_y + 2)]
	for rock in rocks:
		for i in range(1, len(rock)):
			start_x = rock[i - 1][0]
			start_y = rock[i - 1][1]
			end_x = rock[i][0]
			end_y = rock[i][1]
			if start_x == end_x:
				for i in range(start_y, end_y, 1 if start_y < end_y else -1):
					Util.directions.Set(cave, (i, start_x - min_x + 1), '#')
			elif start_y == end_y:
				for i in range(start_x, end_x, 1 if start_x < end_x else -1):
					Util.directions.Set(cave, (start_y, i - min_x + 1), '#')
		Util.directions.Set(cave, (rock[-1][1], rock[-1][0] - min_x + 1), '#')
	return cave, min_x - 1, 0

def _dropSand(cave, start_x):
	sand = (0, 500 - start_x)
	moving = True
	finished = False
	while moving:
		if sand[0] == len(cave) - 1:
			moving = False
			finished = True
		elif Util.directions.Get(cave, (sand[0] + 1, sand[1])) == '.':
			sand = (sand[0] + 1, sand[1])
		elif Util.directions.Get(cave, (sand[0] + 1, sand[1] - 1)) == '.':
			sand = (sand[0] + 1, sand[1] - 1)
		elif Util.directions.Get(cave, (sand[0] + 1, sand[1] + 1)) == '.':
			sand = (sand[0] + 1, sand[1] + 1)
		else:
			moving = False
	Util.directions.Set(cave, sand, 'O')
	return finished

def silver(input_lines):
	cave, start_x, start_y = _parse(input_lines)

	count = 0
	while not _dropSand(cave, start_x):
		count += 1
	return count

def gold(input_lines):
	cave, start_x, start_y = _parse(input_lines)
	unreachable = 0
	for i, line in enumerate(cave):
		for j, col in enumerate(line):
			if Util.directions.Get(cave, (i, j)) == '#':
				unreachable += 1
			elif Util.directions.Get(cave, (i - 1, j - 1)) != '.' and Util.directions.Get(cave, (i - 1, j)) != '.' and Util.directions.Get(cave, (i - 1, j + 1)) != '.':
				Util.directions.Set(cave, (i, j), 'v')
				unreachable += 1

	return len(cave) ** 2 - unreachable