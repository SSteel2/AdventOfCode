import math

input_lines = []
with open('input_sample.txt', 'r') as input_file:
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

# Attempt no.1
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


def LastThreeDirectionsSame(current):
	last_cell = current[:]
	for i in range(3):
		last_cell_pos = tuple(map(sum, zip(last_cell[:2], directions_map[last_cell[2]])))
		last_direction = came_from[last_cell_pos[0]][last_cell_pos[1]]
		if last_direction != current[2]:
			return False
		last_cell = (last_cell_pos[0], last_cell_pos[1], last_direction)
	return True

visited = [[False for _ in heat_map[0]] for _ in heat_map]
distances = [[-1 for _ in heat_map[0]] for _ in heat_map] # list of tuples (dist, direction)
came_from = [[None for _ in heat_map[0]] for _ in heat_map]

distances[0][0] = [(0, ['S'])]
came_from[0][0] = ['S'] # start
visit_queue = PriorityQueue()
visit_queue.append(heat_map[0][0], (0, 0, ['R'], 0))
visit_queue.append(heat_map[0][0], (0, 0, ['R', 'R'], 0))
visit_queue.append(heat_map[0][0], (0, 0, ['R', 'R', 'R'], 0))
visit_queue.append(heat_map[0][0], (0, 0, ['D'], 0))
visit_queue.append(heat_map[0][0], (0, 0, ['D', 'D'], 0))
visit_queue.append(heat_map[0][0], (0, 0, ['D', 'D', 'D'], 0))

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

possible_paths = [['R'], ['R', 'R'], ['R', 'R', 'R'], ['D'], ['D', 'D'], ['D', 'D', 'D'], ['L'], ['L', 'L'], ['L', 'L', 'L'], ['U'], ['U', 'U'], ['U', 'U', 'U']]

start_count = 10000000
count = start_count
while len(visit_queue) > 0 and count > 0:
	queued_value = visit_queue.pop()
	start = (queued_value[0], queued_value[1])
	path = queued_value[2]
	start_distance = queued_value[3]
	current = Move(start, path)
	stored_distance = GetValidDistance(current, path) 

	# last_cell = tuple(map(sum, zip(directions_map[current[2]], current[:2])))

	new_distance = start_distance + CalculateForwardDistance(start, path)
	if stored_distance == -1 or stored_distance > new_distance:
		StoreValidDistance(current, path, new_distance)
		# came_from[current[0]][current[1]] = path

		# ??? idk if still needed		
		# next_visit_directions = list(directions_map.keys())
		# next_visit_directions.remove(inverse_directions[current[2]])

		for possible_path in possible_paths:
			if possible_path[0] == path[0] or possible_path[0] == inverse_directions[path[0]]:
				continue
			if IsValidPosition(Move(current, possible_path)):
				visit_queue.append(new_distance, (current[0], current[1], possible_path, new_distance))	
	count -= 1
print(f'Steps taken: {start_count - count}')

# debug path print

# for i, l in enumerate(distances):
# 	s = ""
# 	for j, c in enumerate(l):
# 		s += str(j) + ': ' + str(c)
# 	print(i, s)

print('Silver answer: ' + str(distances[-1][-1]))

# Attempt no.2
# heat_map = [[int(j) for j in i] for i in input_lines] 

# distances = [[-1 for _ in heat_map[0]] for _ in heat_map]
# directions = [[[] for _ in heat_map[0]] for _ in heat_map]
# distances[-1][-1] = heat_map[-1][-1]

def GetPath(line, col):
	# print(f"GetPath {line}, {col}")
	path = []
	current = (line, col)
	while current != (len(heat_map) - 1, len(heat_map[0]) - 1):
		current_directions = directions[current[0]][current[1]]
		path.extend(current_directions)
		for i in current_directions:
			current = tuple(map(sum, zip(current, directions_map[i])))
	return path

def GetPaths(line, col):
	# print(f"GetPaths {line}, {col}")
	paths = []
	current = (line, col)
	if current == (len(heat_map) - 1, len(heat_map[0]) - 1):
		return [[]]
	current_paths = directions[current[0]][current[1]]
	for path in current_paths:
		next_pos = current
		for i in path:
			next_pos = tuple(map(sum, zip(next_pos, directions_map[i])))
		new_paths = GetPaths(next_pos[0], next_pos[1])
		for i in new_paths:
			if len(path) > 0 and len(i) > 0 and path[-1] == inverse_directions[i[0]]:
				continue
			paths.append(path + i)
	return paths

def IsTopPathValid(line, col):
	paths = GetPaths(line, col)
	for path in paths:
		if len(path) <= 3:
			return True
		if not (path[0] == path[1] == path[2] == path[3]):
			return True
	return False

def Explore(line, col, path):
	# print(f"Explore {line}, {col}, {path}")
	# check is valid
	# if not valid
	# not valid if contains inverse at the end or no distance
	current_distance = 0
	last_cell = (line, col)
	for i in path:
		current_distance += heat_map[last_cell[0]][last_cell[1]]
		last_cell = tuple(map(sum, zip(last_cell, directions_map[i])))
		# if last_cell[0] >= len(heat_map) or last_cell[0] < 0 or last_cell[1] >= len(heat_map[0]) or last_cell[1] < 0:
		# 	return (math.inf, [])
	if distances[last_cell[0]][last_cell[1]] == -1:
		# only way this might happen if at current top left or left top
		# and might require a subsequent BlackMagic run...
		# if path[0] == 'L':
		# 	current_distance += heat_map[last_cell[0]][last_cell[1]]
		# 	path.append('D')
		# 	last_cell = tuple(map(sum, zip(last_cell, directions_map['D'])))
		# elif path[0] == 'U':
		# 	current_distance += heat_map[last_cell[0]][last_cell[1]]
		# 	path.append('R')
		# 	last_cell = tuple(map(sum, zip(last_cell, directions_map['R'])))
		return (math.inf, [])
	if len(directions[last_cell[0]][last_cell[1]]) == 0:
		return (math.inf, [])
	valid_end = False
	for d in directions[last_cell[0]][last_cell[1]]:
		if path[-1] != inverse_directions[d[0]]:
			valid_end = True
			break
	additional_details = None
	if not valid_end:
		# assuming that there is only one valid direction, it requires a blackmagic call if path not valid
		if directions[last_cell[0]][last_cell[1]][0][0] == 'D':
			additional_details = Explore(last_cell[0], last_cell[1], ['R'])
		elif directions[last_cell[0]][last_cell[1]][0][0] == 'R':
			additional_details = Explore(last_cell[0], last_cell[1], ['D'])
		else:
			print(f"This should not happen, it might, but then it requires fixing. last_cell {last_cell}")
		if additional_details != None:
			valid_end = True
	if len(directions[last_cell[0]][last_cell[1]]) == 0 or not valid_end:
		return (math.inf, [])
	if additional_details != None:
		current_distance += additional_details[0]
		return (current_distance, path + additional_details[1])
	else:
		current_distance += distances[last_cell[0]][last_cell[1]]
		return (current_distance, path)

def BlackMagic(line, col):
	print(f"BlackMagic {line}, {col}")
	# if top path is not valid
	# it will either be down or right
	# down:
	distance_paths = []
	paths = GetPaths(line, col)
	current = (line, col)
	# 8 possible options L or R on each of the top 4
	explored_down = False
	explored_right = False
	for path in paths:
		if path[0] == 'D':
			if not explored_down:
				if col + 1 < len(heat_map[0]):
					distance_paths.append(Explore(line, col, ['R']))
					distance_paths.append(Explore(line, col, ['D', 'R']))
					distance_paths.append(Explore(line, col, ['D', 'D', 'R']))
					distance_paths.append(Explore(line, col, ['D', 'D', 'D', 'R']))
				if col - 1 >= 0:
					distance_paths.append(Explore(line, col, ['L']))
					distance_paths.append(Explore(line, col, ['D', 'L']))
					distance_paths.append(Explore(line, col, ['D', 'D', 'L']))
					distance_paths.append(Explore(line, col, ['D', 'D', 'D', 'L']))
				explored_down = True
		elif path[0] == 'R':
			if not explored_right:
				if line + 1 < len(heat_map):
					distance_paths.append(Explore(line, col, ['D']))
					distance_paths.append(Explore(line, col, ['R', 'D']))
					distance_paths.append(Explore(line, col, ['R', 'R', 'D']))
					distance_paths.append(Explore(line, col, ['R', 'R', 'R', 'D']))
				if line - 1 >= 0:
					distance_paths.append(Explore(line, col, ['U']))
					distance_paths.append(Explore(line, col, ['R', 'U']))
					distance_paths.append(Explore(line, col, ['R', 'R', 'U']))
					distance_paths.append(Explore(line, col, ['R', 'R', 'R', 'U']))
				explored_right = True
		else:
			print("very very bad, should not hit here")
	print(distance_paths)
	min_distance = math.inf
	min_distance_paths = []
	for path in distance_paths:
		if path[0] < min_distance:
			min_distance = path[0]
			min_distance_paths = [path[1]]
		elif path[0] == min_distance:
			min_distance_paths.append(path[1])
	# real_path = min(distance_paths, key=lambda x: x[0])
	distances[line][col] = min_distance
	directions[line][col] = min_distance_paths

def Magic(line, col):
	print(f"Magic {line}, {col}")
	dist_down = math.inf
	if line + 1 < len(heat_map):
		dist_down = heat_map[line][col] + distances[line + 1][col]
	dist_right = math.inf
	if col + 1 < len(heat_map):
		dist_right = heat_map[line][col] + distances[line][col + 1]
	distances[line][col] = min(dist_down, dist_right)
	if dist_down < dist_right:
		directions[line][col].append(['D'])
	elif dist_right < dist_down:
		directions[line][col].append(['R'])
	else:
		directions[line][col].append(['D'])
		directions[line][col].append(['R'])
	if not IsTopPathValid(line, col):
		BlackMagic(line, col)

# for level in range(len(heat_map) - 2, -1, -1):
# 	for i in range(len(heat_map) - 1, level, -1):
# 		Magic(level, i)
# 		Magic(i, level)
# 	Magic(level, level)
	# if level == 5:
	# 	break

# debug print
# for i in distances:
# 	out = ''
# 	for j in i:
# 		out += f'{j:>4}'
# 	print(out)

# for i, val in enumerate(directions):
# 	print(i, val)

# Attepmt no.3


def CalculateDistance(position, path):
	distance = heat_map[position[0]][position[1]]
	for i in path:
		position = Move(position, [i])
		distance += heat_map[position[0]][position[1]]
	return distance

def GetShortestPath(start, last_direction):
	if start[0] == len(heat_map) - 1 and start[1] == len(heat_map[0]) -1:
		return heat_map[-1][-1]
	possible_paths = [['R'], ['R', 'R'], ['R', 'R', 'R'], ['D'], ['D', 'D'], ['D', 'D', 'D'], ['L'], ['L', 'L'], ['L', 'L', 'L'], ['U'], ['U', 'U'], ['U', 'U', 'U']]
	returned_paths = []
	for i in possible_paths:
		if i[0] == last_direction:
			continue
		next_pos = Move(start, i)
		if not IsValidPosition(next_pos):
			continue
		current_distance = CalculateDistance(start, i[:-1])
		short_path = GetShortestPath(next_pos, i[0])
		returned_paths.append(short_path[0] + current_distance, i + short_path[1])
		# nebesugalvoju kaip deramai nutraukti rekursija


# heat_map = [[int(j) for j in i] for i in input_lines]
# distances_cache = [[[] for j in i] for i in input_lines]
# shortest_path = GetShortestPath((0, 0), 'S')

# print('Silver answer: ' + str(distance[-1][-1]))

# Gold star

# print('Gold answer: ' + str(max(counts)))
