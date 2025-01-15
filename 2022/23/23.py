import Util.input
import Util.directions
import math

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(input_lines):
	elves = []
	for l, line in enumerate(input_lines):
		for c, char in enumerate(line):
			if char == '#':
				elves.append((l, c))
	return elves

directions = ['U', 'D', 'L', 'R']

def _get_next_postion(ground, current_position, direction_index):
	neighbours = [Utils.directions.Get(ground, Utils.directions.Move(current_position, i)) for i in Util.directions.DirectionsTableDiagonals]
	if sum(neighbours) == 0:
		return current_position
	for i in range(4):
		current_direction = directions[(direction_index + i) % 4]
		if current_direction == 'U' and neighbours[7] + neighbours[0] + neighbours[1] == 0:
			return Util.directions.Move(current_position, current_direction)
		elif current_direction == 'R' and neighbours[1] + neighbours[2] + neighbours[3] == 0:
			return Util.directions.Move(current_position, current_direction)
		elif current_direction == 'D' and neighbours[3] + neighbours[4] + neighbours[5] == 0:
			return Util.directions.Move(current_position, current_direction)
		elif current_direction == 'L' and neighbours[5] + neighbours[6] + neighbours[7] == 0:
			return Util.directions.Move(current_position, current_direction)
	return current_position

def _move(ground, elves, direction_index):
	proposed_positions = []
	taken_positions = {}
	is_moving = False
	for elf in elves:
		next_position = _get_next_postion(ground, elf, direction_index)
		if not is_moving and next_position != elf:
			is_moving = True
		proposed_positions.append(next_position)
		if next_position in taken_positions:
			taken_positions[next_position] += 1
		else:
			taken_positions[next_position] = 1
	next_positions = []
	for position in zip(elves, proposed_positions):
		if taken_positions[position[1]] > 1:
			next_positions.append(position[0])
		else:
			next_positions.append(position[1])
	for position in elves:
		Util.directions.Set(ground, position, 0)
	for position in next_positions:
		Util.directions.Set(ground, position, 1)
	return next_positions, is_moving

def _calculate_empty_ground(elves):
	min_x, min_y, max_x, max_y = math.inf, math.inf, -math.inf, -math.inf
	total_elves = len(elves)
	for i in elves:
		if i[0] < min_y:
			min_y = i[0]
		if i[0] > max_y:
			max_y = i[0]
		if i[1] < min_x:
			min_x = i[1]
		if i[1] > max_x:
			max_x = i[1]
	return (max_x - min_x + 1) * (max_y - min_y + 1) - total_elves

def _create_ground(ground_dimension, ground_offset, elves):
	ground = [[0 for i in range(ground_dimension)] for j in range(ground_dimension)]
	new_elves = []
	for elf in elves:
		new_elves.append((elf[0] + ground_offset, elf[1] + ground_offset))
		ground[elf[0] + ground_offset][elf[1] + ground_offset] = 1
	return ground, new_elves

def silver(input_lines):
	elves = _parse(input_lines)
	ground, elves = _create_ground(100, 10, elves)
	for step in range(10):
		elves, _ = _move(ground, elves, step)
	return _calculate_empty_ground(elves)

def gold(input_lines):
	elves = _parse(input_lines)
	ground, elves = _create_ground(300, 100, elves)
	is_moving = True
	step = 0
	while is_moving:
		elves, is_moving = _move(ground, elves, step)
		step += 1
	return step
