import random
import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _addConnection(graph, edges, start, end):
	if start not in graph:
		graph[start] = {'connections': [], 'weight': 1}
	if end not in graph:
		graph[end] = {'connections': [], 'weight': 1}
	graph[start]['connections'].append(end)
	graph[end]['connections'].append(start)
	edges.append((start, end))

def _parse(input_lines):
	graph = {}
	edges = []
	for line in input_lines:
		nodes = line.split(' ')
		start_node = nodes[0][:-1]
		end_nodes = nodes[1:]
		for node in end_nodes:
			_addConnection(graph, edges, start_node, node)
	return graph, edges

def _getRandomEdge(edges):
	edge = random.choice(edges)
	edges.remove(edge)
	return edge

def _removeEdge(edges, edge):
	for i in edges:
		if edge[0] == i[0] and edge[1] == i[1] or edge[0] == i[1] and edge[1] == i[0]:
			edges.remove(i)
			return

def _mergeGraph(graph, edges, edge):
	for node in graph[edge[1]]['connections']:
		if node == edge[0]:  # same as merge end
			graph[node]['connections'].remove(edge[1])
			_removeEdge(edges, edge)
		else:
			# Move edge to edge[0] from edge[1]
			graph[node]['connections'].remove(edge[1])
			_removeEdge(edges, (node, edge[1]))
			_addConnection(graph, edges, edge[0], node)
	graph[edge[0]]['weight'] += graph[edge[1]]['weight']
	graph.pop(edge[1])

# https://en.wikipedia.org/wiki/Karger%27s_algorithm
def _karger(graph, edges, stop_threshold):
	graph_copy = {i: {'connections': graph[i]['connections'].copy(), 'weight': graph[i]['weight']} for i in graph}
	edges_copy = edges.copy()
	while len(graph_copy) > stop_threshold:
		edge = _getRandomEdge(edges_copy)
		_mergeGraph(graph_copy, edges_copy, edge)
	return graph_copy, edges_copy

def _stackedKarger(graph_list, edges_list, run_count, stop_threshold):
	new_graph_list = []
	new_edges_list = []
	for j in range(len(graph_list)):
		graph = graph_list[j]
		edges = edges_list[j]
		for i in range(run_count):
			reduced_graph, reduced_edges = _karger(graph, edges, stop_threshold)
			new_graph_list.append(reduced_graph)
			new_edges_list.append(reduced_edges)
	return new_graph_list, new_edges_list

def silver(input_lines):
	graph, edges = _parse(input_lines)
	# This config gets the answer ~96% of the time
	reduced_graph_list, reduced_edges_list = _stackedKarger([graph], [edges], 5, 800)
	reduced_graph_list, reduced_edges_list = _stackedKarger(reduced_graph_list, reduced_edges_list, 5, 300)
	reduced_graph_list, reduced_edges_list = _stackedKarger(reduced_graph_list, reduced_edges_list, 5, 100)
	reduced_graph_list, reduced_edges_list = _stackedKarger(reduced_graph_list, reduced_edges_list, 20, 2)
	for i in range(len(reduced_graph_list)):
		if len(reduced_edges_list[i]) == 3:
			# Utilizing the fact, that there is one answer possible
			k = list(reduced_graph_list[i].keys())
			return reduced_graph_list[i][k[0]]['weight'] * reduced_graph_list[i][k[1]]['weight']

	# Failed to find an answer, try again
	return -1

def gold(input_lines):
	pass # no gold task for day 25
