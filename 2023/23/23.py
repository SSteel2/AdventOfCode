import collections

input_lines = []
with open('input.txt', 'r') as input_file:
	for line in input_file:
		input_lines.append(line.removesuffix('\n'))

# Parse input
directions_map = {
	'^': (-1, 0),
	'>': (0, 1),
	'v': (1, 0),
	'<': (0, -1)
}

inverse_directions_map = {
	'^': 'v',
	'>': '<',
	'v': '^',
	'<': '>',
	'.': '.'
}

for i, col in enumerate(input_lines[0]):
	if col == '.':
		global_start = (0, i)
for i, col in enumerate(input_lines[-1]):
	if col == '.':
		global_end = (len(input_lines) - 1, i)

def MapValue(position):
	return input_lines[position[0]][position[1]]

def NextPosition(position, direction):
	return tuple(map(sum, zip(directions_map[direction], position)))

def IsValid(position):
	if position[0] >= len(input_lines) or position[0] < 0 or position[1] >= len(input_lines[0]) or position[1] < 0 or MapValue(position) == '#':
		return False
	return True

def GetBranch(tree, start):
	for i in tree:
		if i['start'] == start:
			return i
	return None

def FindNextPosition(current, last):
	# print(f"FindNextPosition {current} {last}")
	if MapValue(current) in directions_map:
		return [(NextPosition(current, MapValue(current)), False)]
	possible_positions = []
	for direction in directions_map:
		is_end_pos = False
		next_pos = NextPosition(current, direction)
		if not IsValid(next_pos) or last == next_pos or inverse_directions_map[MapValue(next_pos)] == direction:
			continue  # invalid position
		if MapValue(next_pos) in directions_map or next_pos == global_end:
			is_end_pos = True
		possible_positions.append((next_pos, is_end_pos))
	return possible_positions

def ConstructPath(start):
	# print(f"ConstructPath {start}")
	moving = True
	current = start
	last_pos = None
	current_length = 0
	while moving:
		next_positions = FindNextPosition(current, last_pos)
		if next_positions[0][1]:
			moving = False
			if next_positions[0][0] == global_end:
				return {'start': start, 'length': current_length + 1, 'end': []}
		else:
			current, last_pos = next_positions[0][0], current
		current_length += 1
	return {'start': start, 'length': current_length, 'end': [i[0] for i in next_positions]}

def ConstructPathTree(start):
	# print(f"ConstructPathTree {start}")
	tree = []
	queue = collections.deque()
	queue.appendleft(start)
	while len(queue) > 0:
		local_start = queue.pop()
		if GetBranch(tree, local_start) != None:
			continue
		branch = ConstructPath(local_start)
		tree.append(branch)
		for i in branch['end']:
			queue.appendleft(i)
	return tree

tree = ConstructPathTree(global_start)

# debug start
# for i in tree:
# 	print(i)
# debug end

# Silver star

def dfs(tree, start):
	current_length = 0
	current = GetBranch(tree, start)
	current_length += current['length']
	if len(current['end']) == 0:
		return current_length
	max_length = -1
	for i in current['end']:
		l = dfs(tree, i)
		if l > max_length:
			max_length = l
	return current_length + max_length

result = dfs(tree, global_start)
print('Silver answer: ' + str(result))

# Gold star

def FindNextPositionGold(current, last):
	# print(f"FindNextPositionGold {current} {last}")
	possible_positions = []
	for direction in directions_map:
		next_pos = NextPosition(current, direction)
		if not IsValid(next_pos) or last == next_pos:
			continue  # invalid position
		possible_positions.append(next_pos)
	return possible_positions

def ConstructEdges(start):
	# print(f"ConstructEdges {start}")
	edges = []
	for direction in directions_map:
		next_pos = NextPosition(start, direction)
		if not IsValid(next_pos):
			continue

		moving = True
		current = next_pos
		last_pos = start
		current_length = 0

		while moving:
			next_positions = FindNextPositionGold(current, last_pos)
			if len(next_positions) == 1:
				current, last_pos = next_positions[0], current
			else:
				moving = False
			current_length += 1
		edges.append({'start': start, 'length': current_length, 'end': current}) # check for same end
	return edges

def GetEdge(graph, start, end):
	for edge in graph:
		if edge['start'] == start and edge['end'] == end:
			return edge
	return None

def ConstructPathGraph(start):
	# print(f"ConstructPathGraph {start}")
	graph = []
	visited_nodes = [start]
	queue = collections.deque()
	queue.appendleft(start)
	count = 100
	while len(queue) > 0 and count > 0:
		count -= 1
		# print(queue)
		local_start = queue.pop()
		edges = ConstructEdges(local_start)
		visited_nodes.append(local_start)
		for i in edges:
			inverse_edge = GetEdge(graph, i['end'], i['start'])
			if inverse_edge == None:
				graph.append(i)
			else:
				if inverse_edge['length'] < i['length']:
					inverse_edge['length'] = i['length']
			if i['end'] not in visited_nodes and i['end'] not in queue:
				queue.appendleft(i['end'])
	return graph

graph = ConstructPathGraph(global_start)

# debug start
# for i in graph:
# 	print(i)
# debug end

def GetEdges(graph, node):
	edges = []
	for edge in graph:
		if edge['start'] == node or edge['end'] == node:
			edges.append(edge)
	return edges

def OtherEnd(edge, node):
	if node == edge['start']:
		return edge['end']
	elif node == edge['end']:
		return edge['start']
	else:
		print("very very bad")

def backtracking(graph, start, length, visited):
	if start == global_end:
		return length

	visited_nodes = [start] + visited
	edges = GetEdges(graph, start)
	max_length = 0
	for edge in edges:
		end = OtherEnd(edge, start)
		if end not in visited_nodes:
			l = backtracking(graph, end, length + edge['length'], visited_nodes)
			if l > max_length:
				max_length = l
	return max_length

result = backtracking(graph, global_start, 0, [])

print('Gold answer: ' + str(result))
