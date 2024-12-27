import Util.input
from operator import itemgetter

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(input_lines):
	first_section = True
	initial_values = {}
	gates = []
	for line in input_lines:
		if line == "":
			first_section = False
			continue
		if first_section:
			split_line = line.split(': ')
			initial_values[split_line[0]] = bool(int(split_line[1]))
		else:
			split_line = line.split(' ')
			gates.append({'operand1': split_line[0], 'opearation': split_line[1], 'operand2': split_line[2], 'result': split_line[4]})
	return initial_values, gates

def _calculate(operand1, operand2, operation):
	if operation == 'AND':
		return operand1 and operand2
	elif operation == 'OR':
		return operand1 or operand2
	elif operation == 'XOR':
		return operand1 ^ operand2

def _solve(wires, gates):
	added_values = 0
	while True:
		for gate in gates:
			if gate['result'] not in wires and gate['operand1'] in wires and gate['operand2'] in wires:
				wires[gate['result']] = _calculate(wires[gate['operand1']], wires[gate['operand2']], gate['opearation'])
				added_values += 1
		if added_values == 0:
			break
		else:
			added_values = 0

def _collect_number(wires):
	z_numbers = []
	for wire in wires:
		if wire[0] == 'z':
			z_numbers.append((int(wire[1:]), int(wires[wire])))
	z_numbers.sort(key=itemgetter(0))
	return int(''.join([str(i[1]) for i in z_numbers][::-1]), 2)

def silver(input_lines):
	wires, gates = _parse(input_lines)
	_solve(wires, gates)
	return _collect_number(wires)

def _swap_results(gates, result1, result2):
	gate1 = None
	gate2 = None
	for gate in gates:
		if gate['result'] == result1:
			gate1 = gate
		elif gate['result'] == result2:
			gate2 = gate
	gate1['prev_result'], gate1['result'] = gate1['result'], result2
	gate2['prev_result'], gate2['result'] = gate2['result'], result1

def _collect_gates(gates):
	'''Will follow this naming scheme for looking through gates:
	g1: x_n   XOR y_n   = a_n
	g2: a_n   XOR t_n-1 = z_n
	g3: t_n-1 AND a_n   = b_n
	g4: x_n   AND y_n   = c_n
	g5: b_n   OR  c_n   = t_n
	'''

	# sort x and/xor y gates, for easier access
	g1 = {}
	g4 = {}
	max_number = -1
	for gate in gates:
		if gate['operand1'][0] == 'y' and gate['operand2'][0] == 'x':
			gate['operand1'], gate['operand2'] = gate['operand2'], gate['operand1']
		if gate['operand1'][0] == 'x':
			number = int(gate['operand1'][1:])
			if gate['opearation'] == 'XOR':
				g1[number] = gate
			elif gate['opearation'] == 'AND':
				g4[number] = gate
			if number > max_number:
				max_number = number

	incorrect_results = []

	g2 = {}
	g3 = {}
	g5 = {}
	transfer_previous = g4[0]['result']
	for i in range(1, max_number + 1):
		for gate in gates:
			# all good
			if (gate['operand1'] == transfer_previous or gate['operand2'] == transfer_previous) and (gate['operand1'] == g1[i]['result'] or gate['operand2'] == g1[i]['result']):
				if gate['opearation'] == 'XOR':
					g2[i] = gate
				elif gate['opearation'] == 'AND':
					g3[i] = gate
			# g1 or transfer_prev failed
			elif (gate['operand1'] == transfer_previous or gate['operand2'] == transfer_previous):
				if gate['opearation'] == 'XOR':
					if i in g2:
						g2[i].append(("transfer_prev", transfer_previous, gate))
					else:
						g2[i] = [("transfer_prev", transfer_previous, gate)]
				elif gate['opearation'] == 'AND':
					if i in g3:
						g3[i].append(("transfer_prev", transfer_previous, gate))
					else:
						g3[i] = [("transfer_prev", transfer_previous, gate)]
			elif (gate['operand1'] == g1[i]['result'] or gate['operand2'] == g1[i]['result']):
				if gate['opearation'] == 'XOR':
					if i in g2:
						g2[i].append(("g1", g1[i]['result'], gate))
					else:
						g2[i] = [("g1", g1[i]['result'], gate)]
				elif gate['opearation'] == 'AND':
					if i in g3:
						g3[i].append(("g1", g1[i]['result'], gate))
					else:
						g3[i] = [("g1", g1[i]['result'], gate)]
		
		# fix found mistake
		if 'result' not in g2[i]:
			if len(g2[i]) == 1:
				other_operand = g2[i][0][2]['operand2'] if g2[i][0][2]['operand1'] == g2[i][0][1] else g2[i][0][2]['operand1']
				if g2[i][0][0] == 'transfer_prev':
					incorrect_results.append(g1[i]['result'])
					incorrect_results.append(other_operand)
					_swap_results(gates, g1[i]['result'], other_operand)
				if g2[i][0][0] == 'g1':
					incorrect_results.append(g5[i - 1]['result'])
					incorrect_results.append(other_operand)
					_swap_results(gates, g5[i - 1]['result'], other_operand)
				g2[i], g3[i] = g2[i][0][2], g3[i][0][2]

		for gate in gates:
			if i in g3 and 'result' in g3[i]:
				if gate['opearation'] == 'OR' and (gate['operand1'] == g3[i]['result'] or gate['operand2'] == g3[i]['result']) and (gate['operand1'] == g4[i]['result'] or gate['operand2'] == g4[i]['result']):
					g5[i] = gate
					transfer_previous = gate['result']
					break
				elif gate['opearation'] == 'OR' and (gate['operand1'] == g3[i]['result'] or gate['operand2'] == g3[i]['result']):
					g5[i] = [("g3", g3[i]['result'], gate)]
					transfer_previous = gate['result']
					break
				elif gate['opearation'] == 'OR' and (gate['operand1'] == g4[i]['result'] or gate['operand2'] == g4[i]['result']):
					g5[i] = [("g4", g4[i]['result'], gate)]
					transfer_previous = gate['result']
					break
			else:
				if gate['opearation'] == 'OR' and (gate['operand1'] == g4[i]['result'] or gate['operand2'] == g4[i]['result']):
					g5[i] = gate
					transfer_previous = gate['result']
					break

		# fix found mistake
		if 'result' not in g5[i]:
			good_operand = g5[i][0][1]
			other_operand = g5[i][0][2]['operand2'] if g5[i][0][2]['operand1'] == good_operand else g5[i][0][2]['operand1']
			if g5[i][0][0] == 'g3':
				incorrect_results.append(g4[i]['result'])
				incorrect_results.append(other_operand)
				_swap_results(gates, g4[i]['result'], other_operand)
			if g5[i][0][0] == 'g4':
				incorrect_results.append(g3[i]['result'])
				incorrect_results.append(other_operand)
				_swap_results(gates, g3[i]['result'], other_operand)
			g5[i] = g5[i][0][2]

	return incorrect_results

def gold(input_lines):
	wires, gates = _parse(input_lines)
	result = _collect_gates(gates)
	return ','.join(sorted(result))
