import Util.input
import re

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def silver(input_lines):
	pattern = '-?\\d+'
	iterator = re.finditer(pattern, input_lines[0])
	total = 0
	for item in iterator:
		total += int(item[0])
	return total

def _sum_not_red(node):
	if isinstance(node, dict):
		if 'red' in node.values():
			return 0
		return sum([_sum_not_red(node[i]) for i in node])
	elif isinstance(node, list):
		return sum([_sum_not_red(i) for i in node])
	elif isinstance(node, int):
		return node
	elif isinstance(node, str):
		return 0

def gold(input_lines):
	json = eval(input_lines[0])
	return _sum_not_red(json)
