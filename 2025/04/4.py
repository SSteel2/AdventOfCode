import Util.input
import Util.directions
import copy

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def silver(input_lines):
	padded_table = Util.directions.PadTable(input_lines, 1, '.')
	moveable_paper = 0
	for l, line in enumerate(padded_table):
		for c, col in enumerate(line):
			if col == '@':
				adjacent_count = 0
				for d in Util.directions.DirectionsTableDiagonals:
					if Util.directions.Get(padded_table, Util.directions.Move((l, c), d)) == '@':
						adjacent_count += 1
				if adjacent_count < 4:
					moveable_paper += 1
	return moveable_paper

def gold(input_lines):
	# padaryti, kad tikrintų, tik šalia prieš
	current_table = Util.directions.PadTable(input_lines, 1, '.')
	moveable_paper = 0
	last_iteration_paper = -1
	while last_iteration_paper < moveable_paper:
		# patikrinti, ar čia greičiau už list comprehension
		next_table = copy.deepcopy(current_table)
		last_iteration_paper = moveable_paper
		for l, line in enumerate(current_table):
			for c, col in enumerate(line):
				if col == '@':
					adjacent_count = 0
					for d in Util.directions.DirectionsTableDiagonals:
						if Util.directions.Get(current_table, Util.directions.Move((l, c), d)) == '@':
							adjacent_count += 1
					if adjacent_count < 4:
						Util.directions.Set(next_table, (l, c), '.')
						moveable_paper += 1
		current_table = next_table
	return moveable_paper