import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(line):
	return [int(i) for i in line]

def _solve(banks, battery_count):
	total_result = 0
	for bank in banks:
		batteries = [0] * battery_count
		current_index = 0
		for battery_index in range(battery_count):
			current_max = 0
			new_index = 0
			for i in range(current_index, len(bank) - battery_count + 1 + battery_index):
				if bank[i] > current_max:
					current_max = bank[i]
					new_index = i
			current_index = new_index + 1
			batteries[battery_index] = current_max
		result = 0
		for battery in batteries:
			result = result * 10 + battery
		total_result += result
	return total_result

def silver(input_lines):
	banks = Util.input.ParseInputLines(input_lines, _parse)
	return _solve(banks, 2)

def gold(input_lines):
	banks = Util.input.ParseInputLines(input_lines, _parse)
	return _solve(banks, 12)
