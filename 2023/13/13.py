input_lines = []
with open('input.txt', 'r') as input_file:
	for line in input_file:
		input_lines.append(line.removesuffix('\n'))

# Parse input
patterns = []
pattern = []
for i in input_lines:
	if i == '':
		patterns.append(pattern)
		pattern = []
	else:
		pattern.append(i)
patterns.append(pattern)

def IsVerticalSplit(pattern, vertical_split):
	mirror_length = min(len(pattern[0]) - vertical_split, vertical_split)
	for line in pattern:
		if line[vertical_split - mirror_length : vertical_split][::-1] != line[vertical_split : vertical_split + mirror_length]:
			return False
	return True

def IsHorizontalSplit(pattern, horizontal_split):
	# print(horizontal_split)
	mirror_length = min(len(pattern) - horizontal_split, horizontal_split)
	for index in range(mirror_length):
		# print(pattern[horizontal_split - 1 - index], pattern[horizontal_split + index])
		if pattern[horizontal_split - 1 - index] != pattern[horizontal_split + index]:
			return False
	return True

# Silver star
score = 0
for pattern in patterns:
	pattern_score = 0
	for vertical_split in range(1, len(pattern[0])):
		if IsVerticalSplit(pattern, vertical_split):
			pattern_score += vertical_split
	for horizontal_split in range(1, len(pattern)):
		if IsHorizontalSplit(pattern, horizontal_split):
			pattern_score += (100 * horizontal_split)
	score += pattern_score

print('Silver answer: ' + str(score))

# Gold star

def IsVerticalSplitSmudge(pattern, vertical_split):
	mirror_length = min(len(pattern[0]) - vertical_split, vertical_split)
	differences = 0
	for line in pattern:
		left = [char for char in line[vertical_split - mirror_length : vertical_split][::-1]]
		right = [char for char in line[vertical_split : vertical_split + mirror_length]]
		differences += sum([pair[0] != pair[1] for pair in zip(left, right)])
	return differences == 1

def IsHorizontalSplitSmudge(pattern, horizontal_split):
	mirror_length = min(len(pattern) - horizontal_split, horizontal_split)
	differences = 0
	for index in range(mirror_length):
		left = [char for char in pattern[horizontal_split - 1 - index]]
		right = [char for char in pattern[horizontal_split + index]]
		differences += sum([pair[0] != pair[1] for pair in zip(left, right)])
	return differences == 1

score = 0
for pattern in patterns:
	# for i, line in enumerate(pattern):
		# print(f"{i:2}: {line}")
	pattern_score = 0
	for vertical_split in range(1, len(pattern[0])):
		if IsVerticalSplitSmudge(pattern, vertical_split):
			# print("vertical_split", vertical_split)
			pattern_score += vertical_split
	for horizontal_split in range(1, len(pattern)):
		if IsHorizontalSplitSmudge(pattern, horizontal_split):
			# print("horizontal_split", horizontal_split)
			pattern_score += (100 * horizontal_split)
	score += pattern_score

print('Gold answer: ' + str(score))
