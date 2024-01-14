import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(input_lines):
	blocks = []
	current_id = 0
	for i in input_lines:
		start, end = i.split('~')
		sx, sy, sz = start.split(',')
		ex, ey, ez = end.split(',')
		blocks.append({'id': current_id, 'start': {'x': int(sx), 'y': int(sy), 'z': int(sz)}, 'end': {'x': int(ex), 'y': int(ey), 'z': int(ez)}})
		current_id += 1
	return sorted(blocks, key=lambda x: x['start']['z'])

def _getMax(blocks):
	max_x = max(blocks, key=lambda x: x['end']['x'])['end']['x'] + 1
	max_y = max(blocks, key=lambda x: x['end']['y'])['end']['y'] + 1
	return max_x, max_y

def _findPlacementFloor(block, tower):
	highest_occupied = -1
	for x in range(block['start']['x'], block['end']['x'] + 1):
		for y in range(block['start']['y'], block['end']['y'] + 1):
			for z in range(len(tower) - 1, -1, -1):
				if tower[z][x][y] != -1:
					if highest_occupied < z:
						highest_occupied = z
					break
	return highest_occupied + 1

def _growTower(block, placement_level, max_x, max_y, tower):
	max_needed_z = placement_level + block['end']['z'] - block['start']['z']
	levels_needed = max_needed_z - len(tower) + 1
	for i in range(levels_needed):
		tower.append([[-1 for _ in range(max_y)] for _ in range(max_x)])

def _placeBlock(block, new_z, tower):
	for x in range(block['start']['x'], block['end']['x'] + 1):
		for y in range(block['start']['y'], block['end']['y'] + 1):
			for z in range(0, block['end']['z'] - block['start']['z'] + 1):
				tower[new_z + z][x][y] = block['id']

def _findSupports(block, new_z, tower):
	if new_z == 0:
		return []  # ground support
	supports = []
	for x in range(block['start']['x'], block['end']['x'] + 1):
		for y in range(block['start']['y'], block['end']['y'] + 1):
			below_value = tower[new_z - 1][x][y]
			if below_value != -1 and below_value not in supports:
				supports.append(below_value)
	return supports

def _calculateSupports(blocks):
	max_x, max_y = _getMax(blocks)
	tower = [[[-1 for _ in range(max_y)] for _ in range(max_x)]]  # z (floor), x, y
	for block in blocks:
		new_z = _findPlacementFloor(block, tower)
		block['supports'] = _findSupports(block, new_z, tower)
		_growTower(block, new_z, max_x, max_y, tower)
		_placeBlock(block, new_z, tower)

def _getLoads(blocks):
	loads = [[] for _ in range(len(blocks))]
	for block in blocks:
		for support in block['supports']:
			loads[support].append(block['id'])
	return loads

def _getSupports(blocks):
	supports = [[] for _ in range(len(blocks))]
	for block in blocks:
		supports[block['id']] = block['supports'].copy()
	return supports

def _getBlock(block_id, blocks):
	for block in blocks:
		if block['id'] == block_id:
			return block

def silver(input_lines):
	blocks = _parse(input_lines)
	_calculateSupports(blocks)
	loads = _getLoads(blocks)

	total_removables = 0
	for block in blocks:
		disintegratable = True
		for load in loads[block['id']]:
			if len(_getBlock(load, blocks)['supports']) < 2:
				disintegratable = False
				break
		if disintegratable:
			total_removables += 1
	return total_removables

def _disintegrateBlock(block, loads, supports):
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

def gold(input_lines):
	blocks = _parse(input_lines)
	_calculateSupports(blocks)
	loads = _getLoads(blocks)
	supports = _getSupports(blocks)
	
	count = 0
	for block in blocks:
		count += _disintegrateBlock(block, loads, supports)
	return count
