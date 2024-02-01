import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(input_lines):
	is_instruction_stage = False
	crate_lines = []
	instructions = []
	for line in input_lines:
		if not is_instruction_stage and line == "":
			is_instruction_stage = True
			continue
		if is_instruction_stage:
			split_on_from = line.split(' from ')
			split_on_to = split_on_from[1].split(' to ')
			instructions.append({'move': int(split_on_from[0][4:]), 'from': int(split_on_to[0]) - 1, 'to': int(split_on_to[1]) - 1})
		else:
			crate_lines.append(line)
	crates_count = len(crate_lines[-1][1:-1].split('   '))
	crates = [[] for i in range(crates_count)]
	for line in crate_lines[-2::-1]:
		for i in range(crates_count):
			crate = line[1 + 4 * i]
			if crate == ' ':
				continue
			crates[i].append(crate)
	return crates, instructions

def _move(crates, from_crate, to_crate, count):
	for i in range(count):
		crates[to_crate].append(crates[from_crate].pop())

def _moveGold(crates, from_crate, to_crate, count):
	crates[to_crate] += crates[from_crate][-count:]
	crates[from_crate] = crates[from_crate][:-count]

def _solution(input_lines, move_function):
	crates, instructions = _parse(input_lines)
	for i in instructions:
		move_function(crates, i['from'], i['to'], i['move'])
	return ''.join(i[-1] for i in crates)

def silver(input_lines):
	return _solution(input_lines, _move)

def gold(input_lines):
	return _solution(input_lines, _moveGold)
