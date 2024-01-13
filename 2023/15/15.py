import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _getHash(value):
	current_hash = 0
	for char in value:
		current_hash += ord(char)
		current_hash *= 17
		current_hash %= 256
	return current_hash

def silver(input_lines):
	chops = input_lines[0].split(',')
	total_hash = 0
	for chop in chops:
		total_hash += _getHash(chop)
	return total_hash

def _getLabelIndex(label, box):
	for i, lens in enumerate(box):
		if lens[0] == label:
			return i
	return -1

def gold(input_lines):
	chops = input_lines[0].split(',')
	boxes = [[] for _ in range(256)]
	for chop in chops:
		operation_index = chop.find('=')
		if operation_index == -1:
			label = chop[:-1]
			label_hash = _getHash(label)
			label_index = _getLabelIndex(label, boxes[label_hash])
			if label_index != -1:
				del boxes[label_hash][label_index]
		else:
			label = chop[:operation_index]
			lens_value = chop[operation_index + 1:]
			label_hash = _getHash(label)
			label_index = _getLabelIndex(label, boxes[label_hash])
			if label_index != -1:
				boxes[label_hash][label_index] = (label, lens_value)
			else:
				boxes[label_hash].append((label, lens_value))

	focus_power = 0
	box_number = 1
	for box in boxes:
		lens_number = 1
		for lens in box:
			focus_power += (box_number * lens_number * int(lens[1]))
			lens_number += 1
		box_number += 1
	return focus_power
