input_lines = []
with open('input.txt', 'r') as input_file:
	for line in input_file:
		input_lines.append(line.removesuffix('\n'))

# Parse input
springs = [{'map': i.split(' ')[0], 'corrupt': [int(j) for j in i.split(' ')[1].split(',')]} for i in input_lines]

# Silver star

def IsValid(current_map_string, corruptions):
	return [len(i) for i in ''.join(current_map_string).split('.') if i != ''] == corruptions

def IsCorruptionFit(current_map, start_index, corruption_length):
	if start_index + corruption_length > len(current_map):
		return False
	return all([i == '?' or i == '#' for i in current_map[start_index : start_index + corruption_length]])

memoization = {}
def FillCoruptSlot(current_map, start_index, corruptions, coruption_index):
	if (''.join(current_map[start_index:]), coruption_index) in memoization:
		return memoization[(''.join(current_map[start_index:]), coruption_index)]
	result = 0
	for i in range(start_index, len(current_map)):
		if (current_map[i] == '#' or current_map[i] == '?') and IsCorruptionFit(current_map, i, corruptions[coruption_index]):
			if coruption_index == len(corruptions) - 1:
				if all([j == '.' or j == '?' for j in current_map[i + corruptions[coruption_index]:]]):
					result += 1
			elif i + corruptions[coruption_index] + 1 < len(current_map) and current_map[i + corruptions[coruption_index]] != '#':
				# debug start
				next_map = current_map[:]
				for j in range(start_index, i):
					next_map[j] = '.'
				for j in range(i, i + corruptions[coruption_index]):
					next_map[j] = '#'
				next_map[i + corruptions[coruption_index]] = '.'
				# debug end
				result += FillCoruptSlot(next_map, i + corruptions[coruption_index] + 1, corruptions, coruption_index + 1)
		if current_map[i] == '#':
			break
	memoization[(''.join(current_map[start_index:]), coruption_index)] = result
	return result

grand_sum = 0
for spring in springs:
	current_map = [char for char in spring['map']]
	memoization = {}
	current_count = FillCoruptSlot(current_map, 0, spring['corrupt'], 0)
	grand_sum += current_count

print('Silver answer: ' + str(grand_sum))

# Gold star
grand_sum = 0
for index, spring in enumerate(springs):
	current_map = [char for char in spring['map']]
	current_map = (current_map + ['?']) * 4 + current_map
	corruptness = spring['corrupt'] * 5
	memoization = {}
	current_count = FillCoruptSlot(current_map, 0, corruptness, 0)
	grand_sum += current_count

print('Gold answer: ' + str(grand_sum))
