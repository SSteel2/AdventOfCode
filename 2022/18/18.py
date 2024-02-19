import Util.input
from collections import deque

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(line):
	return [int(i) for i in line.split(',')]

def _prevBoundaries(volume, x, y, z):
	prev_boundaries = 0
	if x > 0 and volume[x - 1][y][z] != 0:
		prev_boundaries += 1
	if y > 0 and volume[x][y - 1][z] != 0:
		prev_boundaries += 1
	if z > 0 and volume[x][y][z - 1] != 0:
		prev_boundaries += 1
	return prev_boundaries

def _getMaxExtent(lines):
	max_extent = [0, 0, 0]
	for i in lines:
		for j in range(3):
			if i[j] > max_extent[j]:
				max_extent[j] = i[j]
	return max_extent

def _calculateSurfaceArea(volume, lines):
	# surface = 6 * len(lines)
	surface = 0
	for i in range(len(volume)):
		for j in range(len(volume[0])):
			for k in range(len(volume[0][0])):
				if volume[i][j][k] != 0:
					surface += 6 - _prevBoundaries(volume, i, j, k) * 2
	return surface

def silver(input_lines):
	lines = Util.input.ParseInputLines(input_lines, _parse)
	max_extent = _getMaxExtent(lines)
	volume = [[[0 for _ in range(max_extent[2] + 1)] for _ in range(max_extent[1] + 1)] for _ in range(max_extent[0] + 1)]
	for i in lines:
		volume[i[0]][i[1]][i[2]] = 1
	return _calculateSurfaceArea(volume, lines)

def _markOutside(volume, x, y, z):
	queue = deque()
	queue.append((x, y, z))
	while len(queue) > 0:
		current = queue.popleft()
		if current[0] < 0 or current[0] >= len(volume) or current[1] < 0 or current[1] >= len(volume[0]) or current[2] < 0 or current[2] >= len(volume[0][0]):
			continue
		if volume[current[0]][current[1]][current[2]] != 2:
			continue
		volume[current[0]][current[1]][current[2]] = 0
		queue.append((current[0] + 1, current[1], current[2]))
		queue.append((current[0] - 1, current[1], current[2]))
		queue.append((current[0], current[1] + 1, current[2]))
		queue.append((current[0], current[1] - 1, current[2]))
		queue.append((current[0], current[1], current[2] + 1))
		queue.append((current[0], current[1], current[2] - 1))

def gold(input_lines):
	lines = Util.input.ParseInputLines(input_lines, _parse)
	max_extent = _getMaxExtent(lines)
	volume = [[[2 for _ in range(max_extent[2] + 2)] for _ in range(max_extent[1] + 2)] for _ in range(max_extent[0] + 2)]
	for i in lines:
		volume[i[0]][i[1]][i[2]] = 1
	_markOutside(volume, 0, 0, 0)
	return _calculateSurfaceArea(volume, lines)
