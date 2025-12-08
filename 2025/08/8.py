import Util.input
import Util.Graph
import math
import pprint

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(line):
	return tuple(int(i) for i in line.split(','))

def _visit_cluster(node, visited):
	cluster_size = 0
	queue = [node]
	while len(queue) > 0:
		current = queue.pop()
		if current.name in visited:
			continue
		visited.add(current.name)
		cluster_size += 1
		for node_name in current.edges:
			queue.append(current.edges[node_name].Other(current))
	return cluster_size

def silver(input_lines):
	positions = Util.input.ParseInputLines(input_lines, _parse)
	distance_table = []
	for position in positions:
		distances = []
		for target in positions:
			distance = 0
			for i in range(3):
				distance += (position[i] - target[i]) ** 2
			distances.append(distance)
		distance_table.append(distances)
	for i in range(len(distance_table)):
		distance_table[i][i] = math.inf
	
	min_distances = []
	for distances in distance_table:
		min_distance = math.inf
		min_index = -1
		for index, distance in enumerate(distances):
			if distance < min_distance:
				min_distance = distance
				min_index = index
		min_distances.append((min_distance, min_index))
	
	graph = Util.Graph.Graph()
	for i in range(len(distance_table)):
		graph.AddNode(i)

	# Make 1000 connections
	for _ in range(1000):
		min_distance = math.inf
		min_distance_index = (-1, -1)
		for index, min_distance_info in enumerate(min_distances):
			if min_distance_info[0] < min_distance:
				min_distance = min_distance_info[0]
				min_distance_index = (index, min_distance_info[1])
		graph.AddEdge(graph.nodes[min_distance_index[0]], graph.nodes[min_distance_index[1]], min_distance)
		distance_table[min_distance_index[0]][min_distance_index[1]] = math.inf
		distance_table[min_distance_index[1]][min_distance_index[0]] = math.inf

		# Calculate new min distances (copy pasted, because me very lazy) | TODO: refactor later this eyesore
		min_distance = math.inf
		min_index = -1
		for index, distance in enumerate(distance_table[min_distance_index[0]]):
			if distance < min_distance:
				min_distance = distance
				min_index = index
		min_distances[min_distance_index[0]] = (min_distance, min_index)

		min_distance = math.inf
		min_index = -1
		for index, distance in enumerate(distance_table[min_distance_index[1]]):
			if distance < min_distance:
				min_distance = distance
				min_index = index
		min_distances[min_distance_index[1]] = (min_distance, min_index)

	# Go through graph, collect clusters
	visited = set()
	max_clusters = [0, 0, 0]
	for i in range(len(distance_table)):
		if i in visited:
			continue
		cluster_size = _visit_cluster(graph.nodes[i], visited)
		if cluster_size > max_clusters[0]:
			max_clusters[2] = max_clusters[1]
			max_clusters[1] = max_clusters[0]
			max_clusters[0] = cluster_size
		elif cluster_size > max_clusters[1]:
			max_clusters[2] = max_clusters[1]
			max_clusters[1] = cluster_size
		elif cluster_size > max_clusters[2]:
			max_clusters[2] = cluster_size

	return max_clusters[0] * max_clusters[1] * max_clusters[2]


def gold(input_lines):
	positions = Util.input.ParseInputLines(input_lines, _parse)
	distance_table = []
	for position in positions:
		distances = []
		for target in positions:
			distance = 0
			for i in range(3):
				distance += (position[i] - target[i]) ** 2
			distances.append(distance)
		distance_table.append(distances)
	for i in range(len(distance_table)):
		distance_table[i][i] = math.inf
	
	min_distances = []
	for distances in distance_table:
		min_distance = math.inf
		min_index = -1
		for index, distance in enumerate(distances):
			if distance < min_distance:
				min_distance = distance
				min_index = index
		min_distances.append((min_distance, min_index))

	# Furthest distance for a node will be the last edge
	max_distance = -1
	max_distance_index = (-1, -1)
	for index, min_distance_info in enumerate(min_distances):
		if min_distance_info[0] > max_distance:
			max_distance = min_distance_info[0]
			max_distance_index = (index, min_distance_info[1])
	return positions[max_distance_index[0]][0] * positions[max_distance_index[1]][0]
