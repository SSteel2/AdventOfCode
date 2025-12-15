import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(input_lines):
	shapes = []
	trees = []
	is_parsing_shapes = True
	is_shape_first_line = True
	current_shape = []
	for line in input_lines:
		if is_parsing_shapes:
			if is_shape_first_line:
				if line[1] != ':':
					is_parsing_shapes = False
				is_shape_first_line = False
			elif line == '':
				shapes.append(current_shape)
				current_shape = []
				is_shape_first_line = True
			else:
				current_shape.append(line)
		else:
			parts = line.split(' ')
			size = tuple(int(i) for i in parts[0].strip(':').split('x'))
			trees.append({'size': size, 'presents': [int(i) for i in parts[1:]]})
	return shapes, trees

def silver(input_lines):
	shapes, trees = _parse(input_lines)
	areas = []
	for shape in shapes:
		areas.append(sum(i.count('#') for i in shape))
	fitting_trees = 0
	for tree in trees:
		count_3x3 = (tree['size'][0] // 3) * (tree['size'][1] // 3)
		count_presents = sum(tree['presents'])
		if count_3x3 >= count_presents:
			fitting_trees += 1
			continue
		tree_area = tree['size'][0] * tree['size'][1]
		present_area = sum([i[0] * i[1] for i in zip(tree['presents'], areas)])
		if present_area > tree_area:
			# presents can't fit
			continue
		print("Inconclusive found !!!")  # I think this is a trick task and this doesn't happen
	return fitting_trees


def gold(input_lines):
	pass
