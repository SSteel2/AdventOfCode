import re

input_lines = []
with open('input.txt', 'r') as input_file:
	for line in input_file:
		input_lines.append(line)
total_lines = len(input_lines)
line_length = len(input_lines[0])

def isAdjacentSymbol(line, col, length):
	start_line = max(line - 1, 0)
	end_line = min(line + 1, total_lines - 1)
	start_col = max(col - 1, 0)
	end_col = min(col + length, line_length - 2)
	for i in range(start_line, end_line + 1):
		for j in range(start_col, end_col + 1):
			if input_lines[i][j] != '.' and not input_lines[i][j].isdigit():
				return True
	return False

def AdjacentGearPosition(line, col, length):
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
parts_sum = 0
all_matching = []
for i, line in enumerate(input_lines):
	matches = re.finditer('\\d+', line)
	for match in matches:
		if isAdjacentSymbol(i, match.start(), len(match[0])):
			all_matching.append(int(match[0]))
			#print(match)
			parts_sum += int(match[0])

print('Silver answer: ' + str(parts_sum))

# Gold star
gear_ratio_sum = 0
gear_candidates = {}
for i, line in enumerate(input_lines):
	matches = re.finditer('\\d+', line)
	for match in matches:
		position = AdjacentGearPosition(i, match.start(), len(match[0]))
		if position:
			if position in gear_candidates:
				gear_candidates[position].append(int(match[0]))
			else:
				gear_candidates[position] = [int(match[0])]


for gear_position in gear_candidates:
	if len(gear_candidates[gear_position]) == 2:
		gear_ratio_sum += (gear_candidates[gear_position][0] * gear_candidates[gear_position][1])

print('Gold answer: ' + str(gear_ratio_sum))
