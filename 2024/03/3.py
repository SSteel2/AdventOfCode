import Util.input
import re

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def silver(input_lines):
	line = ''.join(input_lines)
	matches = re.finditer('mul\\((\\d+),(\\d+)\\)', line)
	instructions = 0
	for match in matches:
		instructions += int(match.group(1)) * int(match.group(2))
	return instructions

def gold(input_lines):
	line = ''.join(input_lines)
	matches = re.finditer("mul\\((\\d+),(\\d+)\\)|do\\(\\)|don't\\(\\)", line)
	instructions = 0
	enabled = True
	for match in matches:
		if match.group(0) == 'do()':
			enabled = True
		elif match.group(0) == "don't()":
			enabled = False
		elif enabled:
			instructions += int(match.group(1)) * int(match.group(2))
	return instructions
