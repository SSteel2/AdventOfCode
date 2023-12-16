input_lines = []
with open('input.txt', 'r') as input_file:
	for line in input_file:
		input_lines.append(line.removesuffix('\n'))

# Parse input
energy = [['.' for _ in input_lines[0]] for _ in input_lines]

directions = {
	'U': (-1, 0),
	'R': (0, 1),
	'D': (1, 0),
	'L': (0, -1)
}

mirror_left = '\\'
mirror_right = '/'
splitter_vertical = '|'
splitter_horizontal = '-'

mirror_left_table = {
	'U': 'L',
	'R': 'D',
	'D': 'R',
	'L': 'U'
}
mirror_right_table = {
	'U': 'R',
	'R': 'U',
	'D': 'L',
	'L': 'D'
}

# Silver star

def MoveBeam(current_pos, direction):
	if not (current_pos[0] < 0 or current_pos[0] >= len(input_lines) or current_pos[1] < 0 or current_pos[1] >= len(input_lines[0])):
		energy[current_pos[0]][current_pos[1]] = '#'
	new_pos = tuple(map(sum, zip(current_pos, directions[direction])))
	if new_pos[0] < 0 or new_pos[0] >= len(input_lines) or new_pos[1] < 0 or new_pos[1] >= len(input_lines[0]):
		return []  # no move
	symbol = input_lines[new_pos[0]][new_pos[1]]
	if symbol == '.':
		return [(new_pos[0], new_pos[1], direction)]
	elif symbol == mirror_left:
		return [(new_pos[0], new_pos[1], mirror_left_table[direction])]
	elif symbol == mirror_right:
		return [(new_pos[0], new_pos[1], mirror_right_table[direction])]
	elif symbol == splitter_vertical:
		if direction == 'U' or direction == 'D':
			return [(new_pos[0], new_pos[1], direction)]
		else:
			return [(new_pos[0], new_pos[1], 'U'), (new_pos[0], new_pos[1], 'D')]
	elif symbol == splitter_horizontal:
		if direction == 'R' or direction == 'L':
			return [(new_pos[0], new_pos[1], direction)]
		else:
			return [(new_pos[0], new_pos[1], 'R'), (new_pos[0], new_pos[1], 'L')]

def CountEnergy(energy):
	count = 0
	for i in energy:
		for j in i:
			if j == '#':
				count += 1
	return count

def LaunchBeam(start_beam):
	visited_beams = []
	current_beams = [start_beam]
	while len(current_beams) > 0:
		beam = current_beams.pop()
		if beam in visited_beams:
			continue
		visited_beams.append(beam)
		new_beams = MoveBeam(beam[:2], beam[2])
		current_beams.extend(new_beams)

LaunchBeam((0, -1, 'R'))
print('Silver answer: ' + str(CountEnergy(energy)))

# Gold star

possible_starts = []
for i in range(len(input_lines)):
	possible_starts.append((i, -1, 'R'))
	possible_starts.append((i, len(input_lines[0]), 'L'))
	possible_starts.append((-1, i, 'D'))
	possible_starts.append((len(input_lines), i, 'U'))

counts = []
for start in possible_starts:
	energy = [['.' for _ in input_lines[0]] for _ in input_lines]
	LaunchBeam(start)
	counts.append(CountEnergy(energy))

print('Gold answer: ' + str(max(counts)))
