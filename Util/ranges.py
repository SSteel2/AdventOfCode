# Using the word Span instead of Range, since range is already a built-in python function

class Span:
	def __init__(self, start, end):
		self.start = start # inclusive
		self.end = end # exclusive

	def __str__(self):
		return f"Span({self.start}, {self.end})"

	def __repr__(self):
		return self.__str__()

	def __lt__(self, other):
		return self.start < other.start

	def __len__(self):
		return self.end - self.start

	def isIntersecting(self, span):
		return span.end > self.start and self.end > span.start

	def intersection(self, span):
		if span.end <= self.start or self.end <= span.start:
			return []
		return [Span(max(span.start, self.start), min(self.end, span.end))]

	def difference(self, span):
		if span.end <= self.start or self.end <= span.start:
			return [Span(self.start, self.end)]
		result = []
		if self.start < span.start:
			result.append(Span(self.start, span.start))
		if self.end > span.end:
			result.append(Span(span.end, self.end))
		return result

	def union(self, span):
		if span.end < self.start or self.end < span.start:
			return [Span(self.start, self.end), Span(span.start, span.end)]
		return [Span(min(self.start, span.start), max(self.end, span.end))]

	def split(self, position):
		if position <= self.start:
			return [Span(None, None), Span(self.start, self.end)]
		if position >= self.end:
			return [Span(self.start, self.end), Span(None, None)]
		return [Span(self.start, position), Span(position, self.end)]

	def move(self, offset):
		self.start += offset
		self.end += offset
		return self

class Spans:
	def __init__(self, span=None):
		if span != None:
			self.spans = [span]
		else:
			self.spans = []

	def __str__(self):
		return str(self.spans)

	def __repr__(self):
		return self.__str__()

	def __len__(self):
		length = 0
		for i in self.spans:
			length += len(i)
		return length

	def intersection(self, span):
		result = []
		for r in self.spans:
			if r.isIntersecting(span):
				result.extend(r.intersection(span))
		return result

	def subtract(self, span):
		result = []
		for r in self.spans:
			rr = r.difference(span)
			result.extend(rr)
		self.spans = result

	def union(self, spans):
		all_spans = sorted(self.spans + spans.spans)
		i = 0
		while i < len(all_spans) - 1:
			if all_spans[i].isIntersecting(all_spans[i + 1]):
				all_spans = all_spans[:i] + all_spans[i].union(all_spans[i + 1]) + all_spans[i + 2:]
			else:
				i += 1
		self.spans = all_spans
		return self

	def add(self, span):
		self.spans.append(span)

	def split(self, position):
		left = Spans()
		right = Spans()
		for r in self.spans:
			result = r.split(position)
			left.add(result[0])
			right.add(result[1])
		return (left, right)

# tests
if __name__ == '__main__':
	print('Span tests:')
	a = Span(5, 10)
	b = Span(7, 20)
	print(f'{a.intersection(b)} should be (7, 10)')
	print(f'{a.difference(b)} should be (5, 7)')
	c = Span(2, 6)
	print(f'{a.intersection(c)} should be (5, 6)')
	print(f'{a.difference(c)} should be (6, 10)')
	d = Span(1, 5)
	print(f'{a.intersection(d)} should be ()')
	print(f'{a.difference(d)} should be (5, 10)')
	e = Span(10, 50)
	print(f'{a.intersection(e)} should be ()')
	print(f'{a.difference(e)} should be (5, 10)')
	f = Span(6, 8)
	print(f'{a.intersection(f)} should be (6, 8)')
	print(f'{a.difference(f)} should be (5, 6), (8, 10)')
	g = Span(1, 15)
	print(f'{a.intersection(g)} should be (5, 10)')
	print(f'{a.difference(g)} should be ()')
	print()
	print('Spans tests:')
	ss = Spans(Span(5, 10))
	ss.add(Span(15, 20))
	sa = Spans(Span(7, 16))
	sa.add(Span(19, 22))
	ss.union(sa)
	print(f'{ss} should be (5, 22)')
	ss = Spans(Span(5, 10))
	ss.add(Span(15, 20))
	ss.subtract(Span(6, 18))
	print(f'{ss} should be (5, 6), (18, 20)')
	ss = Spans(Span(5, 10))
	ss.add(Span(15, 20))
	ss.subtract(Span(10, 15))
	print(f'{ss} should be (5, 10), (15, 20)')
	ss = Spans(Span(5, 10))
	ss.add(Span(15, 20))
	ss.subtract(Span(6, 8))
	print(f'{ss} should be (5, 6), (8, 10), (15, 20)')
	ss = Spans(Span(5, 10))
	ss.add(Span(15, 20))
	print(f'{ss.intersection(Span(6, 18))} should be (6, 10), (15, 18)')
	print(f'{ss.intersection(Span(10, 15))} should be ()')
	print(f'{ss.intersection(Span(6, 8))} should be (6, 8)')
	print(f'{ss.intersection(Span(0, 30))} should be (5, 10), (15, 20)')

