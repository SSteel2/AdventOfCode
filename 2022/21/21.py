import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(input_lines):
	monkeys = {}
	for line in input_lines:
		name, command = line.split(': ')
		orders = command.split(' ')
		if len(orders) == 1:
			monkeys[name] = {'value': int(orders[0])}
		else:
			monkeys[name] = {'argument_1': orders[0], 'operation': orders[1], 'argument_2': orders[2]}
	return monkeys

def _calculateValue(name, monkeys):
	arg1 = monkeys[monkeys[name]['argument_1']]['value']
	arg2 = monkeys[monkeys[name]['argument_2']]['value']
	if monkeys[name]['operation'] == '+':
		monkeys[name]['value'] = arg1 + arg2
	elif monkeys[name]['operation'] == '-':
		monkeys[name]['value'] = arg1 - arg2
	elif monkeys[name]['operation'] == '*':
		monkeys[name]['value'] = arg1 * arg2
	elif monkeys[name]['operation'] == '/':
		monkeys[name]['value'] = arg1 // arg2
	else:
		print('Error: Data corruption')

def _solve(monkeys):
	missing = -1
	while missing != 0:
		missing = 0
		for name in monkeys:
			if 'value' in monkeys[name]:
				continue
			if 'value' in monkeys[monkeys[name]['argument_1']] and 'value' in monkeys[monkeys[name]['argument_2']]:
				_calculateValue(name, monkeys)
			else:
				missing += 1

def silver(input_lines):
	monkeys = _parse(input_lines)
	_solve(monkeys)
	return monkeys['root']['value']

def _gatherInputs(name, monkeys):
	if 'value' in monkeys[name]:
		return set([name])
	else:
		return _gatherInputs(monkeys[name]['argument_1'], monkeys) | _gatherInputs(monkeys[name]['argument_2'], monkeys) | set([name])

def _calculateValueGold(name, monkeys):
	if 'value' in monkeys[name]:
		return monkeys[name]['value']
	if 'value' not in monkeys[monkeys[name]['argument_1']]:
		_calculateValueGold(monkeys[name]['argument_1'], monkeys)
	if 'value' not in monkeys[monkeys[name]['argument_2']]:
		_calculateValueGold(monkeys[name]['argument_2'], monkeys)
	if 'value' in monkeys[monkeys[name]['argument_1']] and 'value' in monkeys[monkeys[name]['argument_2']]:
		_calculateValue(name, monkeys)
	return monkeys[name]['value']

def _calculateValueInverse(target, left, right, operation):
	if operation == '+':
		if left == None:
			return target - right
		if right == None:
			return target - left
	if operation == '-':
		if left == None:
			return target + right
		if right == None:
			return left - target
	if operation == '*':
		if left == None:
			return target // right
		if right == None:
			return target // left
	if operation == '/':
		if left == None:
			return target * right
		if right == None:
			return left // target


def _findHumanValue(name, target, monkeys):
	if name == 'humn':
		return target
	inputs_left = _gatherInputs(monkeys[name]['argument_1'], monkeys)
	inputs_right = _gatherInputs(monkeys[name]['argument_2'], monkeys)
	if 'humn' in inputs_left:
		right = _calculateValueGold(monkeys[name]['argument_2'], monkeys)
		inverse_value = _calculateValueInverse(target, None, right, monkeys[name]['operation'])
		return _findHumanValue(monkeys[name]['argument_1'], inverse_value, monkeys)
	elif 'humn' in inputs_right:
		left = _calculateValueGold(monkeys[name]['argument_1'], monkeys)
		inverse_value = _calculateValueInverse(target, left, None, monkeys[name]['operation'])
		return _findHumanValue(monkeys[name]['argument_2'], inverse_value, monkeys)

def gold(input_lines):
	monkeys = _parse(input_lines)
	monkeys['root']['operation'] = '-'
	return _findHumanValue('root', 0, monkeys)
