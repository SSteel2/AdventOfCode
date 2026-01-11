import Util.input
import Util.Graph
import math

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

def _construct_distance_table(positions):
	distance_table = [[math.inf] * len(positions) for _ in range(len(positions))]
	for i in range(len(positions)):
		for j in range(i + 1, len(positions)):
			distance = 0
			for x in range(3):
				distance += (positions[i][x] - positions[j][x]) ** 2
			distance_table[i][j] = distance
			distance_table[j][i] = distance
	return distance_table

def _find_nearest_nodes(distance_table):
	# min_distances is a table of (distance, index) tuples
	min_distances = [0] * len(distance_table)
	for i, distances in enumerate(distance_table):
		min_index = min(range(len(distances)), key=distances.__getitem__)
		min_distance = distances[min_index]
		min_distances[i] = (min_distance, min_index)
	return min_distances

def _update_nearest_nodes(min_distances, distance_table, row):
	min_index = min(range(len(distance_table[row])), key=distance_table[row].__getitem__)
	min_distance = distance_table[row][min_index]
	min_distances[row] = (min_distance, min_index)

def _find_connection_indices(min_distances, selection_function):
	# NOTE: When comparing tuples, the standard comparer uses the first element which works in our case instead of slower: key=lambda x: min_distances[x][0]
	min_distance_info_index = selection_function(range(len(min_distances)), key=min_distances.__getitem__)
	return (min_distance_info_index, min_distances[min_distance_info_index][1])

def _calculate_cluster_sizes(graph):
	visited = set()
	max_clusters = [0, 0, 0]
	for i in range(len(graph.nodes)):
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
	return max_clusters

def silver(input_lines):
	positions = Util.input.ParseInputLines(input_lines, _parse)
	distance_table = _construct_distance_table(positions)	
	min_distances = _find_nearest_nodes(distance_table)
	
	graph = Util.Graph.Graph()
	for i in range(len(distance_table)):
		graph.AddNode(i)

	# Make 1000 connections
	for _ in range(1000):
		min_distance_edge_indices = _find_connection_indices(min_distances, min)
		min_distance = min_distances[min_distance_edge_indices[0]][0]
		graph.AddEdge(graph.nodes[min_distance_edge_indices[0]], graph.nodes[min_distance_edge_indices[1]], min_distance)
		distance_table[min_distance_edge_indices[0]][min_distance_edge_indices[1]] = math.inf
		distance_table[min_distance_edge_indices[1]][min_distance_edge_indices[0]] = math.inf
		_update_nearest_nodes(min_distances, distance_table, min_distance_edge_indices[0])
		_update_nearest_nodes(min_distances, distance_table, min_distance_edge_indices[1])

	max_clusters = _calculate_cluster_sizes(graph)
	return max_clusters[0] * max_clusters[1] * max_clusters[2]

def gold(input_lines):
	positions = Util.input.ParseInputLines(input_lines, _parse)
	distance_table = _construct_distance_table(positions)
	min_distances = _find_nearest_nodes(distance_table)
	# Furthest distance for a node will be the last edge
	max_distance_index = _find_connection_indices(min_distances, max)
	return positions[max_distance_index[0]][0] * positions[max_distance_index[1]][0]
