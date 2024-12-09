import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(input_lines):
	total_sum = 0
	for number in input_lines[0]:
		total_sum += int(number)
	filesystem = ['.' for i in range(total_sum)]
	current_index = 0
	empty_block = False
	current_id = 0
	for number in input_lines[0]:
		if empty_block:
			current_index += int(number)
		else:
			for i in range(int(number)):
				filesystem[current_index] = current_id
				current_index += 1
			current_id += 1
		empty_block = not empty_block
	return filesystem

def _calculate_checksum(filesystem):
	checksum = 0
	for index, value in enumerate(filesystem):
		if value != '.':
			checksum += (index * filesystem[index])
	return checksum

def silver(input_lines):
	filesystem = _parse(input_lines)
	back_index = len(filesystem) - 1
	for index, value in enumerate(filesystem):
		if index >= back_index:
			break
		if value == '.':
			filesystem[index], filesystem[back_index] = filesystem[back_index], '.'
			back_index -= 1
			while filesystem[back_index] == '.' and back_index > index:
				back_index -= 1
	return _calculate_checksum(filesystem)

def _find_first_empty(start_index, filesystem):
	for i in range(start_index, len(filesystem)):
		if filesystem[i] == '.':
			return i
	return len(filesystem)

def _create_id_index_map(filesystem):
	id_index_map = []
	current_id = filesystem[0]
	current_length = 1
	start_index = 0
	for index, i in enumerate(filesystem[1:]):
		if i != '.' and i != current_id:
			id_index_map.append((current_id, start_index, current_length))
			current_length = 1
			current_id = i
			start_index = index + 1
		elif i == current_id:
			current_length += 1
	id_index_map.append((i, start_index, current_length))
	return id_index_map

def _move_file(back_index, start_index, segment_length, filesystem):
	current_gap = 0
	current_index = start_index
	new_start = start_index
	while current_gap < segment_length:
		if filesystem[current_index] == '.':
			current_gap += 1
		elif filesystem[current_index] != '.':
			current_gap = 0
			new_start = current_index + 1
		current_index += 1
		if current_index > back_index:
			return
	moveable_id = filesystem[back_index]
	for i in range(segment_length):
		filesystem[new_start + i] = moveable_id
		filesystem[back_index + i] = '.'

def gold(input_lines):
	filesystem = _parse(input_lines)
	start_index = _find_first_empty(0, filesystem)
	id_index_map = _create_id_index_map(filesystem)
	for current_id, back_index, segment_length in id_index_map[::-1]:
		if back_index < start_index:
			break
		_move_file(back_index, start_index, segment_length, filesystem)
		start_index = _find_first_empty(start_index, filesystem)
	return _calculate_checksum(filesystem)
