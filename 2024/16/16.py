import Util.input
import Util.PriorityQueue
import Util.directions
import math

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _find(grid, marker):
	for line_num, line in enumerate(grid):
		for col_num, col in enumerate(line):
			if col == marker:
				return (line_num, col_num)

def _manhattan_distance(a, b):
	return abs(a[0] - b[0]) + abs(a[1] - b[1])

def _get_next_cell(position, grid, direction):
	# gets next cell in traversal path
	for current_direction in Util.directions.DirectionsTable:
		if current_direction == Util.directions.Inverse(direction):
			continue
		next_position = Util.directions.Move(position, current_direction)
		if Util.directions.Get(grid, next_position) != '#':
			return {'position': next_position, 'direction': current_direction}
	return None

def _is_node(position, grid, terminal_position):
	# if Util.directions.Get(grid, position) in ['E', 'S']:
	if position == terminal_position:
		return True
	non_wall_count = 0
	for direction in Util.directions.DirectionsTable:
		if Util.directions.Get(grid, Util.directions.Move(position, direction)) != "#":
			non_wall_count += 1
	return non_wall_count > 2

def _find_next_node(current, direction, grid, terminal_position):
	next_position = Util.directions.Move(current, direction)
	if Util.directions.Get(grid, next_position) == '#':
		return None
	distance = 1
	while not _is_node(next_position, grid, terminal_position):
		next_vector = _get_next_cell(next_position, grid, direction)
		if next_vector == None:
			return None
		if next_vector['direction'] != direction:
			distance += 1000
			direction = next_vector['direction']
		distance += 1
		next_position = next_vector['position']
	return {'position': next_position, 'facing': direction, 'distance': distance}

def _find_next_nodes(current, grid, facing, terminal_position):
	# returns list of nodes with distance and facings [{'position': (y, x), 'facing': 'X', 'distance': 999}, ...]
	nodes = []
	for direction in Util.directions.DirectionsTable:
		if direction == Util.directions.Inverse(facing):
			continue
		node = _find_next_node(current, direction, grid, terminal_position)
		if node != None:
			if direction != facing:
				node['distance'] += 1000
			nodes.append(node)
	return nodes

def silver(input_lines):
	start = _find(input_lines, 'S')
	end = _find(input_lines, 'E')
	best_distance = math.inf
	nodes = {start: {'distance': 0, 'facing': 'R'}}
	queue = Util.PriorityQueue.PriorityQueue()
	queue.append(_manhattan_distance(start, end), start)
	while len(queue) > 0:
		current = queue.pop()
		if nodes[current]['distance'] > best_distance:
			continue
		facing = nodes[current]['facing']
		next_nodes = _find_next_nodes(current, input_lines, facing, end)
		for next_node in next_nodes:
			next_distance = next_node['distance'] + nodes[current]['distance']
			if next_node['position'] not in nodes or next_distance < nodes[next_node['position']]['distance']:
				nodes[next_node['position']] = {'distance': next_distance, 'facing': next_node['facing']}
				if next_node['position'] == end:
					if nodes[next_node['position']]['distance'] < best_distance:
						best_distance = nodes[next_node['position']]['distance']
				else:
					queue.append(next_distance + _manhattan_distance(next_node['position'], end), next_node['position'])
	return best_distance

def _add_node_distances(node1, node2):
	turning_distance = 0
	if node1['facing'] != Util.directions.Inverse(node2['facing']):
		turning_distance = 1000
	return node1['distance'] + node2['distance'] + turning_distance

def _mark_path(grid, location, facing, terminal_position):
	# go in direction and mark all cells until next node
	if Util.directions.Get(grid, location) == '#':
		return # should not happen

	# print(location)
	Util.directions.Set(grid, location, 'X')	
	while not _is_node(location, grid, terminal_position):
		# location, facing = _get_next_cell(location, grid, facing)
		cell = _get_next_cell(location, grid, facing)
		# print(cell)
		location = cell['position']
		facing = cell['direction']
		# print(location)
		Util.directions.Set(grid, location, 'X')

def _mark_fastest_path(grid, location, direction, distance, goal, nodes, terminal_position):
	# print("_mark_fastest_path", location, direction, distance)
	if Util.directions.Get(grid, location) == '#':
		return
	candidate_node = _find_next_node(location, direction, grid, terminal_position)
	if candidate_node == None:
		return
	# print(candidate_node, nodes[candidate_node['position']], _add_node_distances(nodes[candidate_node['position']], candidate_node))
	if candidate_node is not None and candidate_node['position'] in nodes and _add_node_distances(nodes[candidate_node['position']], candidate_node) == distance:
		_mark_path(grid, location, direction, terminal_position)
		# call _mark_fastest_path on all directions except for one that came from with reduced distance
		for current_direction in Util.directions.DirectionsTable:
			if current_direction == Util.directions.Inverse(candidate_node['facing']):
				continue
			current_distance = distance - candidate_node['distance'] - 1
			if current_direction != candidate_node['facing']:
				current_distance -= 1000
			_mark_fastest_path(grid, Util.directions.Move(candidate_node['position'], current_direction), current_direction, current_distance, goal, nodes, terminal_position)

def gold(input_lines):
	start = _find(input_lines, 'S')
	end = _find(input_lines, 'E')
	best_distance = math.inf
	nodes = {start: {'distance': 0, 'facing': 'R'}}
	queue = Util.PriorityQueue.PriorityQueue()
	queue.append(_manhattan_distance(start, end), start)
	while len(queue) > 0:
		current = queue.pop()
		if nodes[current]['distance'] > best_distance:
			continue
		facing = nodes[current]['facing']
		next_nodes = _find_next_nodes(current, input_lines, facing, end)
		for next_node in next_nodes:
			next_distance = next_node['distance'] + nodes[current]['distance']
			if next_node['position'] not in nodes or next_distance < nodes[next_node['position']]['distance']:
				nodes[next_node['position']] = {'distance': next_distance, 'facing': next_node['facing']}
				if next_node['position'] == end:
					if nodes[next_node['position']]['distance'] < best_distance:
						best_distance = nodes[next_node['position']]['distance']
				else:
					queue.append(next_distance + _manhattan_distance(next_node['position'], end), next_node['position'])

	# for i in nodes:
	# 	print(i, nodes[i])

	grid = [[i for i in line] for line in input_lines]
	Util.directions.Set(grid, end, 'X')

	# reconstruct path
	for direction in Util.directions.DirectionsTable:
		next_location = Util.directions.Move(end, direction)
		_mark_fastest_path(grid, next_location, direction, best_distance - 1, start, nodes, start)

	# Util.directions.PrintTable(grid)

	return Util.directions.Count(grid, 'X')
