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

	def union(self, spans):
		all_spans = sorted(self.spans + spans.spans)
		i = 0
		while i < len(all_spans) - 1:
			if all_spans[i].isIntersecting(all_spans[i + 1]):
				all_spans = all_spans[:i] + all_spans[i].union(all_spans[i + 1]) + all_spans[i + 2:]
			else:
				i += 1
		self.spans = all_spans

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