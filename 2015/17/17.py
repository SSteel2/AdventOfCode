import Util.input
import Util.Frequency

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parseLine(line):
	return int(line)

def _fit_containers(container_sizes, eggnog, current_size):
	combination_sizes = Util.Frequency.Frequency()
	for index, size in enumerate(container_sizes):
		if size < eggnog:
			combination_sizes.merge(_fit_containers(container_sizes[index + 1:], eggnog - size, current_size + 1))
		elif size == eggnog:
			combination_sizes.add(current_size + 1)
	return combination_sizes

def silver(input_lines):
	container_sizes = sorted(Util.input.ParseInputLines(input_lines, _parseLine), reverse=True)
	combinations = _fit_containers(container_sizes, 150, 0)
	return sum(combinations.values())

def gold(input_lines):
	container_sizes = sorted(Util.input.ParseInputLines(input_lines, _parseLine), reverse=True)
	combinations = _fit_containers(container_sizes, 150, 0)
	return combinations[min(combinations.keys())]
