class PriorityQueue:
	def __init__(self):
		self.values = {}

	def __len__(self):
		return len(self.values)

	def append(self, priority, value):
		if priority in self.values:
			self.values[priority].append(value)
		else:
			self.values[priority] = [value]

	def pop(self):
		low_key = min(self.values)
		if len(self.values[low_key]) == 1:
			result = self.values[low_key][0]
			del self.values[low_key]
			return result
		else:
			return self.values[low_key].pop()
