from functools import reduce
import Util.input
import Util.math

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(input_lines):
	instructions = input_lines[0]
	roads = {i[0:3]: {'L': i[7:10], 'R': i[12:15]} for i in input_lines[2:]}
	return instructions, roads

def silver(input_lines):
	instructions, roads = _parse(input_lines)
	steps = 0
	current = 'AAA'
	while current != 'ZZZ':
		current = roads[current][instructions[steps % len(instructions)]]
		steps += 1
	return steps

def gold(input_lines):
	instructions, roads = _parse(input_lines)
	steps = []
	starts = [i for i in roads if i[2] == 'A']
	for start in starts:
		step_count = 0
		while start[-1] != 'Z':
			start = roads[start][instructions[step_count % len(instructions)]]
			step_count += 1
		steps.append(step_count)

	return reduce(Util.math.lcm, steps)
