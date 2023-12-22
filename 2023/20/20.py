import collections

input_lines = []
with open('input.txt', 'r') as input_file:
	for line in input_file:
		input_lines.append(line.removesuffix('\n'))

B = 'broadcaster'
FF = 'flip-flop'
CON = 'conjunction'

# Parse input
def ParseEquipment():
	equipment = {}
	for line in input_lines:
		split_arrow = line.split(' -> ')
		outputs = split_arrow[1].split(', ')
		if split_arrow[0] == B:
			equipment[split_arrow[0]] = {'type': B, 'outputs': outputs}
		elif split_arrow[0][0] == '%':
			equipment[split_arrow[0][1:]] = {'type': FF, 'outputs': outputs, 'state': 'off'}
		elif split_arrow[0][0] == '&':
			equipment[split_arrow[0][1:]] = {'type': CON, 'outputs': outputs, 'memory': None}
	for name in equipment:
		if equipment[name]['type'] == CON:
			memory = {}
			for i in equipment:
				if name in equipment[i]['outputs']:
					memory[i] = 'low'
			equipment[name]['memory'] = memory
	return equipment

# Silver star
def ProcessBroadcaster(current):
	name = current[0]
	signal = current[1]
	for i in equipment[name]['outputs']:
		queue.appendleft((i, signal, name))

def ProcessFlipflop(current):
	name = current[0]
	signal = current[1]
	if signal == 'high':
		return
	if equipment[name]['state'] == 'off':
		for i in equipment[name]['outputs']:
			queue.appendleft((i, 'high', name))
		equipment[name]['state'] = 'on'
	else:
		for i in equipment[name]['outputs']:
			queue.appendleft((i, 'low', name))
		equipment[name]['state'] = 'off'

def ProcessConjunction(current):
	name = current[0]
	signal = current[1]
	sender = current[2]
	equipment[name]['memory'][sender] = signal
	if all([(True if equipment[name]['memory'][x] == 'high' else False) for x in equipment[name]['memory']]):
		for i in equipment[name]['outputs']:
			queue.appendleft((i, 'low', name))
	else:
		for i in equipment[name]['outputs']:
			queue.appendleft((i, 'high', name))

def ProcessQueue():
	while len(queue) > 0:
		current = queue.pop()
		# print(f"{current[2]} -{current[1]}-> {current[0]}")
		counts[current[1]] += 1
		if current[0] not in equipment:
			continue
		if equipment[current[0]]['type'] == B:
			ProcessBroadcaster(current)
		elif equipment[current[0]]['type'] == FF:
			ProcessFlipflop(current)
		elif equipment[current[0]]['type'] == CON:
			ProcessConjunction(current)			

def PushButton():
	queue.appendleft((B, 'low', 'button'))
	ProcessQueue()

queue = collections.deque()
counts = {'low': 0, 'high': 0}

equipment = ParseEquipment()

for i in range(1000):
	PushButton()

print('Silver answer: ' + str(counts['low'] * counts['high']))

# Gold star

def ProcessQueueGold():
	while len(queue) > 0:
		current = queue.pop()
		# print(f"{current[2]} -{current[1]}-> {current[0]}")
		counts[current[1]] += 1
		if current[0] not in equipment:
			continue
		if equipment[current[0]]['type'] == B:
			ProcessBroadcaster(current)
		elif equipment[current[0]]['type'] == FF:
			ProcessFlipflop(current)
		elif equipment[current[0]]['type'] == CON:
			if current[0] in con_memory and current[1] == 'low':
				con_memory[current[0]].append(button_pushes)
			ProcessConjunction(current)

def PushButtonGold():
	queue.appendleft((B, 'low', 'button'))
	ProcessQueueGold()

queue = collections.deque()
equipment = ParseEquipment()

con_memory = {}
for name in equipment:
	if equipment[name]['type'] == CON and len(equipment[name]['memory']) == 1:
		con_memory[name] = []

button_pushes = 0
max_count = 5000
current_push = 0
while max_count > 0:
	button_pushes += 1
	PushButtonGold()
	max_count -= 1

product = 1
for name in con_memory:
	product *= con_memory[name][0]

print('Gold answer: ' + str(product))
