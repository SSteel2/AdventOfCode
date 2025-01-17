import Util.input
import Util.PriorityQueue
import Util.directions

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def IsValidPosition(position, heat_map):
	return not (position[0] < 0 or position[0] >= len(heat_map) or position[1] < 0 or position[1] >= len(heat_map[0]))

def Move(position, path):
	for i in path:
		position = Util.directions.Move(position, i)
	return position

def CalculateForwardDistance(position, path, heat_map):
	distance = 0
	for i in path:
		position = Move(position, [i])
		distance += heat_map[position[0]][position[1]]
	return distance

def GetValidDistance(position, path, distances):
	dist = distances[position[0]][position[1]]
	if dist == -1:
		return dist
	for i in dist:
		if i[1][0] == path[-1] or i[1][0] == Util.directions.Inverse(path[-1]):
			return i[0]
	return -1

def StoreValidDistance(position, path, distance, distances):
	dist = distances[position[0]][position[1]]
	if dist == -1:
		distances[position[0]][position[1]] = [(distance, path)]
		return
	index = -1
	for i, val in enumerate(dist):
		if val[1][0] == path[-1] or val[1][0] == Util.directions.Inverse(path[-1]):
			index = i
			break
	if index == -1:
		distances[position[0]][position[1]].append((distance, path))
	else:
		distances[position[0]][position[1]][index] = (distance, path)

def DjikstraDistances(visit_queue, possible_paths, heat_map, distances):
	while len(visit_queue) > 0:
		queued_value = visit_queue.pop()
		start = (queued_value[0], queued_value[1])
		path = queued_value[2]
		start_distance = queued_value[3]
		current = Move(start, path)
		stored_distance = GetValidDistance(current, path, distances) 
		new_distance = start_distance + CalculateForwardDistance(start, path, heat_map)
		if stored_distance == -1 or stored_distance > new_distance:
			StoreValidDistance(current, path, new_distance, distances)
			for possible_path in possible_paths:
				if possible_path[0] == path[0] or possible_path[0] == Util.directions.Inverse(path[0]):
					continue
				if IsValidPosition(Move(current, possible_path), heat_map):
					visit_queue.append(new_distance, (current[0], current[1], possible_path, new_distance))	

def _calculateDistance(input_lines, step_range):
	heat_map = [[int(j) for j in i] for i in input_lines]
	distances = [[-1 for _ in heat_map[0]] for _ in heat_map] # list of tuples (dist, direction)
	distances[0][0] = [(0, ['S'])]
	possible_paths = []
	for d in ['R', 'D', 'L', 'U']:  # this order is required specifically
		for i in step_range:
			possible_paths.append([d] * i)
	visit_queue = Util.PriorityQueue.PriorityQueue()
	for i in possible_paths[:len(possible_paths) // 2]:
		visit_queue.append(heat_map[0][0], (0, 0, i, 0))
	DjikstraDistances(visit_queue, possible_paths, heat_map, distances)
	return min(distances[-1][-1], key=lambda x: x[0])[0]

def silver(input_lines):
	return _calculateDistance(input_lines, range(1, 4))

def gold(input_lines):
	return _calculateDistance(input_lines, range(4, 11))
