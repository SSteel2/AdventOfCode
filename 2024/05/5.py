import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(input_lines):
	rules = {}
	updates = []
	is_first_parsing_stage = True
	for instruction in input_lines:
		if instruction == '':
			is_first_parsing_stage = False
			continue
		if is_first_parsing_stage:
			pages = instruction.split('|')
			if int(pages[0]) not in rules:
				rules[int(pages[0])] = [int(pages[1])]
			else:
				rules[int(pages[0])].append(int(pages[1]))
		else:
			updates.append([int(i) for i in instruction.split(',')])
	return rules, updates

def _check_rule_adhearing(update, rules):
	for index, page in enumerate(update):
		if page not in rules:
			continue
		for pre_page in update[:index]:
			if pre_page in rules[page]:
				return False
	return True

def _make_rule_adhearing(update, rules):
	current_order = update
	while not _check_rule_adhearing(current_order, rules):
		for index, page in enumerate(current_order):
			if page not in rules:
				continue
			for pre_index, pre_page in enumerate(current_order[:index]):
				if pre_page in rules[page]:
					current_order = current_order[:pre_index] + [current_order[index]] + current_order[pre_index:index] + current_order[index + 1:]
	return current_order

def silver(input_lines):
	rules, updates = _parse(input_lines)
	middle_sum = 0
	for update in updates:
		if _check_rule_adhearing(update, rules):
			middle_sum += update[len(update) // 2]
	return middle_sum

def gold(input_lines):
	rules, updates = _parse(input_lines)
	middle_sum = 0
	for update in updates:
		if not _check_rule_adhearing(update, rules):
			correct_order = _make_rule_adhearing(update, rules)
			middle_sum += correct_order[len(correct_order) // 2]
	return middle_sum
