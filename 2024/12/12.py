import Util.input
import Util.directions
from collections import deque
from functools import cmp_to_key

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def bfs(start, grid):
	matching_id = Util.directions.Get(grid, start)
	next_locations = deque([start])
	visited = set()
	while len(next_locations) != 0:
		current_location = next_locations.pop()
		if current_location in visited:
			continue
		visited.add(current_location)
		for direction in Util.directions.DirectionsTable:
			new_location = Util.directions.Move(current_location, direction)
			if Util.directions.IsOutOfBounds(grid, new_location):
				continue
			if Util.directions.Get(grid, new_location) != matching_id:
				continue
			next_locations.appendleft(new_location)
	return visited

def _calculate_price(farm_plot):
	perimeter = 0
	for tile in farm_plot:
		for direction in Util.directions.DirectionsTable:
			touching_tile = Util.directions.Move(tile, direction)
			if touching_tile not in farm_plot:
				perimeter += 1
	area = len(farm_plot)
	return perimeter * area

def _calculate_price_gold(farm_plot):
	# Get all perimeter tiles with their coresponding directions (a tile can stand in for up to 4 perimeter tiles)
	perimeter_tiles = {i: [] for i in Util.directions.DirectionsTable}
	for tile in farm_plot:
		for direction in Util.directions.DirectionsTable:
			touching_tile = Util.directions.Move(tile, direction)
			if touching_tile not in farm_plot:
				perimeter_tiles[direction].append(tile)

	# Sort all perimeter tiles according to their direction and relevant coordinate
	# Then all matching sides will only have one significant coordinate as their difference
	perimeter_tiles['U'].sort(key=cmp_to_key(lambda l, r: (l[0] - r[0]) * 1000 + l[1] - r[1]))
	perimeter_tiles['D'].sort(key=cmp_to_key(lambda l, r: (l[0] - r[0]) * 1000 + l[1] - r[1]))
	perimeter_tiles['L'].sort(key=cmp_to_key(lambda l, r: (l[1] - r[1]) * 1000 + l[0] - r[0]))
	perimeter_tiles['R'].sort(key=cmp_to_key(lambda l, r: (l[1] - r[1]) * 1000 + l[0] - r[0]))
	sides = 0
	for direction in perimeter_tiles:
		last = (-1, -1)
		for tile in perimeter_tiles[direction]:
			if direction == 'U' or direction == 'D':
				if not (last[0] == tile[0] and last[1] + 1 == tile[1]):
					sides += 1
			if direction == 'L' or direction == 'R':
				if not (last[0] + 1 == tile[0] and last[1] == tile[1]):
					sides += 1
			last = tile

	area = len(farm_plot)
	return sides * area

def _mark_visited(farm_plot, visited_grid):
	for tile in farm_plot:
		Util.directions.Set(visited_grid, tile, 'X')

def _solution(input_lines, calculate_price_function):
	visited_grid = [['.' for i in input_lines[0]] for j in input_lines]
	price = 0
	for line_num in range(len(input_lines)):
		for col_num in range(len(input_lines[line_num])):
			start_location = (line_num, col_num)
			if Util.directions.Get(visited_grid, start_location) == '.':
				farm_plot = bfs(start_location, input_lines)
				price += calculate_price_function(farm_plot)
				_mark_visited(farm_plot, visited_grid)
	return price

def silver(input_lines):
	return _solution(input_lines, _calculate_price)

def gold(input_lines):
	return _solution(input_lines, _calculate_price_gold)
