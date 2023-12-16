input_lines = []
with open('input.txt', 'r') as input_file:
	for line in input_file:
		input_lines.append(line.removesuffix('\n'))

def FindStart():
	for i, line in enumerate(input_lines):
		for j, col in enumerate(line):
			if col == 'S':
				return (i, j)

directions = {
	'N': (-1, 0),
	'E': (0, 1),
	'S': (1, 0),
	'W': (0, -1)
}

valid_moves = {
	'|': ['N', 'S'],
	'-': ['E', 'W'],
	'L': ['N', 'E'],
	'J': ['N', 'W'],
	'7': ['S', 'W'],
	'F': ['S', 'E']
}

def GetNextMove(current, last):
	moves = valid_moves[input_lines[current[0]][current[1]]]
	if tuple(map(sum, zip(current, directions[moves[0]]))) != last:
		return tuple(map(sum, zip(current, directions[moves[0]])))
	else:
		return tuple(map(sum, zip(current, directions[moves[1]])))

# Parse input
start = FindStart()

# Silver star
last_pos = (start[0], start[1])
current_pos = (start[0], start[1] + 1)
route = [current_pos]
while current_pos != start:
	next_pos = GetNextMove(current_pos, last_pos)
	route.append(next_pos)
	last_pos = current_pos
	current_pos = next_pos

print('Silver answer: ' + str(len(route) // 2))

# Gold star
clean_lines = [['.' for _ in range(140)] for _ in range(140)]
for i in route:
	clean_lines[i[0]][i[1]] = input_lines[i[0]][i[1]]
clean_lines[start[0]][start[1]] = 'L'
with open('input_gold.txt', 'w') as write_file:
	for line in clean_lines:
		write_file.write(''.join(line))
		write_file.write('\n')

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

print('Gold answer: ' + str(inside_spaces))
