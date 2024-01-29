import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _groupCalories(input_lines):
	groups = []
	current_group = []
	for i in input_lines:
		if i == "":
			groups.append(current_group)
			current_group = []
			continue
		current_group.append(int(i))
	groups.append(current_group)
	return groups

def silver(input_lines):
	calorie_groups = _groupCalories(input_lines)
	max_sum = 0
	for group in calorie_groups:
		current_sum = sum(group)
		if current_sum > max_sum:
			max_sum = current_sum
	return max_sum

def gold(input_lines):
	calorie_groups = _groupCalories(input_lines)
	max_sums = [0, 0, 0]
	for group in calorie_groups:
		current_sum = sum(group)
		if current_sum > max_sums[0]:
			max_sums[2] = max_sums[1]
			max_sums[1] = max_sums[0]
			max_sums[0] = current_sum
		elif current_sum > max_sums[1]:
			max_sums[2] = max_sums[1]
			max_sums[1] = current_sum
		elif current_sum > max_sums[2]:
			max_sums[2] = current_sum
	return sum(max_sums)
