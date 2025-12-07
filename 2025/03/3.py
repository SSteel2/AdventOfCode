import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(line):
	return [int(i) for i in line]

def silver(input_lines):
	banks = Util.input.ParseInputLines(input_lines, _parse)
	result = 0
	for bank in banks:
		first_battery = 0
		second_battery = 0
		for i in range(len(bank) - 1):
			if bank[i] > first_battery:
				first_battery = bank[i]
				second_battery = 0
				for j in range(i + 1, len(bank)):
					if bank[j] > second_battery:
						second_battery = bank[j]
						if second_battery == 9:
							break
				if first_battery == 9:
					break
		result += first_battery * 10 + second_battery
	return result

def gold(input_lines):
	banks = Util.input.ParseInputLines(input_lines, _parse)
	total_result = 0
	for bank in banks:
		batteries = [0] * 12
		current_index = 0
		for battery_index in range(12):
			current_max = 0
			new_index = 0
			# print(current_index)
			for i in range(current_index, len(bank) - 11 + battery_index):
				if bank[i] > current_max:
					current_max = bank[i]
					new_index = i
			current_index = new_index + 1
			batteries[battery_index] = current_max
		result = 0
		for battery in batteries:
			result = result * 10 + battery
		total_result += result
		# print(result)
	return total_result