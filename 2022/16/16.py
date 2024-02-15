import Util.input
import Util.PriorityQueue
from collections import deque

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(input_lines):
	rooms = {}
	for line in input_lines:
		split_line = line.split(' ')
		room = {}
		room['rate'] = int(split_line[4][5:-1])
		room['neighbours'] = [i.removesuffix(',') for i in split_line[9:]]
		rooms[split_line[1]] = room
	return rooms

def _bfs(rooms, room):
	queue = deque()
	queue.append(room)
	distances = {room: 0}
	while len(queue) > 0:
		current = queue.popleft()
		current_distance = distances[current]
		for neighbour in rooms[current]['neighbours']:
			if neighbour in distances:
				continue
			distances[neighbour] = current_distance + 1
			queue.append(neighbour)
	return distances

def _createTraversalRoutes(room, room_names, distances):
	routes = {}
	for i in room_names:
		routes[i] = []
		if room == i:
			continue
		for traverse_room in room_names:
			if traverse_room == i or traverse_room == room:
				continue
			if distances[room][i] == distances[room][traverse_room] + distances[traverse_room][i]:
				routes[i].append(traverse_room)
	return routes

def _createDenseGraph(rooms):
	goal_rooms = [i for i in rooms if rooms[i]['rate'] > 0]
	goal_rooms.append('AA')
	traversal_graph = {}
	for i in goal_rooms:
		distances = _bfs(rooms, i)
		traversal_graph[i] = {}
		for j in goal_rooms:
			traversal_graph[i][j] = distances[j]
		traversal_graph[i][i] = 0

	traversal_routes = {}
	for room in goal_rooms:
		traversal_routes[room] = _createTraversalRoutes(room, goal_rooms, traversal_graph)
	return goal_rooms, traversal_graph, traversal_routes

def _isPathEfficient(start_node, end_node, value_gain, routes, visited, distances, rooms, max_time):
	for route in routes[start_node][end_node]:
		if route in visited:
			continue
		possible_value = (max_time - distances[start_node][route] - 1) * rooms[route]['rate'] + \
			(max_time - distances[start_node][route] - 1 - distances[route][end_node] - 1) * rooms[end_node]['rate']
		if possible_value > value_gain:
			return False
	return True

def _walk(max_time, names, distances, routes, rooms, is_return_positions=False, disabled_nodes=[]):
	queue = Util.PriorityQueue.PriorityQueue()
	start_node = 'AA'
	queue.append(0, {'distance': 0, 'value': 0, 'path': disabled_nodes + [start_node]})

	max_value = 0
	end_positions = []
	while len(queue) > 0:
		current = queue.pop()
		is_moving = False
		for name in names:
			if name in current['path'] or name == start_node:
				continue
			new_distance = current['distance'] + distances[current['path'][-1]][name] + 1
			if new_distance > max_time:
				continue

			value_gain = (max_time - new_distance) * rooms[name]['rate']
			if not _isPathEfficient(current['path'][-1], name, value_gain, routes, current['path'], distances, rooms, max_time):
				continue

			new_value = current['value'] + value_gain
			new_path = current['path'] + [name]
			if new_value > max_value:
				max_value = new_value
			current_position = {'distance': new_distance, 'value': new_value, 'path': new_path}

			queue.append(new_distance, current_position)
			is_moving = True
		if is_return_positions and not is_moving:
			end_positions.append(current)
	return end_positions if is_return_positions else max_value

def silver(input_lines):
	rooms = _parse(input_lines)
	names, distances, routes = _createDenseGraph(rooms)
	max_time = 30
	return _walk(max_time, names, distances, routes, rooms)

def gold(input_lines):
	rooms = _parse(input_lines)
	names, distances, routes = _createDenseGraph(rooms)
	max_time = 26
	end_positions = _walk(max_time, names, distances, routes, rooms, True)

	global_max_value = 0
	for end_position in end_positions:
		local_max_value = _walk(max_time, names, distances, routes, rooms, disabled_nodes=end_position['path'])
		if local_max_value + end_position['value'] > global_max_value:
			global_max_value = local_max_value + end_position['value']

	return global_max_value