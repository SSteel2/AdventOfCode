import Util.input
import Util.directions

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def silver(input_lines):
	padded_table = Util.directions.PadTable(input_lines, 1, '.')
	_, paper_queue = _construct_neighbour_table(padded_table)
	return len(paper_queue)

def _construct_neighbour_table(table):
	current_table = [[-1 for _ in range(len(table[0]))] for _ in table]
	paper_queue = []
	for l, line in enumerate(table):
		for c, col in enumerate(line):
			if col == '@':
				adjacent_count = 0
				for d in Util.directions.DirectionsTableDiagonals:
					if Util.directions.Get(table, Util.directions.Move((l, c), d)) == '@':
						adjacent_count += 1
				Util.directions.Set(current_table, (l, c), adjacent_count)
				if adjacent_count < 4:
					paper_queue.append((l, c))
	return current_table, paper_queue

def gold(input_lines):
	padded_table = Util.directions.PadTable(input_lines, 1, -1)
	current_table, paper_queue = _construct_neighbour_table(padded_table)

	moveable_paper = 0
	while len(paper_queue) > 0:
		current_cell = paper_queue.pop()
		if Util.directions.Get(current_table, current_cell) == -1:
			continue
		Util.directions.Set(current_table, current_cell, -1)
		for d in Util.directions.DirectionsTableDiagonals:
			neighbour = Util.directions.Move(current_cell, d)
			neighbour_value = Util.directions.Get(current_table, neighbour)
			if neighbour_value == -1:
				continue
			Util.directions.Set(current_table, neighbour, neighbour_value - 1)
			if neighbour_value - 1 < 4:
				paper_queue.append(neighbour)
		moveable_paper += 1
	return moveable_paper
