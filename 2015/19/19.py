import Util.input
from math import inf

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(input_lines):
	rules = {}
	molecule = ''
	is_first_phase = True
	for line in input_lines:
		if line == '':
			is_first_phase = False
			continue
		if is_first_phase:
			split_line = line.split(' => ')
			if split_line[0] in rules:
				rules[split_line[0]].append(split_line[1])
			else:
				rules[split_line[0]] = [split_line[1]]
		else:
			molecule = line
	return rules, molecule

def _find_all(text, pattern):
	start = 0
	while True:
		start = text.find(pattern, start)
		if start == -1:
			return
		yield start
		start += len(pattern)

def _create_combination(text, index, pattern, result):
	return text[:index] + result + text[index + len(pattern):]

def silver(input_lines):
	rules, molecule = _parse(input_lines)
	combinations = set()
	for key in rules:
		for index in _find_all(molecule, key):
			for result in rules[key]:
				combinations.add(_create_combination(molecule, index, key, result))
	return len(combinations)

def _create_molecule(current, target, rules, moves):
	if current == target:
		return moves
	for key in rules:
		for index in _find_all(current, key):
			current_moves = _create_molecule(_create_combination(current, index, key, rules[key]), target, rules, moves + 1)
			if current_moves < inf:
				return current_moves

def _invert_rules(rules):
	inverted_rules = {}
	for key in rules:
		for result in rules[key]:
			inverted_rules[result] = key
	return inverted_rules

def gold(input_lines):
	rules, molecule = _parse(input_lines)
	rules = _invert_rules(rules)
	return _create_molecule(molecule, 'e', rules, 0)

