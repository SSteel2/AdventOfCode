import Util.input
import Util.Frequency

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(line):
	return [int(i) for i in line.split('   ')]

def silver(input_lines):
	lines = Util.input.ParseInputLines(input_lines, _parse)
	lines = [sorted([i[j] for i in lines]) for j in range(len(lines[0]))]
	return sum(abs(lines[0][i] - lines[1][i]) for i in range(len(lines[0])))

def gold(input_lines):
	lines = Util.input.ParseInputLines(input_lines, _parse)
	locations = [i[0] for i in lines]
	frequency = Util.Frequency.Frequency()
	for i in lines:
		frequency.add(i[1])
	score = 0
	for i in locations:
		if i not in frequency:
			continue
		score += i * frequency[i]
	return score
