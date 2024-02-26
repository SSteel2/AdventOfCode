import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(line):
	return int(line)

def _parseGold(line):
	return int(line) * 811589153

class Node:
	def __init__(self, index, value):
		self.index = index
		self.value = value
		self.next_node = None
		self.prev_node = None

	def __str__(self):
		return f'{value}'

	def __repr__(self):
		return self.__str__()

	def get_node(self, move):
		if move == 0:
			return self
		elif move > 0:
			current = self
			for i in range(move):
				current = current.next_node
			return current
		else:
			current = self.prev_node
			for i in range(0, move, -1):
				current = current.prev_node
			return current

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

	def reorder(self):
		for i in range(self.length):
			node = self.nodes[i]
			move = node.value
			if move == 0:
				continue
			old_next = node.next_node
			old_prev = node.prev_node
			new_prev = node.get_node(move % (self.length - 1))
			old_prev.next_node = old_next
			old_next.prev_node = old_prev
			node.prev_node = new_prev
			node.next_node = new_prev.next_node
			new_prev.next_node.prev_node = node
			new_prev.next_node = node
			# print(self)

	def sum_criticals(self):
		critical_indexes = [1000, 2000, 3000]
		# critical_indexes = [i % self.length for i in critical_indexes]
		total = 0
		for i in critical_indexes:
			v = self.nodes[self.start_index].get_node(i % self.length).value
			total += v

			print(f'{i % self.length}: {v}')
			# print(total)
		return total

	def debug(self):
		current = self.nodes[0]
		for i in range(self.length):
			print(f'Node {current.index}: {current.value} (next: {current.next_node.value}, prev: {current.prev_node.value})')
			current = current.next_node

def _reorder(indexed_list):
	for i in range(len(indexed_list)):
		for j, index_value in enumerate(indexed_list):
			if index_value[0] == i:
				moves = index_value[1]
				new_index = (j + moves) % (len(indexed_list) - 1)
				list_removed = indexed_list[:j] + indexed_list[j + 1:]
				indexed_list = list_removed[:new_index] + [index_value] + list_removed[new_index:]
				break
	return indexed_list

def _findZeroIndex(indexed_list):
	for i, index_value in enumerate(indexed_list):
		if index_value[1] == 0:
			return i

def _calculateCriticalSum(indexed_list):
	zero_index = _findZeroIndex(indexed_list)
	critical_indexes = [1000, 2000, 3000]
	total = 0
	for i in critical_indexes:
		total += indexed_list[(i + zero_index) % len(indexed_list)][1]
	return total

def _failedSolution():
	parsed = Util.input.ParseInputLines(input_lines, _parse)
	linked_list = LinkedList()
	for i in parsed:
		linked_list.add(i)
	linked_list.reorder()
	print(linked_list)
	linked_list.debug()
	return linked_list.sum_criticals()

def silver(input_lines):
	parsed = Util.input.ParseInputLines(input_lines, _parse)
	indexed_list = []
	for i, number in enumerate(parsed):
		indexed_list.append((i, number))
	indexed_list = _reorder(indexed_list)
	return _calculateCriticalSum(indexed_list)

def gold(input_lines):
	parsed = Util.input.ParseInputLines(input_lines, _parseGold)
	indexed_list = []
	for i, number in enumerate(parsed):
		indexed_list.append((i, number))
	for i in range(10):
		indexed_list = _reorder(indexed_list)
	return _calculateCriticalSum(indexed_list)
