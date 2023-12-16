input_lines = []
with open('input.txt', 'r') as input_file:
	for line in input_file:
		input_lines.append(line.removesuffix('\n'))

# Parse input
galaxy = [[j for j in i] for i in input_lines]
galaxy_gold = [[j for j in i] for i in input_lines]

# Silver star
# Expand galaxy
empty_cols = []
for i in range(len(galaxy[0])):
	if all(galaxy[j][i] == '.' for j in range(len(galaxy[0]))):
		empty_cols.append(i)
for empty_col in empty_cols[::-1]:
	for i in galaxy:
		i.insert(empty_col, '.')
empty_rows = []
for i, values in enumerate(galaxy):
	if all(j == '.' for j in values):
		empty_rows.append(i)
for empty_row in empty_rows[::-1]:
	galaxy.insert(empty_row, ['.' for i in range(len(galaxy[0]))])
with open('input_expanded.txt', 'w') as write_file:
	for line in galaxy:
		write_file.write(''.join(line))
		write_file.write('\n')

stars = []
for i, line in enumerate(galaxy):
	for j, val in enumerate(line):
		if val == '#':
			stars.append((i, j))

def distance(a, b):
	return abs(a[0] - b[0]) + abs(a[1] - b[1])

distance_sum = 0
for i in range(len(stars)):
	for j in range(i + 1, len(stars)):
		distance_sum += distance(stars[i], stars[j])

print('Silver answer: ' + str(distance_sum))

# Gold star
def distance_gold(a, b):
	distance = abs(a[0] - b[0]) + abs(a[1] - b[1])
	longs = len([i for i in empty_rows if i > min(a[0], b[0]) and i < max(a[0], b[0])]) + len([i for i in empty_cols if i > min(a[1], b[1]) and i < max(a[1], b[1])])
	return longs * 999999 + distance

stars_gold = []
for i, line in enumerate(galaxy_gold):
	for j, val in enumerate(line):
		if val == '#':
			stars_gold.append((i, j))

distance_gold_sum = 0
for i in range(len(stars_gold)):
	for j in range(i + 1, len(stars_gold)):
		distance_gold_sum += distance_gold(stars_gold[i], stars_gold[j])

print('Gold answer: ' + str(distance_gold_sum))
