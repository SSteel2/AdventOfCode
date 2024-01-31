import Util.input
import Util.ranges

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parseLine(line):
	spans = line.split(',')
	span_left = spans[0].split('-')
	span_right = spans[1].split('-')
	return (Util.ranges.Span(int(span_left[0]), int(span_left[1]) + 1), Util.ranges.Span(int(span_right[0]), int(span_right[1]) + 1))

def silver(input_lines):
	parsed = Util.input.ParseInputLines(input_lines, _parseLine)
	score = 0
	for line in parsed:
		result = line[0].union(line[1])
		if len(result) == 1 and len(result[0]) == max(len(line[0]), len(line[1])):
			score += 1
	return score

def gold(input_lines):
	parsed = Util.input.ParseInputLines(input_lines, _parseLine)
	score = 0
	for line in parsed:
		if line[0].isIntersecting(line[1]):
			score += 1
	return score
