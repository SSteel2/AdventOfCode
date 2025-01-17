import Util.input
import Util.Graph

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(input_lines):
	graph = Util.Graph.Graph()
	for line in input_lines:
		split_line = line.split(' ')
		left = graph.AddNode(split_line[0])
		right = graph.AddNode(split_line[2])
		graph.AddEdge(left, right, int(split_line[4]))
	return graph

def _traverse(graph, current_path, curent_distance, selection_function):
	'''Traveling salesman problem (TSP)'''
	best_distance = None
	for node_name in graph.nodes:
		if node_name in current_path:
			continue
		distance = _traverse(graph, current_path + [node_name], curent_distance + graph.nodes[current_path[-1]].edges[node_name].weight, selection_function)
		if best_distance == None:
			best_distance = distance
		else:
			best_distance = selection_function(best_distance, distance)
	if best_distance == None:  # no more nodes
		return curent_distance
	return best_distance

def _solve(input_lines, selection_function):
	graph = _parse(input_lines)
	best_distance = None
	for node_name in graph.nodes:
		distance = _traverse(graph, [node_name], 0, selection_function)
		if best_distance == None:
			best_distance = distance
		else:
			best_distance = selection_function(best_distance, distance)
	return best_distance

def silver(input_lines):
	return _solve(input_lines, min)

def gold(input_lines):
	return _solve(input_lines, max)
