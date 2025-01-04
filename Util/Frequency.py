class Frequency:
	'''Wrapper class for dict. Meant for quickly counting frequencies of items.'''

	def __init__(self):
		self.counts = {}

	def __str__(self):
		return self.orderedByValue()

	def __repr__(self):
		return str(self.counts)

	def add(self, value, count=1):
		if value not in self.counts:
			self.counts[value] = 0
		self.counts[value] += count

	def values(self):
		return self.counts.values()

	def keys(self):
		return self.counts.keys()

	def __getitem__(self, key):
		return self.counts[key]

	def __contains__(self, item):
		return item in self.counts

	def orderedValues(self):
		return sorted(list(self.counts.values()), reverse=True)

	def orderedByValue(self):
		sorted_items = sorted(list(self.counts.items()), key=lambda x: x[1], reverse=True)
		return self._constructString(sorted_items)		

	def orderedByKey(self):
		sorted_items = sorted(list(self.counts.items()), key=lambda x: x[0])
		return self._constructString(sorted_items)

	def _constructString(self, items):
		constructed_str = ''
		for i in items:
			constructed_str += f'{i[0]}: {i[1]}\n'
		return constructed_str

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
	print('Contains check (should be true)')
	print(3 in f)
	print('Order by value')
	print(f)
	print('Order by key')
	print(f.orderedByKey())
