DirectionsTable = {
	'U': (-1, 0),
	'R': (0, 1),
	'D': (1, 0),
	'L': (0, -1)
}

InverseDirectionsTable = {
	'U': 'D',
	'R': 'L',
	'D': 'U',
	'L': 'R',
}

def Move(position, direction):
	return tuple(map(sum, zip(position, DirectionsTable[direction])))

def MoveMultiple(position, direction, count):
	return tuple(map(sum, zip(position, tuple(i * count for i in DirectionsTable[direction]))))

def MoveCustom(position, custom_direction):
	return tuple(map(sum, zip(position, custom_direction)))

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

def Get(table, position):
	return table[position[0]][position[1]]

def Set(table, position, value):
	table[position[0]][position[1]] = value
