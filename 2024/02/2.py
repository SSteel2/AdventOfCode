import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(line):
	return [int(i) for i in line.split(' ')]

def is_safe(report):
	differences = [report[i + 1] - report[i] for i in range(len(report) - 1)]
	return all(i >= 1 and i <= 3 for i in differences) or all(i >= -3 and i <= -1 for i in differences)

def silver(input_lines):
	reports = Util.input.ParseInputLines(input_lines, _parse)
	safe = 0
	for i in reports:
		if is_safe(i):
			safe += 1
	return safe

def gold(input_lines):
	reports = Util.input.ParseInputLines(input_lines, _parse)
	safe = 0
	for i in reports:
		if is_safe(i):
			safe += 1
		else:
			for j in range(len(i)):
				if is_safe(i[:j] + i[j + 1:]):
					safe += 1
					break
	return safe
