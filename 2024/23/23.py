import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parseLine(line):
	return tuple(line.split('-'))

class Graph:
	def __init__(self):
		self.nodes = {}

	def AddNode(self, node_name):
		if node_name in self.nodes:
			return self.nodes[node_name]
		else:
			node = Node(node_name)
			self.nodes[node_name] = node
			return node

	def GetPartiesSilver(self):
		parties = set()
		for node_name in self.nodes:
			if node_name[0] != 't':
				continue
			node_parties = self.nodes[node_name].GetParties()
			for i in node_parties:
				parties.add(i)
		return parties

	def GetPartiesGold(self):
		parties = set()
		for node_name in self.nodes:
			node_parties = self.nodes[node_name].GetParties()
			for i in node_parties:
				parties.add(i)
		return parties

	def GetMaxQlique(self):
		parties = self.GetPartiesGold()  # {(n1, n2, n3), ...}
		current_size = 3
		while True:
			new_parties = set()
			for party in parties:
				extended_parties = self.nodes[party[0]].GetExtendedParties(party[1:])
				for i in extended_parties:
					new_parties.add(i)
			if len(new_parties) > 0:
				parties = new_parties
				current_size += 1
			else:
				break
		return parties

class Node:
	def __init__(self, name):
		self.name = name
		self.connections = {}

	def AddConnection(self, other):
		if other.name not in self.connections:
			self.connections[other.name] = other
			other.AddConnection(self)

	def GetParties(self):
		parties = set()
		for other_name in self.connections:
			common_nodes = set(self.connections.values()).intersection(set(self.connections[other_name].connections.values()))
			for i in common_nodes:
				parties.add(tuple(sorted([self.name, other_name, i.name])))
		return parties

	def GetExtendedParties(self, neighbour_names):
		common_neighbours = set(self.connections.keys())
		for i in neighbour_names:
			common_neighbours = common_neighbours.intersection(set(self.connections[i].connections.keys()))
		result = set()
		for i in common_neighbours:
			result.add(tuple(sorted([self.name, *neighbour_names, i])))
		return result

def _construct_graph(input_lines):
	connections = Util.input.ParseInputLines(input_lines, _parseLine)
	graph = Graph()
	for connection in connections:
		nodeA = graph.AddNode(connection[0])
		nodeB = graph.AddNode(connection[1])
		nodeA.AddConnection(nodeB)
	return graph

def silver(input_lines):
	graph = _construct_graph(input_lines)
	return len(graph.GetPartiesSilver())

def gold(input_lines):
	graph = _construct_graph(input_lines)
	max_cliques = graph.GetMaxQlique()
	return ','.join([str(i) for i in sorted(max_cliques.pop())])
