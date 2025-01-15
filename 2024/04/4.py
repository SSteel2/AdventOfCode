import Util.input
import Util.directions

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _pad_table(input_lines, count):
	padded_table = [['.' for i in range(len(input_lines[0]) + count * 2)] for j in range(len(input_lines) + count * 2)]
	for line_num, line in enumerate(input_lines):
		for col_num, col in enumerate(line):
			padded_table[line_num + count][col_num + count] = col
	return padded_table

def _find_xmas(grid, line, col):
	if Util.directions.Get(grid, (line, col)) != 'X':
		return 0
	found_xmas = 8
	for direction in Util.directions.DirectionsTableDiagonals:
		current_location = (line, col)
		for i in 'MAS':
			current_location = Util.directions.Move(current_location, direction)
			if i != Util.directions.Get(grid, current_location):
				found_xmas -= 1
				break
	return found_xmas

MAS_Inverse = {'M': 'S', 'S': 'M'}

def _find_x_mas(grid, line, col):
	center = (line, col)
	if Util.directions.Get(grid, center) != 'A':
		return 0
	letter_UR = Util.directions.Get(grid, Util.directions.Move(center, 'UR'))
	letter_DR = Util.directions.Get(grid, Util.directions.Move(center, 'DR'))
	letter_UL = Util.directions.Get(grid, Util.directions.Move(center, 'UL'))
	letter_DL = Util.directions.Get(grid, Util.directions.Move(center, 'DL'))
	if letter_UR in MAS_Inverse and letter_DL in MAS_Inverse and letter_UR == MAS_Inverse[letter_DL]:
		if letter_DR in MAS_Inverse and letter_UL in MAS_Inverse and letter_DR == MAS_Inverse[letter_UL]:
			return 1
	return 0

def _search_table(input_lines, pad_count, find_function):
	padded_table = _pad_table(input_lines, pad_count)
	found_xmas = 0
	for line_num in range(pad_count, len(input_lines) + pad_count):
		for col_num in range(pad_count, len(input_lines[line_num - pad_count]) + pad_count):
			found_xmas += find_function(padded_table, line_num, col_num)
	return found_xmas

def silver(input_lines):
	return _search_table(input_lines, 3, _find_xmas)

def gold(input_lines):
	return _search_table(input_lines, 1, _find_x_mas)
