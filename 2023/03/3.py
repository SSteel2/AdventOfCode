import re
import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _isAdjacentSymbol(input_lines, line, col, length, total_lines, line_length):
	start_line = max(line - 1, 0)
	end_line = min(line + 1, total_lines - 1)
	start_col = max(col - 1, 0)
	end_col = min(col + length, line_length - 2)
	for i in range(start_line, end_line + 1):
		for j in range(start_col, end_col + 1):
			if input_lines[i][j] != '.' and not input_lines[i][j].isdigit():
				return True
	return False

def _getAdjacentGearPosition(input_lines, line, col, length, total_lines, line_length):
	start_line = max(line - 1, 0)
	end_line = min(line + 1, total_lines - 1)
	start_col = max(col - 1, 0)
	end_col = min(col + length, line_length - 2)
	for i in range(start_line, end_line + 1):
		for j in range(start_col, end_col + 1):
			if input_lines[i][j] == '*':
				return (i, j)
	return None

# Silver star
def silver(input_lines):
	total_lines = len(input_lines)
	line_length = len(input_lines[0])
	parts_sum = 0
	all_matching = []
	for i, line in enumerate(input_lines):
		matches = re.finditer('\\d+', line)
		for match in matches:
			if _isAdjacentSymbol(input_lines, i, match.start(), len(match[0]), total_lines, line_length):
				all_matching.append(int(match[0]))
				parts_sum += int(match[0])
	return parts_sum

# Gold star
def gold(input_lines):
	total_lines = len(input_lines)
	line_length = len(input_lines[0])
	gear_ratio_sum = 0
	gear_candidates = {}
	for i, line in enumerate(input_lines):
		matches = re.finditer('\\d+', line)
		for match in matches:
			position = _getAdjacentGearPosition(input_lines, i, match.start(), len(match[0]), total_lines, line_length)
			if position:
				if position in gear_candidates:
					gear_candidates[position].append(int(match[0]))
				else:
					gear_candidates[position] = [int(match[0])]

	for gear_position in gear_candidates:
		if len(gear_candidates[gear_position]) == 2:
			gear_ratio_sum += (gear_candidates[gear_position][0] * gear_candidates[gear_position][1])

	return gear_ratio_sum
