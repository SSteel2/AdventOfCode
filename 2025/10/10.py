import Util.input
import itertools
import math
import Util.Frequency

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(line):
	parts = line.split(' ')
	target = [1 if i == '#' else 0 for i in parts[0][1:-1]]
	buttons = [[int(j) for j in i[1:-1].split(',')] for i in parts[1:-1]]
	joltage = [int(i) for i in parts[-1][1:-1].split(',')]
	return target, buttons, joltage

def silver(input_lines):
	problems = Util.input.ParseInputLines(input_lines, _parse)
	total_result = 0
	for problem in problems:
		target, buttons, _ = problem
		min_presses = math.inf
		is_correct = False
		for presses in range(len(buttons)):
			for combination in itertools.combinations(buttons, presses):
				result = [i for i in target]
				for button in combination:
					for position in button:
						result[position] += 1
				is_correct = all(i % 2 == 0 for i in result)
				if is_correct:
					break
			if is_correct:
				min_presses = presses
				break
		total_result += min_presses
	return total_result


def gold(input_lines):
	problems = Util.input.ParseInputLines(input_lines, _parse)
	total_result = 0
	for index, problem in enumerate(problems):
		_, buttons, joltage = problem
		# f = Util.Frequency.Frequency()
		# for button in buttons:
		# 	for i in button:
		# 		f.add(i)
		# print(joltage)
		# print(buttons)
		# print(f)
		# print(f'{index}: {len(joltage) - len(buttons)} {len(joltage)}, {len(buttons)}')
