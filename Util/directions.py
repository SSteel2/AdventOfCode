DirectionsTable = {
	'U': (-1, 0),
	'R': (0, 1),
	'D': (1, 0),
	'L': (0, -1)
}

DirectionsTableDiagonals = {
	'U': (-1, 0),
	'UR': (-1, 1),
	'R': (0, 1),
	'DR': (1, 1),
	'D': (1, 0),
	'DL': (1, -1),
	'L': (0, -1),
	'UL': (-1, -1)
}

InverseDirectionsTable = {
	'U': 'D',
	'R': 'L',
	'D': 'U',
	'L': 'R',
}

ClockwiseRotations = ['U', 'R', 'D', 'L']

# This line below is the coolest way to move in a grid, but unfortunately it is significantly slower than just using simple addition
# tuple(map(sum, zip(position, DirectionsTable[direction])))

def Move(position, direction):
	return (position[0] + DirectionsTableDiagonals[direction][0], position[1] + DirectionsTableDiagonals[direction][1])

def MoveMultiple(position, direction, count):
	return tuple(map(sum, zip(position, tuple(i * count for i in DirectionsTable[direction]))))

def MoveCustom(position, custom_direction):
	return (position[0] + custom_direction[0], position[1] + custom_direction[1])

def MoveMultipleCustom(position, custom_direction, count):
	return (position[0] + custom_direction[0] * count, position[1] + custom_direction[1] * count)

def ManhattanDistance(start_position, end_position):
	return abs(start_position[0] - end_position[0]) + abs(start_position[1] - end_position[1])

def Convert(graph, conversion_table):
	new_graph = [[c for c in line] for line in graph]
	for l, line in enumerate(graph):
		for c, char in enumerate(line):
			if char in conversion_table:
				new_graph[l][c] = conversion_table[char]
	return new_graph

def Inverse(direction):
	if direction not in InverseDirectionsTable:
		return direction
	else:
		return InverseDirectionsTable[direction]

def RotateClockwise(direction):
	return ClockwiseRotations[(ClockwiseRotations.index(direction) + 1) % len(ClockwiseRotations)]

def Get(table, position):
	return table[position[0]][position[1]]

def Set(table, position, value):
	table[position[0]][position[1]] = value

def IsOutOfBounds(table, position):
	return position[0] >= len(table) or position[0] < 0 or position[1] >= len(table[0]) or position[1] < 0

def PadTable(table, pad_count, pad_symbol):
	padded_table = [[pad_symbol for i in range(len(table[0]) + pad_count * 2)] for j in range(len(table) + pad_count * 2)]
	for line_num, line in enumerate(table):
		for col_num, col in enumerate(line):
			padded_table[line_num + pad_count][col_num + pad_count] = col
	return padded_table

def Count(table, value):
	count = 0
	for line in table:
		for col in line:
			if col == value:
				count += 1
	return count

def PrintTable(table):
	'''Debugging helper'''
	for line in table:
		print(''.join([str(i) for i in line]))
