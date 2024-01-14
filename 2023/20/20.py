import collections
import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

B = 'broadcaster'
FF = 'flip-flop'
CON = 'conjunction'

def ParseEquipment(input_lines):
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

def ProcessBroadcaster(current, equipment):
	receivers = []
	name = current[0]
	signal = current[1]
	for i in equipment[name]['outputs']:
		receivers.append((i, signal, name))
	return receivers

def ProcessFlipflop(current, equipment):
	receivers = []
	name = current[0]
	signal = current[1]
	if signal == 'high':
		return receivers
	if equipment[name]['state'] == 'off':
		for i in equipment[name]['outputs']:
			receivers.append((i, 'high', name))
		equipment[name]['state'] = 'on'
	else:
		for i in equipment[name]['outputs']:
			receivers.append((i, 'low', name))
		equipment[name]['state'] = 'off'
	return receivers

def ProcessConjunction(current, equipment):
	receivers = []
	name = current[0]
	signal = current[1]
	sender = current[2]
	equipment[name]['memory'][sender] = signal
	if all([(True if equipment[name]['memory'][x] == 'high' else False) for x in equipment[name]['memory']]):
		for i in equipment[name]['outputs']:
			receivers.append((i, 'low', name))
	else:
		for i in equipment[name]['outputs']:
			receivers.append((i, 'high', name))
	return receivers

def ProcessQueue(queue, equipment, counts):
	while len(queue) > 0:
		receivers = []
		current = queue.pop()
		counts[current[1]] += 1
		if current[0] not in equipment:
			continue
		if equipment[current[0]]['type'] == B:
			receivers = ProcessBroadcaster(current, equipment)
		elif equipment[current[0]]['type'] == FF:
			receivers = ProcessFlipflop(current, equipment)
		elif equipment[current[0]]['type'] == CON:
			receivers = ProcessConjunction(current, equipment)
		for receiver in receivers:
			queue.appendleft(receiver)

def PushButton(equipment, func, params):
	queue = collections.deque()
	queue.appendleft((B, 'low', 'button'))
	func(queue, equipment, *params)

def silver(input_lines):
	equipment = ParseEquipment(input_lines)
	counts = {'low': 0, 'high': 0}
	for i in range(1000):
		PushButton(equipment, ProcessQueue, [counts])
	return counts['low'] * counts['high']

def ProcessQueueGold(queue, equipment, con_memory, button_pushes):
	while len(queue) > 0:
		receivers = []
		current = queue.pop()
		if current[0] not in equipment:
			continue
		if equipment[current[0]]['type'] == B:
			receivers = ProcessBroadcaster(current, equipment)
		elif equipment[current[0]]['type'] == FF:
			receivers = ProcessFlipflop(current, equipment)
		elif equipment[current[0]]['type'] == CON:
			if current[0] in con_memory and current[1] == 'low':
				con_memory[current[0]].append(button_pushes)
			receivers = ProcessConjunction(current, equipment)
		for receiver in receivers:
			queue.appendleft(receiver)

def gold(input_lines):
	equipment = ParseEquipment(input_lines)

	con_memory = {}
	for name in equipment:
		if equipment[name]['type'] == CON and len(equipment[name]['memory']) == 1:
			con_memory[name] = []

	button_pushes = 0
	max_count = 5000
	current_push = 0
	while button_pushes < max_count:
		button_pushes += 1
		PushButton(equipment, ProcessQueueGold, [con_memory, button_pushes])

	product = 1
	for name in con_memory:
		product *= con_memory[name][0]
	return product
