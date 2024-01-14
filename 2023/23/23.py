import collections
import Util.input
import Util.directions

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _getBoundaryLocations(input_lines):
	for i, col in enumerate(input_lines[0]):
		if col == '.':
			global_start = (0, i)
	for i, col in enumerate(input_lines[-1]):
		if col == '.':
			global_end = (len(input_lines) - 1, i)
	return global_start, global_end

def _mapValue(position, input_lines):
	return input_lines[position[0]][position[1]]

def _isValid(position, input_lines):
	if position[0] >= len(input_lines) or position[0] < 0 or position[1] >= len(input_lines[0]) or position[1] < 0 or _mapValue(position, input_lines) == '#':
		return False
	return True

def _getBranch(tree, start):
	for i in tree:
		if i['start'] == start:
			return i
	return None

def _findNextPosition(current, last, input_lines, global_end):
	if _mapValue(current, input_lines) in Util.directions.DirectionsTable:
		return [(Util.directions.Move(current, _mapValue(current, input_lines)), False)]
	possible_positions = []
	for direction in Util.directions.DirectionsTable:
		is_end_pos = False
		next_pos = Util.directions.Move(current, direction)
		if not _isValid(next_pos, input_lines) or last == next_pos or Util.directions.Inverse(_mapValue(next_pos, input_lines)) == direction:
			continue  # invalid position
		if _mapValue(next_pos, input_lines) in Util.directions.DirectionsTable or next_pos == global_end:
			is_end_pos = True
		possible_positions.append((next_pos, is_end_pos))
	return possible_positions

def _constructPath(start, input_lines, global_end):
	moving = True
	current = start
	last_pos = None
	current_length = 0
	while moving:
		next_positions = _findNextPosition(current, last_pos, input_lines, global_end)
		if next_positions[0][1]:
			moving = False
			if next_positions[0][0] == global_end:
				return {'start': start, 'length': current_length + 1, 'end': []}
		else:
			current, last_pos = next_positions[0][0], current
		current_length += 1
	return {'start': start, 'length': current_length, 'end': [i[0] for i in next_positions]}

def _constructPathTree(start, input_lines, global_end):
	tree = []
	queue = collections.deque()
	queue.appendleft(start)
	while len(queue) > 0:
		local_start = queue.pop()
		if _getBranch(tree, local_start) != None:
			continue
		branch = _constructPath(local_start, input_lines, global_end)
		tree.append(branch)
		for i in branch['end']:
			queue.appendleft(i)
	return tree

def _dfs(tree, start):
	current_length = 0
	current = _getBranch(tree, start)
	current_length += current['length']
	if len(current['end']) == 0:
		return current_length
	max_length = -1
	for i in current['end']:
		l = _dfs(tree, i)
		if l > max_length:
			max_length = l
	return current_length + max_length

def silver(input_lines):
	chart = Util.directions.Convert(input_lines, {'^': 'U', '<': 'L', 'v': 'D', '>': 'R'})
	global_start, global_end = _getBoundaryLocations(chart)
	tree = _constructPathTree(global_start, chart, global_end)
	result = _dfs(tree, global_start)
	return result

def _findNextPositionGold(current, last, input_lines):
	possible_positions = []
	for direction in Util.directions.DirectionsTable:
		next_pos = Util.directions.Move(current, direction)
		if not _isValid(next_pos, input_lines) or last == next_pos:
			continue  # invalid position
		possible_positions.append(next_pos)
	return possible_positions

def _constructEdges(start, input_lines):
	edges = []
	for direction in Util.directions.DirectionsTable:
		next_pos = Util.directions.Move(start, direction)
		if not _isValid(next_pos, input_lines):
			continue

		moving = True
		current = next_pos
		last_pos = start
		current_length = 0

		while moving:
			next_positions = _findNextPositionGold(current, last_pos, input_lines)
			if len(next_positions) == 1:
				current, last_pos = next_positions[0], current
			else:
				moving = False
			current_length += 1
		edges.append({'start': start, 'length': current_length, 'end': current}) # check for same end
	return edges

def _getEdge(graph, start, end):
	for edge in graph:
		if edge['start'] == start and edge['end'] == end:
			return edge
	return None

def _constructPathGraph(start, input_lines):
	graph = []
	visited_nodes = [start]
	queue = collections.deque()
	queue.appendleft(start)
	count = 100
	while len(queue) > 0 and count > 0:
		count -= 1
		local_start = queue.pop()
		edges = _constructEdges(local_start, input_lines)
		visited_nodes.append(local_start)
		for i in edges:
			inverse_edge = _getEdge(graph, i['end'], i['start'])
			if inverse_edge == None:
				graph.append(i)
			else:
				if inverse_edge['length'] < i['length']:
					inverse_edge['length'] = i['length']
			if i['end'] not in visited_nodes and i['end'] not in queue:
				queue.appendleft(i['end'])
	return graph

def _getEdges(graph, node):
	edges = []
	for edge in graph:
		if edge['start'] == node or edge['end'] == node:
			edges.append(edge)
	return edges

def _otherEnd(edge, node):
	if node == edge['start']:
		return edge['end']
	elif node == edge['end']:
		return edge['start']
	else:
		print("very very bad")

def _backtracking(graph, start, length, visited, global_end):
	if start == global_end:
		return length

	visited_nodes = [start] + visited
	edges = _getEdges(graph, start)
	max_length = 0
	for edge in edges:
		end = _otherEnd(edge, start)
		if end not in visited_nodes:
			l = _backtracking(graph, end, length + edge['length'], visited_nodes, global_end)
			if l > max_length:
				max_length = l
	return max_length

def gold(input_lines):
	global_start, global_end = _getBoundaryLocations(input_lines)
	graph = _constructPathGraph(global_start, input_lines)
	result = _backtracking(graph, global_start, 0, [], global_end)
	return result
