input_lines = []
with open('input.txt', 'r') as input_file:
	for line in input_file:
		input_lines.append(line.removesuffix('\n'))

# Parse input
workflows = {}
parts = []

is_first_parsing_stage = True
for instruction in input_lines:
	if instruction == '':
		is_first_parsing_stage = False
		continue
	if is_first_parsing_stage:
		split1 = instruction.split('{')
		name = split1[0]
		# split1[1] = split1[1].removesuffix('}')
		split2 = split1[1].removesuffix('}').split(',')
		rules = []
		for i in split2:
			split3 = i.split(':')
			if len(split3) == 1:
				rules.append({'variable': None, 'condition': None, 'value': None, 'destination': split3[0]})
			else:
				rules.append({'variable': split3[0][0], 'condition': split3[0][1], 'value': int(split3[0][2:]), 'destination': split3[1]})
		workflows[name] = rules
	else:
		split1 = instruction.removesuffix('}').removeprefix('{').split(',')
		part = {}
		for i in split1:
			part[i[0]] = int(i[2:])
		parts.append(part)

# Silver star

def ProcessWorkflow(part, workflow_name):
	rules = workflows[workflow_name]
	for rule in rules:
		if rule['variable'] == None:
			return rule['destination']
		if rule['condition'] == '>' and part[rule['variable']] > rule['value']:
			return rule['destination']
		if rule['condition'] == '<' and part[rule['variable']] < rule['value']:
			return rule['destination']

accepted_parts = []
start_workflow = 'in'
for part in parts:
	workflow = start_workflow
	while workflow != 'R':
		workflow = ProcessWorkflow(part, workflow)
		if workflow == 'A':
			accepted_parts.append(part)
			break

total = 0
for i in accepted_parts:
	total += i['x'] + i['m'] + i['a'] + i['s']

print('Silver answer: ' + str(total))

# Gold star

# MAJOR TODO: Write a bootstrapper which launches and enables proper import of util files
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

variables = ['x', 'm', 'a', 's']

def CountVariants(ranges):
	variants = 1
	for variable in variables:
		variants *= len(ranges[variable])
	return variants


def SolveWorkflow(workflow_name, ranges):
	if workflow_name == 'A':
		variants = CountVariants(ranges)
		return variants
	if workflow_name == 'R':
		return 0
	rules = workflows[workflow_name]

	variants = 0
	for rule in rules:
		if rule['variable'] == None:
			variants += SolveWorkflow(rule['destination'], ranges)
			continue
		split_number = rule['value']
		if rule['condition'] == '>':
			split_number += 1
		split_range = ranges[rule['variable']].split(split_number)
		left = ranges.copy()
		left[rule['variable']] = split_range[0]
		right = ranges.copy()
		right[rule['variable']] = split_range[1]
		if rule['condition'] == '<':
			variants += SolveWorkflow(rule['destination'], left)
			ranges = right
		else:
			variants += SolveWorkflow(rule['destination'], right)
			ranges = left
	return variants

ranges = {'x': Spans(Span(1, 4001)), 'm': Spans(Span(1, 4001)), 'a': Spans(Span(1, 4001)), 's': Spans(Span(1, 4001))}
variants = SolveWorkflow('in', ranges)
print('Gold answer: ' + str(variants))
