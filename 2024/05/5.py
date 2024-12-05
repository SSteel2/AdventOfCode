import Util.input
from functools import cmp_to_key

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

def _compare_order(a, b, rules):
	if a in rules and b in rules[a]:
		return -1
	if b in rules and a in rules[b]:
		return 1
	return 0

def _make_rule_adhearing(update, rules):
	return sorted(update, key=cmp_to_key(lambda a, b: _compare_order(a, b, rules)))

def _quickselect(pages, index, rules):
	'''This is a really cool O(n) median selection algorithm. It actually selects the k-th largest element in a list.
	More information about it: https://rcoh.me/posts/linear-time-median-finding/
	Unfortunately, since the lists are really small a standard sort approach works ~0.0038s faster in this case.
	Leaving this in here in case I ever need something like it.
	'''
	if len(pages) == 1:
		return pages[0]
	pivot = pages[0]
	lows = [page for page in pages if _compare_order(page, pivot, rules) == -1]
	highs = [page for page in pages if _compare_order(page, pivot, rules) == 1]
	pivots = [page for page in pages if _compare_order(page, pivot, rules) == 0]
	if index < len(lows):
		return _quickselect(lows, index, rules)
	elif index < len(lows) + len(pivots):
		return pivots[0]
	else:
		return _quickselect(highs, index - len(lows) - len(pivots), rules)

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
			# middle_sum += _quickselect(update, len(update) // 2, rules)
	return middle_sum
