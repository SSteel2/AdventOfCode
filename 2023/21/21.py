import time

input_lines = []
with open('input.txt', 'r') as input_file:
	for line in input_file:
		input_lines.append(line.removesuffix('\n'))

# Parse input
start_position = None
for i, line in enumerate(input_lines):
	for j, col in enumerate(line):
		if col == 'S':
			start_position = (i, j)

directions_map = {
	'U': (-1, 0),
	'R': (0, 1),
	'D': (1, 0),
	'L': (0, -1)
}

# Silver star

def isValid(position):
	if position[0] >= len(input_lines) or position[0] < 0 or position[1] >= len(input_lines[0]) or position[1] < 0:
		return False
	if input_lines[position[0]][position[1]] == '#':
		return False
	return True

def bfs(queue, visited):
	new_queue = []
	for position in queue:
		for direction in directions_map:
			new_position = tuple(map(sum, zip(directions_map[direction], position)))
			if isValid(new_position) and new_position not in new_queue and new_position not in visited:
				new_queue.append(new_position)
	return new_queue

def CountSteps(start, steps):
	new_part = [(start)]
	queue_even = [(start)]
	queue_odd = []
	for i in range(steps):
		if i % 2 == 0:
			new_part = bfs(new_part, queue_odd)
			queue_odd.extend(new_part)
		else:
			new_part = bfs(new_part, queue_even)
			queue_even.extend(new_part)
	if steps % 2 == 0:
		return len(queue_even)
	else:
		return len(queue_odd)

print('Silver answer: ' + str(CountSteps(start_position, 64)))

# Gold star
even_count = CountSteps(start_position, 130) # even has (i + j) % 2 -> full
odd_count = CountSteps(start_position, 129)

total_steps = 26501365
board_length = len(input_lines)
half_length = board_length // 2
max_reach_in_spans = (total_steps - half_length) // board_length
leftover = total_steps - board_length * max_reach_in_spans - half_length  # literally 0
full_spans = max_reach_in_spans
if leftover < half_length:
	full_spans -= 1

big_span_count = (full_spans + 1) ** 2
small_span_count = full_spans ** 2
if full_spans % 2 == 0:
	odd_full_spans_count = small_span_count
	even_full_spans_count = big_span_count
else:
	odd_full_spans_count = big_span_count
	even_full_spans_count = small_span_count
	odd_count, even_count = even_count, odd_count

big_side_spans_count = full_spans
small_side_spans_count = full_spans + 1

steps_count_corner = board_length - 1
steps_count_small_side = steps_count_corner - half_length - 1
steps_count_big_side = steps_count_small_side + board_length

steps_count_corner_top = CountSteps((len(input_lines) - 1, start_position[1]), steps_count_corner)
steps_count_corner_bottom = CountSteps((0, start_position[1]), steps_count_corner)
steps_count_corner_right = CountSteps((start_position[0], 0), steps_count_corner)
steps_count_corner_left = CountSteps((start_position[0], len(input_lines[0]) - 1), steps_count_corner)

steps_count_small_side_topleft = CountSteps((len(input_lines) - 1, len(input_lines[0]) - 1), steps_count_small_side)
steps_count_small_side_topright = CountSteps((len(input_lines) - 1, 0), steps_count_small_side)
steps_count_small_side_bottomright = CountSteps((0, 0), steps_count_small_side)
steps_count_small_side_bottomleft = CountSteps((0, len(input_lines[0]) - 1), steps_count_small_side)

steps_count_big_side_topleft = CountSteps((len(input_lines) - 1, len(input_lines[0]) - 1), steps_count_big_side)
steps_count_big_side_topright = CountSteps((len(input_lines) - 1, 0), steps_count_big_side)
steps_count_big_side_bottomright = CountSteps((0, 0), steps_count_big_side)
steps_count_big_side_bottomleft = CountSteps((0, len(input_lines[0]) - 1), steps_count_big_side)

total_full = odd_full_spans_count * odd_count + even_full_spans_count * even_count
total_big_sides = (steps_count_big_side_topleft + steps_count_big_side_topright + steps_count_big_side_bottomright + steps_count_big_side_bottomleft) * big_side_spans_count
total_small_sides = (steps_count_small_side_topleft + steps_count_small_side_topright + steps_count_small_side_bottomright + steps_count_small_side_bottomleft) * small_side_spans_count
total_corners = steps_count_corner_top + steps_count_corner_bottom + steps_count_corner_left + steps_count_corner_right
total = total_full + total_big_sides + total_small_sides + total_corners
print('Gold answer: ' + str(total))
