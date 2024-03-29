import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(line):
	return {'map': [char for char in line.split(' ')[0]], 'corrupt': [int(j) for j in line.split(' ')[1].split(',')]}

def _isCorruptionFit(current_map, start_index, corruption_length):
	if start_index + corruption_length > len(current_map):
		return False
	return all([i == '?' or i == '#' for i in current_map[start_index : start_index + corruption_length]])

def _fillCoruptSlot(current_map, start_index, corruptions, coruption_index, memoization):
	if (''.join(current_map[start_index:]), coruption_index) in memoization:
		return memoization[(''.join(current_map[start_index:]), coruption_index)]
	result = 0
	for i in range(start_index, len(current_map)):
		if (current_map[i] == '#' or current_map[i] == '?') and _isCorruptionFit(current_map, i, corruptions[coruption_index]):
			if coruption_index == len(corruptions) - 1:
				if all([j == '.' or j == '?' for j in current_map[i + corruptions[coruption_index]:]]):
					result += 1
			elif i + corruptions[coruption_index] + 1 < len(current_map) and current_map[i + corruptions[coruption_index]] != '#':
				next_map = current_map[:]
				for j in range(start_index, i):
					next_map[j] = '.'
				for j in range(i, i + corruptions[coruption_index]):
					next_map[j] = '#'
				next_map[i + corruptions[coruption_index]] = '.'
				result += _fillCoruptSlot(next_map, i + corruptions[coruption_index] + 1, corruptions, coruption_index + 1, memoization)
		if current_map[i] == '#':
			break
	memoization[(''.join(current_map[start_index:]), coruption_index)] = result
	return result

def _calculateCorruption(springs):
	grand_sum = 0
	for spring in springs:
		grand_sum += _fillCoruptSlot(spring['map'], 0, spring['corrupt'], 0, {})
	return grand_sum	

def silver(input_lines):
	springs = Util.input.ParseInputLines(input_lines, _parse)
	return _calculateCorruption(springs)

def gold(input_lines):
	springs = Util.input.ParseInputLines(input_lines, _parse)
	springs = [{'map': (i['map'] + ['?']) * 4 + i['map'], 'corrupt': i['corrupt'] * 5} for i in springs]
	return _calculateCorruption(springs)
