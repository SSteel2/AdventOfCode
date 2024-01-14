import collections
import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

B = 'broadcaster'
FF = 'flip-flop'
CON = 'conjunction'

def _parseEquipment(input_lines):
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

def _processBroadcaster(current, equipment):
	receivers = []
	name = current[0]
	signal = current[1]
	for i in equipment[name]['outputs']:
		receivers.append((i, signal, name))
	return receivers

def _processFlipflop(current, equipment):
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

def _processConjunction(current, equipment):
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

def _processQueue(queue, equipment, counts):
	while len(queue) > 0:
		receivers = []
		current = queue.pop()
		counts[current[1]] += 1
		if current[0] not in equipment:
			continue
		if equipment[current[0]]['type'] == B:
			receivers = _processBroadcaster(current, equipment)
		elif equipment[current[0]]['type'] == FF:
			receivers = _processFlipflop(current, equipment)
		elif equipment[current[0]]['type'] == CON:
			receivers = _processConjunction(current, equipment)
		for receiver in receivers:
			queue.appendleft(receiver)

def _pushButton(equipment, func, params):
	queue = collections.deque()
	queue.appendleft((B, 'low', 'button'))
	func(queue, equipment, *params)

def silver(input_lines):
	equipment = _parseEquipment(input_lines)
	counts = {'low': 0, 'high': 0}
	for i in range(1000):
		_pushButton(equipment, _processQueue, [counts])
	return counts['low'] * counts['high']

def _processQueueGold(queue, equipment, con_memory, button_pushes):
	while len(queue) > 0:
		receivers = []
		current = queue.pop()
		if current[0] not in equipment:
			continue
		if equipment[current[0]]['type'] == B:
			receivers = _processBroadcaster(current, equipment)
		elif equipment[current[0]]['type'] == FF:
			receivers = _processFlipflop(current, equipment)
		elif equipment[current[0]]['type'] == CON:
			if current[0] in con_memory and current[1] == 'low':
				con_memory[current[0]].append(button_pushes)
			receivers = _processConjunction(current, equipment)
		for receiver in receivers:
			queue.appendleft(receiver)

def gold(input_lines):
	equipment = _parseEquipment(input_lines)

	con_memory = {}
	for name in equipment:
		if equipment[name]['type'] == CON and len(equipment[name]['memory']) == 1:
			con_memory[name] = []

	button_pushes = 0
	max_count = 5000
	current_push = 0
	while button_pushes < max_count:
		button_pushes += 1
		_pushButton(equipment, _processQueueGold, [con_memory, button_pushes])

	product = 1
	for name in con_memory:
		product *= con_memory[name][0]
	return product
