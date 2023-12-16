input_lines = []
with open('input.txt', 'r') as input_file:
	for line in input_file:
		input_lines.append(line.removesuffix('\n'))

# Parse input
chops = input_lines[0].split(',')

def GetHash(value):
	current_hash = 0
	for char in value:
		current_hash += ord(char)
		current_hash *= 17
		current_hash %= 256
	return current_hash

# Silver star
total_hash = 0
for chop in chops:
	total_hash += GetHash(chop)

print('Silver answer: ' + str(total_hash))

# Gold star

def GetLabelIndex(label, box):
	for i, lens in enumerate(box):
		if lens[0] == label:
			return i
	return -1

boxes = [[] for _ in range(256)]
for chop in chops:
	operation_index = chop.find('=')
	if operation_index == -1:
		label = chop[:-1]
		label_hash = GetHash(label)
		label_index = GetLabelIndex(label, boxes[label_hash])
		if label_index != -1:
			del boxes[label_hash][label_index]
	else:
		label = chop[:operation_index]
		lens_value = chop[operation_index + 1:]
		label_hash = GetHash(label)
		label_index = GetLabelIndex(label, boxes[label_hash])
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

print('Gold answer: ' + str(focus_power))

