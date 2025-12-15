import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(input_line):
	ranges = input_line.split(',')
	parsed = []
	for i in ranges:
		split_range = i.split('-')
		parsed.append((int(split_range[0]), int(split_range[1])))
	return parsed

def _normalize_ranges(ranges):
	new_ranges = []
	for i in ranges:
		digits_start = len(str(i[0]))
		digits_end = len(str(i[1]))
		if digits_start == digits_end:
			new_ranges.append(i)
		else:
			new_ranges.append((i[0], 10 ** digits_start - 1))
			new_ranges.append((10 ** digits_start, i[1]))
	return new_ranges

def _construct_multiple(number, helper, repetitions):
	result = number
	for i in range(repetitions - 1):
		result = result * helper + number
	return result

def _repetition_sum(start, end, digits, repetitions, used_ids):
	result = 0
	helper = 10 ** (digits // repetitions)
	start_sequence = start // (helper ** (repetitions - 1))
	end_sequence = end // (helper ** (repetitions - 1))
	for number in range(start_sequence, end_sequence + 1):
		current_id = _construct_multiple(number, helper, repetitions)
		if current_id < start or current_id in used_ids:
			continue
		if current_id > end:
			break
		result += current_id
		used_ids.add(current_id)
	return result

def _solve(ranges, max_repetitions):
	total_result = 0
	for i in ranges:
		digits = len(str(i[0]))
		used_ids = set()
		for repetitions in range(2, max_repetitions + 1):
			if digits % repetitions == 0:
				total_result += _repetition_sum(i[0], i[1], digits, repetitions, used_ids)
	return total_result	

def silver(input_lines):
	ranges = _normalize_ranges(_parse(input_lines[0]))
	return _solve(ranges, 2)

def gold(input_lines):
	ranges = _normalize_ranges(_parse(input_lines[0]))
	return _solve(ranges, 10)
