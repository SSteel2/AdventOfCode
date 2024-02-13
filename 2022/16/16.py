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

def _createDenseGraph(rooms):
	goal_rooms = []
	for i in rooms:
		if rooms[i]['rate'] > 0:
			goal_rooms.append(i)
	# traversal_graph = [[0 for _ in goal_rooms] for _ in goal_rooms]
	traversal_graph = {}
	for i, room_i in enumerate(goal_rooms):
		distances = _bfs(rooms, room_i)
		traversal_graph[room_i] = distances
		# for j, room_j in enumerate(goal_rooms):
		# 	if room_i == room_j:
		# 		continue
		# 	# traversal_graph[i][j] = distances[room_j]
	return goal_rooms, traversal_graph

def silver(input_lines):
	rooms = _parse(input_lines)
	names, distances = _createDenseGraph(rooms)

	# print('  ' + ''.join([str(j).rjust(4, ' ') for j in names]))
	# for i in range(len(names)):
	# 	row = ''.join([str(j).rjust(4, ' ') for j in distances[i]])
	# 	print(f'{names[i]}{row}')

	start_distances = _bfs(rooms, 'AA')
	# print(start_distances)

	queue = Util.PriorityQueue.PriorityQueue()
	for name in names:
		queue.append(start_distances[name] + 1, {'distance': start_distances[name] + 1, 'visited': set([name]), 'value': (29 - start_distances[name]) * rooms[name]['rate'], 'path': [name]})

	max_value = 0
	max_path = []
	while len(queue) > 0:
		current = queue.pop()
		# print(current)
		for name in names:
			if name in current['visited']:
				continue
			# print(distances)
			# print(current['path'][-1])
			new_distance = current['distance'] + distances[current['path'][-1]][name] + 1
			if new_distance > 30:
				continue
			new_value = current['value'] + (30 - new_distance) * rooms[name]['rate']
			new_path = current['path'] + [name]
			if new_value > max_value:
				max_value = new_value
				max_path = new_path
			new_visited = current['visited'].copy()
			new_visited.add(name)
			current_position = {'distance': new_distance, 'visited': new_visited, 'value': new_value, 'path': new_path}

			queue.append(new_distance, current_position)
	# print(max_path)
	return max_value

	# for i in rooms:
	# 	print(i, rooms[i])

def gold(input_lines):
	pass
