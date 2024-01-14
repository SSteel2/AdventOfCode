import Util.input
import Util.ranges

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

variables = ['x', 'm', 'a', 's']

def _parse(input_lines):
	workflows = {}
	parts = []

	is_first_parsing_stage = True
	for instruction in input_lines:
		if instruction == '':
			is_first_parsing_stage = False
			continue
		if is_first_parsing_stage:
			split1 = instruction.split('{')
			name = split1[0]
			split2 = split1[1].removesuffix('}').split(',')
			rules = []
			for i in split2:
				split3 = i.split(':')
				if len(split3) == 1:
					rules.append({'variable': None, 'condition': None, 'value': None, 'destination': split3[0]})
				else:
					rules.append({'variable': split3[0][0], 'condition': split3[0][1], 'value': int(split3[0][2:]), 'destination': split3[1]})
			workflows[name] = rules
		else:
			split1 = instruction.removesuffix('}').removeprefix('{').split(',')
			part = {}
			for i in split1:
				part[i[0]] = int(i[2:])
			parts.append(part)
	return workflows, parts

def _processWorkflow(part, rules):
	for rule in rules:
		if rule['variable'] == None:
			return rule['destination']
		if rule['condition'] == '>' and part[rule['variable']] > rule['value']:
			return rule['destination']
		if rule['condition'] == '<' and part[rule['variable']] < rule['value']:
			return rule['destination']

def silver(input_lines):
	workflows, parts = _parse(input_lines)
	accepted_parts = []
	start_workflow = 'in'
	for part in parts:
		workflow_name = start_workflow
		while workflow_name != 'R':
			workflow_name = _processWorkflow(part, workflows[workflow_name])
			if workflow_name == 'A':
				accepted_parts.append(part)
				break

	total = 0
	for i in accepted_parts:
		total += i['x'] + i['m'] + i['a'] + i['s']
	return total

def _countVariants(ranges):
	variants = 1
	for variable in variables:
		variants *= len(ranges[variable])
	return variants

def _solveWorkflow(workflow_name, ranges, workflows):
	if workflow_name == 'A':
		variants = _countVariants(ranges)
		return variants
	if workflow_name == 'R':
		return 0
	rules = workflows[workflow_name]

	variants = 0
	for rule in rules:
		if rule['variable'] == None:
			variants += _solveWorkflow(rule['destination'], ranges, workflows)
			continue
		split_number = rule['value']
		if rule['condition'] == '>':
			split_number += 1
		split_range = ranges[rule['variable']].split(split_number)
		left = ranges.copy()
		left[rule['variable']] = split_range[0]
		right = ranges.copy()
		right[rule['variable']] = split_range[1]
		if rule['condition'] == '<':
			variants += _solveWorkflow(rule['destination'], left, workflows)
			ranges = right
		else:
			variants += _solveWorkflow(rule['destination'], right, workflows)
			ranges = left
	return variants

def gold(input_lines):
	workflows, _ = _parse(input_lines)
	ranges = {variable: Util.ranges.Spans(Util.ranges.Span(1, 4001)) for variable in variables}
	variants = _solveWorkflow('in', ranges, workflows)
	return variants
