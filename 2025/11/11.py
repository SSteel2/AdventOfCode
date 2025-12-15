import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(line):
	parts = line.split(' ')
	return {'start': parts[0][:-1], 'end': parts[1:]}

def silver(input_lines):
	nodes_list = Util.input.ParseInputLines(input_lines, _parse)
	nodes = {}
	for i in nodes_list:
		nodes[i['start']] = {'destinations': i['end'], 'pathways': None}
	# handle the last node in list if all dependencies are calculated, if not, add dependencies to list
	queue = ['you']
	while len(queue) > 0:
		is_calculated = True
		possible_pathways = 0
		for destination in nodes[queue[-1]]['destinations']:
			if destination == 'out':
				possible_pathways += 1
			elif nodes[destination]['pathways'] != None:
				possible_pathways += nodes[destination]['pathways']
			else:
				is_calculated = False
				queue.append(destination)
		if is_calculated:
			nodes[queue.pop()]['pathways'] = possible_pathways
	return nodes['you']['pathways']
	
def gold(input_lines):
	nodes_list = Util.input.ParseInputLines(input_lines, _parse)
	nodes = {}
	for i in nodes_list:
		nodes[i['start']] = {'destinations': i['end'], 'pathways': None, 'pathways_dac': None, 'pathways_fft': None, 'pathways_both': None}
	# handle the last node in list if all dependencies are calculated, if not, add dependencies to list
	queue = ['svr']
	while len(queue) > 0:
		current_node = queue[-1]
		is_calculated = True
		pathways_none = 0
		pathways_dac = 0
		pathways_fft = 0
		pathways_both = 0
		for destination in nodes[current_node]['destinations']:
			if destination == 'out':
				pathways_none += 1
			elif nodes[destination]['pathways'] != None:
				pathways_none += nodes[destination]['pathways']
				pathways_dac += nodes[destination]['pathways_dac']
				pathways_fft += nodes[destination]['pathways_fft']
				pathways_both += nodes[destination]['pathways_both']
			else:
				is_calculated = False
				queue.append(destination)
		if is_calculated:
			if current_node == 'dac':
				nodes[current_node]['pathways'] = 0
				nodes[current_node]['pathways_dac'] = pathways_dac + pathways_none
				nodes[current_node]['pathways_fft'] = 0
				nodes[current_node]['pathways_both'] = pathways_both + pathways_fft
			elif current_node == 'fft':
				nodes[current_node]['pathways'] = 0
				nodes[current_node]['pathways_dac'] = 0
				nodes[current_node]['pathways_fft'] = pathways_fft + pathways_none
				nodes[current_node]['pathways_both'] = pathways_both + pathways_dac
			else:
				nodes[current_node]['pathways'] = pathways_none
				nodes[current_node]['pathways_dac'] = pathways_dac
				nodes[current_node]['pathways_fft'] = pathways_fft
				nodes[current_node]['pathways_both'] = pathways_both
			queue.pop()
	return nodes['svr']['pathways_both']
