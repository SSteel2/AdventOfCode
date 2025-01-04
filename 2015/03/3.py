import Util.input
import Util.directions

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

conversion_table = {
	'^': 'U',
	'>': 'R',
	'v': 'D',
	'<': 'L'
}

def _visit_houses(instructions):
	visited = set()
	current = (0, 0)
	visited.add(current)
	for instruction in instructions:
		current = Util.directions.Move(current, instruction)
		visited.add(current)
	return visited

def silver(input_lines):
	instructions = Util.directions.Convert(input_lines, conversion_table)[0]
	return len(_visit_houses(instructions))

def gold(input_lines):
	instructions = Util.directions.Convert(input_lines, conversion_table)[0]
	return len(_visit_houses(instructions[::2]).union(_visit_houses(instructions[1::2])))
