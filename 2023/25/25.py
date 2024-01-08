import random

input_lines = []
with open('input.txt', 'r') as input_file:
	for line in input_file:
		input_lines.append(line.removesuffix('\n'))

# Parse input
def AddConnection(graph, edges, start, end):
	if start not in graph:
		graph[start] = {'connections': [], 'weight': 1}
	if end not in graph:
		graph[end] = {'connections': [], 'weight': 1}
	graph[start]['connections'].append(end)
	graph[end]['connections'].append(start)
	edges.append((start, end))

graph = {}
edges = []
for line in input_lines:
	nodes = line.split(' ')
	start_node = nodes[0][:-1]
	end_nodes = nodes[1:]
	for node in end_nodes:
		AddConnection(graph, edges, start_node, node)

# Silver star
# TODO: Frequency counting should be moved to utilities
def AddFrequency(counts, val):
	if val not in counts:
		counts[val] = 0
	counts[val] += 1

# for key in graph:
# 	AddFrequency(counts, len(graph[key]))

def PrintGraph(graph):
	for i in graph:
		print(f"{i}: {graph[i]}")

def GetRandomEdge(edges):
	edge = random.choice(edges)
	edges.remove(edge)
	return edge

def RemoveEdge(edges, edge):
	for i in edges:
		if edge[0] == i[0] and edge[1] == i[1] or edge[0] == i[1] and edge[1] == i[0]:
			edges.remove(i)
			return

def MergeGraph(graph, edges, edge):
	for node in graph[edge[1]]['connections']:
		if node == edge[0]:  # same as merge end
			graph[node]['connections'].remove(edge[1])
			RemoveEdge(edges, edge)
		else:
			# Move edge to edge[0] from edge[1]
			graph[node]['connections'].remove(edge[1])
			RemoveEdge(edges, (node, edge[1]))
			AddConnection(graph, edges, edge[0], node)
	graph[edge[0]]['weight'] += graph[edge[1]]['weight']
	graph.pop(edge[1])

# https://en.wikipedia.org/wiki/Karger%27s_algorithm
def Karger(graph, edges):
	while len(graph) > 2:
		edge = GetRandomEdge(edges)
		MergeGraph(graph, edges, edge)
	return graph, edges

# debug test
# test_graph = {}
# test_edges = []
# AddConnection(test_graph, test_edges, 'A', 'C')
# AddConnection(test_graph, test_edges, 'A', 'D')
# AddConnection(test_graph, test_edges, 'A', 'B')
# AddConnection(test_graph, test_edges, 'A', 'B')
# AddConnection(test_graph, test_edges, 'D', 'B')
# AddConnection(test_graph, test_edges, 'E', 'B')
# PrintGraph(test_graph)
# print(test_edges)
# print("after merge A-B")
# MergeGraph(test_graph, test_edges, ('A', 'B'))
# PrintGraph(test_graph)
# print(test_edges)

# run the simulation a 100 times
counts = {}
edge_counts = {}
for i in range(1000):
	if i % 10 == 0:
		print(i)
	graph_copy = {i: {'connections': graph[i]['connections'].copy(), 'weight': graph[i]['weight']} for i in graph}
	edges_copy = edges.copy()
	reduced_graph, reduced_edges = Karger(graph_copy, edges_copy)
	AddFrequency(edge_counts, len(reduced_edges))
	if len(reduced_edges) == 3:
		k = list(reduced_graph.keys())
		AddFrequency(counts, reduced_graph[k[0]]['weight'] * reduced_graph[k[1]]['weight'])

print("edge count frequencies", edge_counts)
print("possible answers", counts)

most_frequent_answer = 0
most_frequent_index = -1
for i in counts:
	if counts[i] > most_frequent_answer:
		most_frequent_answer = counts[i]
		most_frequent_index = i

# edge count frequencies {4: 874, 5: 69, 6: 35, 3: 9, 7: 10, 10: 2, 8: 1}
# possible answers {600369: 9}

print('Silver answer: ' + str(most_frequent_index))

# Gold star
# print('Gold answer: ' + str(result['px'] + result['py'] + result['pz']))
