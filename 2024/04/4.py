import Util.input
import Util.directions

DirectionsTable8 = {
	'U': (-1, 0),
	'UR': (-1, 1),
	'R': (0, 1),
	'DR': (1, 1),
	'D': (1, 0),
	'DL': (1, -1),
	'L': (0, -1),
	'UL': (-1, -1)
}

DirectionsExtentsTable8 = {
	'U': (-3, 0),
	'UR': (-3, 3),
	'R': (0, 3),
	'DR': (3, 3),
	'D': (3, 0),
	'DL': (3, -3),
	'L': (0, -3),
	'UL': (-3, -3)
}
def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _find_xmas(input_lines, line, col, direction):
	current_location = (line, col)
	if Util.directions.Get(input_lines, current_location) != 'X':
		return False
	max_location = Util.directions.MoveCustom(current_location, DirectionsExtentsTable8[direction])
	if max_location[0] >= len(input_lines) or max_location[0] < 0 or max_location[1] >= len(input_lines[0]) or max_location[1] < 0:
		return False
	for i in 'MAS':
		current_location = Util.directions.MoveCustom(current_location, DirectionsTable8[direction])
		if i != Util.directions.Get(input_lines, current_location):
			return False
	return True

MAS_Inverse = {'M': 'S', 'S': 'M'}

def _find_x_mas(input_lines, line, col):
	if line >= len(input_lines) - 1 or line < 1 or col >= len(input_lines[0]) - 1 or col < 1:
		return False
	center_location = (line, col)
	if Util.directions.Get(input_lines, center_location) != 'A':
		return False
	letter_UR = Util.directions.Get(input_lines, Util.directions.MoveCustom(center_location, DirectionsTable8['UR']))
	letter_DR = Util.directions.Get(input_lines, Util.directions.MoveCustom(center_location, DirectionsTable8['DR']))
	letter_UL = Util.directions.Get(input_lines, Util.directions.MoveCustom(center_location, DirectionsTable8['UL']))
	letter_DL = Util.directions.Get(input_lines, Util.directions.MoveCustom(center_location, DirectionsTable8['DL']))
	if letter_UR in MAS_Inverse and letter_DL in MAS_Inverse and letter_UR == MAS_Inverse[letter_DL]:
		if letter_DR in MAS_Inverse and letter_UL in MAS_Inverse and letter_DR == MAS_Inverse[letter_UL]:
			return True
	return False

def silver(input_lines):
	found_xmas = 0
	for line_num, line in enumerate(input_lines):
		for col_num, col in enumerate(line):
			for direction in DirectionsTable8:
				if _find_xmas(input_lines, line_num, col_num, direction):
					found_xmas += 1
	return found_xmas

def gold(input_lines):
	found_xmas = 0
	for line_num, line in enumerate(input_lines):
		for col_num, col in enumerate(line):
			if _find_x_mas(input_lines, line_num, col_num):
				found_xmas += 1
	return found_xmas
