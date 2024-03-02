import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(line):
	return int(line)

def _parseGold(line):
	return int(line) * 811589153

class HighwayNode:
	def __init__(self, node):
		self.node = node
		self.next_node = None
		self.prev_node = None
		self.jump_size = None

	def __str__(self):
		return f'HN {self.node.value}'

	def __repr__(self):
		return self.__str__()

	def pushForward(self, end_node):
		current = self.node
		current.highway_node = None
		current.next_node.highway_node = self
		self.node = current.next_node
		if self != end_node:
			self.next_node.pushForward(end_node)

class Node:
	def __init__(self, index, value):
		self.index = index
		self.value = value
		self.next_node = None
		self.prev_node = None
		self.highway_node = None

	def __str__(self):
		return f'{self.value}'

	def __repr__(self):
		return self.__str__()

	def get_node(self, move):
		current = self
		moved = 0
		start_highway = None
		last_highway = None
		while moved < move:
			if current.highway_node != None:
				last_highway = current.highway_node
				if start_highway == None:
					if moved == 0:
						start_highway = current.highway_node
					else:
						start_highway = current.highway_node.prev_node
				if move - moved >= last_highway.jump_size:
					moved += last_highway.jump_size
					current = last_highway.next_node.node
				else:
					current = current.next_node
					moved += 1
			else:
				current = current.next_node
				moved += 1
		if current.highway_node != None:
			last_highway = current.highway_node
			if start_highway == None:
				start_highway = current.highway_node.prev_node
		return current, start_highway, last_highway

class LinkedList:
	def __init__(self):
		self.nodes = {}
		self.length = 0
		self.start_index = -1

	def __str__(self):
		if self.length == 0:
			return []
		current = self.nodes[0]
		values = []
		for i in range(self.length):
			values.append(current.value)
			current = current.next_node
		return str(values)

	def __repr__(self):
		return self.__str__()

	def __len__(self):
		return self.length

	def add(self, value):
		self.nodes[self.length] = Node(self.length, value)
		if value == 0:
			self.start_index = self.length
		self.nodes[self.length].next_node = self.nodes[0]
		self.nodes[self.length].prev_node = self.nodes[-2 % (self.length + 1)]
		self.nodes[self.length].next_node.prev_node = self.nodes[self.length]
		self.nodes[self.length].prev_node.next_node = self.nodes[self.length]
		self.length += 1

	def createHighwayNodes(self, jump_size):
		first_highway = self.nodes[0].highway_node = HighwayNode(self.nodes[0])
		last_highway = first_highway
		current = self.nodes[0].next_node
		traveled = 0
		while first_highway != current:
			traveled += 1
			if traveled % jump_size == 0:
				current_highway = current.highway_node = HighwayNode(current)
				last_highway.next_node = current_highway
				last_highway.jump_size = jump_size
				current_highway.prev_node = last_highway
				last_highway = current_highway
				if self.length - traveled < 2 * jump_size:
					break
			current = current.next_node
		last_highway.next_node = first_highway
		last_highway.jump_size = self.length - traveled
		first_highway.prev_node = last_highway		

	def reorder(self):
		for i in range(self.length):
			node = self.nodes[i]
			move = node.value
			if move % (self.length - 1) == 0:
				continue
			old_next = node.next_node
			old_prev = node.prev_node
			new_prev, old_highway, new_highway = node.get_node(move % (self.length - 1))
			old_prev.next_node = old_next
			old_next.prev_node = old_prev
			node.prev_node = new_prev
			node.next_node = new_prev.next_node
			new_prev.next_node.prev_node = node
			new_prev.next_node = node
			if node.highway_node != None:
				old_next.highway_node = node.highway_node
				node.highway_node = None
				old_next.highway_node.node = old_next
			if old_highway != None and new_highway != None and old_highway != new_highway:
				old_highway.next_node.pushForward(new_highway)

	def sum_criticals(self):
		critical_indexes = [1000, 2000, 3000]
		total = 0
		for i in critical_indexes:
			node, _, _ = self.nodes[self.start_index].get_node(i % self.length)
			total += node.value
		return total

def _solve(parsed, iterations):
	linked_list = LinkedList()
	for i in parsed:
		linked_list.add(i)
	linked_list.createHighwayNodes(120)
	for i in range(iterations):
		linked_list.reorder()
	return linked_list.sum_criticals()

def silver(input_lines):
	parsed = Util.input.ParseInputLines(input_lines, _parse)
	return _solve(parsed, 1)

def gold(input_lines):
	parsed = Util.input.ParseInputLines(input_lines, _parseGold)
	return _solve(parsed, 10)
