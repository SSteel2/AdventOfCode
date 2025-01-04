import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(input_lines):
	wires = {}
	gates = []
	for line in input_lines:
		split_line = line.split(' ')
		if len(split_line) == 3:  # assignment
			try:
				wires[split_line[2]] = int(split_line[0])
			except ValueError:
				gates.append({'command': 'EQUALS', 'operand1': split_line[0], 'operand2': None, 'result': split_line[2]})
		elif len(split_line) == 4:  # negation
			gates.append({'command': split_line[0], 'operand1': split_line[1], 'operand2': None, 'result': split_line[3]})
		elif len(split_line) == 5:
			gates.append({'command': split_line[1], 'operand1': split_line[0], 'operand2': split_line[2], 'result': split_line[4]})
	return wires, gates

def _calculate(command, left, right):
	if command == 'EQUALS':
		return left
	elif command == 'NOT':
		return left ^ 65535
	elif command == 'RSHIFT':
		return left >> right
	elif command == 'LSHIFT':
		return (left << right) % 65536
	elif command == 'AND':
		return left & right
	elif command == 'OR':
		return left | right

def _calculate_circuit(wires, gates):
	new_wires = len(wires)
	while new_wires > 0:
		new_wires = 0
		for gate in gates:
			if gate['result'] not in wires and gate['operand1'] in wires and gate['operand2'] in wires:
				wires[gate['result']] = _calculate(gate['command'], wires[gate['operand1']], wires[gate['operand2']])
				new_wires += 1
	return wires['a']

def silver(input_lines):
	wires, gates = _parse(input_lines)
	wires[None] = 0
	for i in range(16):
		wires[str(i)] = i
	return _calculate_circuit(wires, gates)

def gold(input_lines):
	wires, gates = _parse(input_lines)
	wires[None] = 0
	for i in range(16):
		wires[str(i)] = i
	wires['b'] = _calculate_circuit(dict(wires), gates)
	return _calculate_circuit(wires, gates)
