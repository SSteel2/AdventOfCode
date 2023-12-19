input_lines = []
with open('input.txt', 'r') as input_file:
	for line in input_file:
		input_lines.append(line.removesuffix('\n'))

# Parse input
heat_map = [[int(j) for j in i] for i in input_lines]

directions_map = {
	'U': (-1, 0),
	'R': (0, 1),
	'D': (1, 0),
	'L': (0, -1)
}

inverse_directions = {
	'U': 'D',
	'R': 'L',
	'D': 'U',
	'L': 'R',
	'S': 'S'
}

# Silver star

class PriorityQueue:
	def __init__(self):
		self.values = {}

	def append(self, priority, value):
		if priority in self.values:
			self.values[priority].append(value)
		else:
			self.values[priority] = [value]

	def pop(self):
		low_key = min(self.values)
		if len(self.values[low_key]) == 1:
			result = self.values[low_key][0]
			del self.values[low_key]
			return result
		else:
			return self.values[low_key].pop()

	def __len__(self):
		return len(self.values)

def IsValidPosition(position):
	if position[0] < 0 or position[0] >= len(heat_map) or position[1] < 0 or position[1] >= len(heat_map[0]):
		return False
	return True

def Move(position, path):
	for i in path:
		position = tuple(map(sum, zip(position, directions_map[i])))
	return position

def CalculateForwardDistance(position, path):
	distance = 0
	for i in path:
		position = Move(position, [i])
		distance += heat_map[position[0]][position[1]]
	return distance

def GetValidDistance(position, path):
	dist = distances[position[0]][position[1]]
	if dist == -1:
		return dist
	for i in dist:
		if i[1][0] == path[-1] or i[1][0] == inverse_directions[path[-1]]:
			return i[0]
	return -1

def StoreValidDistance(position, path, distance):
	dist = distances[position[0]][position[1]]
	if dist == -1:
		distances[position[0]][position[1]] = [(distance, path)]
		return
	index = -1
	for i, val in enumerate(dist):
		if val[1][0] == path[-1] or val[1][0] == inverse_directions[path[-1]]:
			index = i
			break
	if index == -1:
		distances[position[0]][position[1]].append((distance, path))
	else:
		distances[position[0]][position[1]][i] = (distance, path)


def DjikstraDistances(visit_queue, possible_paths):
	while len(visit_queue) > 0:
		queued_value = visit_queue.pop()
		start = (queued_value[0], queued_value[1])
		path = queued_value[2]
		start_distance = queued_value[3]
		current = Move(start, path)
		stored_distance = GetValidDistance(current, path) 
		new_distance = start_distance + CalculateForwardDistance(start, path)
		if stored_distance == -1 or stored_distance > new_distance:
			StoreValidDistance(current, path, new_distance)
			for possible_path in possible_paths:
				if possible_path[0] == path[0] or possible_path[0] == inverse_directions[path[0]]:
					continue
				if IsValidPosition(Move(current, possible_path)):
					visit_queue.append(new_distance, (current[0], current[1], possible_path, new_distance))	

distances = [[-1 for _ in heat_map[0]] for _ in heat_map] # list of tuples (dist, direction)
distances[0][0] = [(0, ['S'])]
visit_queue = PriorityQueue()
visit_queue.append(heat_map[0][0], (0, 0, ['R'], 0))
visit_queue.append(heat_map[0][0], (0, 0, ['R', 'R'], 0))
visit_queue.append(heat_map[0][0], (0, 0, ['R', 'R', 'R'], 0))
visit_queue.append(heat_map[0][0], (0, 0, ['D'], 0))
visit_queue.append(heat_map[0][0], (0, 0, ['D', 'D'], 0))
visit_queue.append(heat_map[0][0], (0, 0, ['D', 'D', 'D'], 0))

possible_paths = [['R'], ['R', 'R'], ['R', 'R', 'R'], ['D'], ['D', 'D'], ['D', 'D', 'D'], ['L'], ['L', 'L'], ['L', 'L', 'L'], ['U'], ['U', 'U'], ['U', 'U', 'U']]

DjikstraDistances(visit_queue, possible_paths)

print('Silver answer: ' + str(min(distances[-1][-1], key=lambda x: x[0])[0]))

# Gold star

distances = [[-1 for _ in heat_map[0]] for _ in heat_map] # list of tuples (dist, direction)
distances[0][0] = [(0, ['S'])]
visit_queue = PriorityQueue()
visit_queue.append(heat_map[0][0], (0, 0, ['R', 'R', 'R', 'R'], 0))
visit_queue.append(heat_map[0][0], (0, 0, ['R', 'R', 'R', 'R', 'R'], 0))
visit_queue.append(heat_map[0][0], (0, 0, ['R', 'R', 'R', 'R', 'R', 'R'], 0))
visit_queue.append(heat_map[0][0], (0, 0, ['R', 'R', 'R', 'R', 'R', 'R', 'R'], 0))
visit_queue.append(heat_map[0][0], (0, 0, ['R', 'R', 'R', 'R', 'R', 'R', 'R', 'R'], 0))
visit_queue.append(heat_map[0][0], (0, 0, ['R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R'], 0))
visit_queue.append(heat_map[0][0], (0, 0, ['R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R'], 0))
visit_queue.append(heat_map[0][0], (0, 0, ['D', 'D', 'D', 'D'], 0))
visit_queue.append(heat_map[0][0], (0, 0, ['D', 'D', 'D', 'D', 'D'], 0))
visit_queue.append(heat_map[0][0], (0, 0, ['D', 'D', 'D', 'D', 'D', 'D'], 0))
visit_queue.append(heat_map[0][0], (0, 0, ['D', 'D', 'D', 'D', 'D', 'D', 'D'], 0))
visit_queue.append(heat_map[0][0], (0, 0, ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D'], 0))
visit_queue.append(heat_map[0][0], (0, 0, ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D'], 0))
visit_queue.append(heat_map[0][0], (0, 0, ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D'], 0))

possible_paths = [
	['R', 'R', 'R', 'R'],
	['R', 'R', 'R', 'R', 'R'],
	['R', 'R', 'R', 'R', 'R', 'R'],
	['R', 'R', 'R', 'R', 'R', 'R', 'R'],
	['R', 'R', 'R', 'R', 'R', 'R', 'R', 'R'],
	['R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R'],
	['R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R'],
	['D', 'D', 'D', 'D'],
	['D', 'D', 'D', 'D', 'D'],
	['D', 'D', 'D', 'D', 'D', 'D'],
	['D', 'D', 'D', 'D', 'D', 'D', 'D'],
	['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D'],
	['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D'],
	['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D'],
	['L', 'L', 'L', 'L'],
	['L', 'L', 'L', 'L', 'L'],
	['L', 'L', 'L', 'L', 'L', 'L'],
	['L', 'L', 'L', 'L', 'L', 'L', 'L'],
	['L', 'L', 'L', 'L', 'L', 'L', 'L', 'L'],
	['L', 'L', 'L', 'L', 'L', 'L', 'L', 'L', 'L'],
	['L', 'L', 'L', 'L', 'L', 'L', 'L', 'L', 'L', 'L'],
	['U', 'U', 'U', 'U'],
	['U', 'U', 'U', 'U', 'U'],
	['U', 'U', 'U', 'U', 'U', 'U'],
	['U', 'U', 'U', 'U', 'U', 'U', 'U'],
	['U', 'U', 'U', 'U', 'U', 'U', 'U', 'U'],
	['U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U'],
	['U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U']]

DjikstraDistances(visit_queue, possible_paths)

print('Gold answer: ' + str(min(distances[-1][-1], key=lambda x: x[0])[0]))
