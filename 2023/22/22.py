input_lines = []
with open('input.txt', 'r') as input_file:
	for line in input_file:
		input_lines.append(line.removesuffix('\n'))

# Parse input
blocks = []
current_id = 0
for i in input_lines:
	start, end = i.split('~')
	sx, sy, sz = start.split(',')
	ex, ey, ez = end.split(',')
	blocks.append({'id': current_id, 'start': {'x': int(sx), 'y': int(sy), 'z': int(sz)}, 'end': {'x': int(ex), 'y': int(ey), 'z': int(ez)}})
	current_id += 1

max_x = max(blocks, key=lambda x: x['end']['x'])['end']['x'] + 1
max_y = max(blocks, key=lambda x: x['end']['y'])['end']['y'] + 1

# Silver star

def FindPlacementFloor(block):
	highest_occupied = -1
	for x in range(block['start']['x'], block['end']['x'] + 1):
		for y in range(block['start']['y'], block['end']['y'] + 1):
			for z in range(len(tower) - 1, -1, -1):
				if tower[z][x][y] != -1:
					if highest_occupied < z:
						highest_occupied = z
					break
	return highest_occupied + 1

def GrowTower(block, placement_level):
	max_needed_z = placement_level + block['end']['z'] - block['start']['z']
	levels_needed = max_needed_z - len(tower) + 1
	for i in range(levels_needed):
		tower.append([[-1 for _ in range(max_y)] for _ in range(max_x)])

def PlaceBlock(block, new_z):
	for x in range(block['start']['x'], block['end']['x'] + 1):
		for y in range(block['start']['y'], block['end']['y'] + 1):
			for z in range(0, block['end']['z'] - block['start']['z'] + 1):
				tower[new_z + z][x][y] = block['id']

def FindSupports(block, new_z):
	if new_z == 0:
		return []  # ground support
	supports = []
	for x in range(block['start']['x'], block['end']['x'] + 1):
		for y in range(block['start']['y'], block['end']['y'] + 1):
			below_value = tower[new_z - 1][x][y]
			if below_value != -1 and below_value not in supports:
				supports.append(below_value)
	return supports

def GetBlock(block_id):
	for block in blocks:
		if block['id'] == block_id:
			return block

sorted_blocks = sorted(blocks, key=lambda x: x['start']['z'])

tower = [[[-1 for _ in range(max_y)] for _ in range(max_x)]]  # z (floor), x, y

for block in sorted_blocks:
	new_z = FindPlacementFloor(block)
	block['supports'] = FindSupports(block, new_z)
	GrowTower(block, new_z)
	PlaceBlock(block, new_z)

loads = [[] for _ in range(len(blocks))]
for block in sorted_blocks:
	for support in block['supports']:
		loads[support].append(block['id'])

total_removables = 0
for block in sorted_blocks:
	disintegratable = True
	for load in loads[block['id']]:
		if len(GetBlock(load)['supports']) < 2:
			disintegratable = False
			break
	if disintegratable:
		total_removables += 1

# debug start
# print(loads)
# for i in sorted_blocks:
# 	print(i)

# for i, level in enumerate(tower):
# 	print(f"-------------- level {i} ----------------")
# 	for j in level:
# 		print(j)
# debug end

print('Silver answer: ' + str(total_removables))

# Gold star
supports = [[] for _ in range(len(blocks))]
for block in sorted_blocks:
	supports[block['id']] = block['supports'].copy()

# print(loads)
# print(supports)

def DisintegrateBlock(block):
	fallen = 0
	local_loads = [[j for j in i] for i in loads]
	local_supports = [[j for j in i] for i in supports]
	queue_to_fall = [block['id']]
	while len(queue_to_fall) > 0:
		falling = queue_to_fall.pop()
		fallen += 1
		for index, local_support_group in enumerate(local_supports):
			if falling in local_support_group:
				local_support_group.remove(falling)
				if len(local_support_group) == 0:
					queue_to_fall.append(index)
	return fallen - 1

count = 0
for block in sorted_blocks:
	c = DisintegrateBlock(block)
	# print(c, block)
	count += c

print('Gold answer: ' + str(count))
