import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _isVisible(tree_map, line, col):
	visible = True
	for i in range(line - 1, -1, -1):
		if tree_map[i][col] >= tree_map[line][col]:
			visible = False
			break
	if visible == True:
		return True
	visible = True
	for i in range(line + 1, len(tree_map)):
		if tree_map[i][col] >= tree_map[line][col]:
			visible = False
			break
	if visible == True:
		return True
	visible = True
	for i in range(col - 1, -1, -1):
		if tree_map[line][i] >= tree_map[line][col]:
			visible = False
			break
	if visible == True:
		return True
	visible = True
	for i in range(col + 1, len(tree_map[0])):
		if tree_map[line][i] >= tree_map[line][col]:
			visible = False
			break
	if visible == True:
		return True
	return False

def _scenicScore(tree_map, line, col):
	scenic_score = 1
	viewing_distance = 0
	for i in range(line - 1, -1, -1):
		viewing_distance += 1
		if tree_map[i][col] >= tree_map[line][col]:
			break
	scenic_score *= viewing_distance
	viewing_distance = 0
	for i in range(line + 1, len(tree_map)):
		viewing_distance += 1
		if tree_map[i][col] >= tree_map[line][col]:
			break
	scenic_score *= viewing_distance
	viewing_distance = 0
	for i in range(col - 1, -1, -1):
		viewing_distance += 1
		if tree_map[line][i] >= tree_map[line][col]:
			break
	scenic_score *= viewing_distance
	viewing_distance = 0
	for i in range(col + 1, len(tree_map[0])):
		viewing_distance += 1
		if tree_map[line][i] >= tree_map[line][col]:
			break
	scenic_score *= viewing_distance
	return scenic_score

def silver(input_lines):
	count_visible = 0
	for i in range(len(input_lines)):
		for j in range(len(input_lines[i])):
			if _isVisible(input_lines, i, j):
				count_visible += 1
	return count_visible

def gold(input_lines):
	max_scenic_score = 0
	for i in range(len(input_lines)):
		for j in range(len(input_lines[i])):
			if (scenic_score := _scenicScore(input_lines, i, j)) > max_scenic_score:
				max_scenic_score = scenic_score
	return max_scenic_score
