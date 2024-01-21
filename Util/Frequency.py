class Frequency:
	def __init__(self):
		self.counts = {}

	def __str__(self):
		items = list(self.counts.items())
		sorted_items = sorted(items, key=lambda x: x[1], reverse=True)
		constructed_str = ''
		for i in sorted_items:
			constructed_str += f'{i[0]}: {i[1]}\n'
		return constructed_str

	def __repr__(self):
		return str(self.counts)

	def add(self, value):
		if value not in self.counts:
			self.counts[value] = 0
		self.counts[value] += 1

	def values(self):
		return self.counts.values()

# tests
if __name__ == '__main__':
	print('Frequency tests:')
	f = Frequency()
	for i in range(10):
		f.add(i)
	f.add(1)
	f.add(1)
	f.add(1)
	f.add(3)
	f.add(3)
	f.add(3)
	f.add(3)
	print(f)
