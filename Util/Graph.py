class Graph:
	def __init__(self):
		self.nodes = {}  # name/id: Node
		self.edges = []

	def AddNode(self, name):
		if name not in self.nodes:
			self.nodes[name] = Node(name)
		return self.nodes[name]

	def AddEdge(self, left, right, weight):
		edge = Edge(left, right, weight)
		self.edges.append(edge)
		left.AddEdge(edge)
		right.AddEdge(edge)

class Node:
	def __init__(self, name):
		self.name = name
		self.edges = {}

	def AddEdge(self, edge):
		other_node = edge.left if edge.right.name == self.name else edge.right
		self.edges[other_node.name] = edge

class Edge:
	def __init__(self, left, right, weight):
		self.left = left
		self.right = right
		self.weight = weight

	def Other(self, node):
		if node == self.left:
			return self.right
		elif node == self.right:
			return self.left
		else:
			return None  # shouldn't happen
