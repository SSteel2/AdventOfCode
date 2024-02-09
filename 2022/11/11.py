import Util.input
import Util.Frequency

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _createOperation(members, is_worry_reduced, common_reducer):
	if is_worry_reduced:
		if members[1] == '+':
			return lambda x: ((x + int(members[2])) // 3) % (common_reducer * 3)
		elif members[1] == '*' and members[0] == members[2] == 'old':
			return lambda x: ((x * x) // 3) % (common_reducer * 3)
		elif members[1] == '*':
			return lambda x: ((x * int(members[2])) // 3) % (common_reducer * 3)
	else:
		if members[1] == '+':
			return lambda x: (x + int(members[2])) % common_reducer
		elif members[1] == '*' and members[0] == members[2] == 'old':
			return lambda x: (x * x) % common_reducer
		elif members[1] == '*':
			return lambda x: (x * int(members[2])) % common_reducer

def _parseMonkey(monkey_lines, is_worry_reduced):
	monkey = {}
	monkey_id = int(monkey_lines[0].split(' ')[1].removesuffix(':'))
	monkey['items'] = [int(i) for i in monkey_lines[1].split(': ')[1].split(', ')]
	monkey['operation_params'] = monkey_lines[2].split('= ')[1].split(' ')
	monkey['test'] = int(monkey_lines[3].split(' ')[-1])
	monkey[True] = int(monkey_lines[4].split(' ')[-1])
	monkey[False] = int(monkey_lines[5].split(' ')[-1])
	return monkey_id, monkey

def _parse(input_lines, is_worry_reduced):
	monkeys = {}
	monkey_lines = []
	for line in input_lines:
		if line != '':
			monkey_lines.append(line)
		else:
			monkey_id, monkey = _parseMonkey(monkey_lines, is_worry_reduced)
			monkeys[monkey_id] = monkey
			monkey_lines = []
	monkey_id, monkey = _parseMonkey(monkey_lines, is_worry_reduced)
	monkeys[monkey_id] = monkey

	multiplier = 1
	for monkey_id in monkeys:
		multiplier *= monkeys[monkey_id]['test']
	for monkey_id in monkeys:
		monkeys[monkey_id]['operation'] = _createOperation(monkeys[monkey_id]['operation_params'], is_worry_reduced, multiplier)
	return monkeys

def _solve(input_lines, total_rounds, is_worry_reduced):
	monkeys = _parse(input_lines, is_worry_reduced)
	inspections = Util.Frequency.Frequency()
	for _ in range(total_rounds):
		for monkey_id in monkeys:
			inspections.add(monkey_id, len(monkeys[monkey_id]['items']))
			for item in monkeys[monkey_id]['items']:
				new_value = monkeys[monkey_id]['operation'](item)
				monkeys[monkeys[monkey_id][new_value % monkeys[monkey_id]['test'] == 0]]['items'].append(new_value)
			monkeys[monkey_id]['items'] = []
	values = inspections.orderedValues()
	return values[0] * values[1]	

def silver(input_lines):
	return _solve(input_lines, 20, True)

def gold(input_lines):
	return _solve(input_lines, 10000, False)
