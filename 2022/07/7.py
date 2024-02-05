import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

class TreeNode:
	def __init__(self, name, parent):
		self.name = name
		self.parent = parent
		self.nodes = []
		self.leaves = []
		self.size = None

	def addDirectory(self, name):
		self.nodes.append(TreeNode(name, self))

	def addLeaf(self, name, size):
		self.leaves.append({'name': name, 'size': int(size)})

	def getDirectory(self, name):
		for node in self.nodes:
			if node.name == name:
				return node
		return None

	def calculateSize(self):
		if self.size != None:
			return self.size
		size = 0
		for node in self.nodes:
			size += node.calculateSize()
		for leaf in self.leaves:
			size += leaf['size']
		self.size = size
		return size

def _parseCommands(input_lines):
	tree = None
	current_tree = None
	for line in input_lines:
		split_line = line.split(' ')
		if split_line[0] == '$':
			if split_line[1] == 'cd':
				if split_line[2] == '/':
					tree = TreeNode('/', None)
					current_tree = tree
				elif split_line[2] == '..':
					current_tree = current_tree.parent
				else:
					current_tree = current_tree.getDirectory(split_line[2])
		elif split_line[0] == 'dir':
			current_tree.addDirectory(split_line[1])
		else:
			current_tree.addLeaf(split_line[1], split_line[0])
	return tree

def _calculateSmallSizes(tree):
	queue = [tree]
	size = 0
	while len(queue) > 0:
		node = queue.pop()
		for child in node.nodes:
			queue.append(child)
		if node.size < 100000:
			size += node.size
	return size

def _findSmallestThresholdDirectory(tree, threshold):
	queue = [tree]
	size = 999999999
	while len(queue) > 0:
		node = queue.pop()
		for child in node.nodes:
			queue.append(child)
		if node.size > threshold and node.size < size:
			size = node.size
	return size

def silver(input_lines):
	tree = _parseCommands(input_lines)
	tree.calculateSize()
	return _calculateSmallSizes(tree)

def gold(input_lines):
	tree = _parseCommands(input_lines)
	tree.calculateSize()
	unused_space = 70000000 - tree.size
	required_space = 30000000
	missing_space = required_space - unused_space
	return _findSmallestThresholdDirectory(tree, missing_space)
