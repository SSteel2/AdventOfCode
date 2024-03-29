import Util.input
import Util.directions

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def FindStart(input_lines):
	for i, line in enumerate(input_lines):
		for j, col in enumerate(line):
			if col == 'S':
				return (i, j)

valid_moves = {
	'|': ['U', 'D'],
	'-': ['R', 'L'],
	'L': ['U', 'R'],
	'J': ['U', 'L'],
	'7': ['D', 'L'],
	'F': ['D', 'R']
}

def GetNextMove(input_lines, current, last):
	moves = valid_moves[input_lines[current[0]][current[1]]]
	if Util.directions.Move(current, moves[0]) != last:
		return Util.directions.Move(current, moves[0])
	else:
		return Util.directions.Move(current, moves[1])

def GetRoute(input_lines, start):
	last_pos = (start[0], start[1])
	current_pos = (start[0], start[1] + 1)
	route = [current_pos]
	while current_pos != start:
		next_pos = GetNextMove(input_lines, current_pos, last_pos)
		route.append(next_pos)
		last_pos = current_pos
		current_pos = next_pos
	return route

def silver(input_lines):
	start = FindStart(input_lines)
	route = GetRoute(input_lines, start)
	return len(route) // 2

def gold(input_lines):
	start = FindStart(input_lines)
	route = GetRoute(input_lines, start)
	clean_lines = [['.' for _ in range(len(input_lines[0]))] for _ in range(len(input_lines))]
	for i in route:
		clean_lines[i[0]][i[1]] = input_lines[i[0]][i[1]]
	clean_lines[start[0]][start[1]] = 'L' # ideally this should be deduced automatically, but I'm lazy

	inside_spaces = 0
	for line in clean_lines:
		winding_number = 0
		for val in line:
			if val == '.' and winding_number % 4 == 2:
				inside_spaces += 1
			elif val == 'F' or val == 'J':
				winding_number += 1
			elif val == 'L' or val == '7':
				winding_number -= 1
			elif val == '|':
				winding_number += 2
	return inside_spaces
