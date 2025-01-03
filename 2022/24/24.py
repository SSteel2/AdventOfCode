import Util.input
import Util.directions
import Util.PriorityQueue

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

class BlizzardLine:
	def __init__(self, line_length, padding):
		self.line_length = line_length
		self.blizzards = []
		self.padding = padding

	def AddBlizzard(self, start_coordinate, is_forward):
		self.blizzards.append((start_coordinate - self.padding, 1 if is_forward else -1))

	def CheckLocationSafety(self, coordinate, time):
		for blizzard in self.blizzards:
			if (blizzard[0] + blizzard[1] * time) % self.line_length + self.padding == coordinate:
				return False
		return True

def _parse(input_lines):
	blizzards = []
	ground = [['.' for i in j] for j in input_lines]
	for l, line in enumerate(input_lines):
		for c, char in enumerate(line):
			if char == '#':
				ground[l][c] = '#'
			elif char != '.':
				blizzards.append((l, c, char))
	return ground, blizzards

def _arrange_blizzards(blizzards, ground, padding):
	vertical_blizzard_lines = [BlizzardLine(len(ground) - padding * 2, padding) for _ in range(len(ground[0]))]
	horizontal_blizzard_lines = [BlizzardLine(len(ground[0]) - padding * 2, padding) for _ in range(len(ground))]
	for blizzard in blizzards:
		if blizzard[2] == '^' or blizzard[2] == 'v':
			vertical_blizzard_lines[blizzard[1]].AddBlizzard(blizzard[0], False if blizzard[2] == '^' else True)
		elif blizzard[2] == '<' or blizzard[2] == '>':
			horizontal_blizzard_lines[blizzard[0]].AddBlizzard(blizzard[1], False if blizzard[2] == '<' else True)
	return vertical_blizzard_lines, horizontal_blizzard_lines

def _get_open_slot(ground, line_num):
	for i, col in enumerate(ground[line_num]):
		if col == '.':
			return (line_num, i)

def _manhattanDistance(point1, point2):
	return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

def _is_position_valid(position, time, ground, vertical_blizzard_lines, horizontal_blizzard_lines):
	if Util.directions.Get(ground, position) == '#':
		return False
	if not vertical_blizzard_lines[position[1]].CheckLocationSafety(position[0], time):
		return False
	if not horizontal_blizzard_lines[position[0]].CheckLocationSafety(position[1], time):
		return False
	return True

def _find_best_path(ground, vertical_blizzard_lines, horizontal_blizzard_lines, start_position, end_position, start_time):
	next_positions = Util.PriorityQueue.PriorityQueue()
	next_positions.append(_manhattanDistance(start_position, end_position), (start_position, []))
	visited = set()
	while len(next_positions) > 0:
		current_position, current_path = next_positions.pop()
		current_length = len(current_path)
		if (current_position, current_length) in visited:
			continue
		if current_position == end_position:
			return current_path
		for direction in Util.directions.DirectionsTable:
			next_position = Util.directions.Move(current_position, direction)
			if _is_position_valid(next_position, start_time + current_length + 1, ground, vertical_blizzard_lines, horizontal_blizzard_lines):
				next_positions.append(_manhattanDistance(current_position, end_position) + current_length + 1, (next_position, current_path + [direction]))
		# waiting
		if _is_position_valid(current_position, start_time + current_length + 1, ground, vertical_blizzard_lines, horizontal_blizzard_lines):
			next_positions.append(_manhattanDistance(current_position, end_position) + current_length + 1, (current_position, current_path + ['_']))
		visited.add((current_position, current_length))

def _prepare(input_lines):
	ground, blizzards = _parse(input_lines)
	ground = Util.directions.PadTable(ground, 1, '#')
	blizzards = [(i[0] + 1, i[1] + 1, i[2]) for i in blizzards]
	vertical_blizzard_lines, horizontal_blizzard_lines = _arrange_blizzards(blizzards, ground, 2)
	start_position = _get_open_slot(ground, 1)
	end_position = _get_open_slot(ground, len(ground) - 2)
	return ground, vertical_blizzard_lines, horizontal_blizzard_lines, start_position, end_position

def silver(input_lines):
	ground, vertical_blizzard_lines, horizontal_blizzard_lines, start_position, end_position = _prepare(input_lines)
	best_path = _find_best_path(ground, vertical_blizzard_lines, horizontal_blizzard_lines, start_position, end_position, 0)
	return len(best_path)

def gold(input_lines):
	ground, vertical_blizzard_lines, horizontal_blizzard_lines, start_position, end_position = _prepare(input_lines)
	first_traversal = _find_best_path(ground, vertical_blizzard_lines, horizontal_blizzard_lines, start_position, end_position, 0)
	second_traversal = _find_best_path(ground, vertical_blizzard_lines, horizontal_blizzard_lines, end_position, start_position, len(first_traversal))
	third_traversal = _find_best_path(ground, vertical_blizzard_lines, horizontal_blizzard_lines, start_position, end_position, len(first_traversal) + len(second_traversal))
	return len(first_traversal) + len(second_traversal) + len(third_traversal)
