import time

input_lines = []
with open('input.txt', 'r') as input_file:
	for line in input_file:
		input_lines.append(line.removesuffix('\n'))

# Parse input
chart = [[char for char in line] for line in input_lines]

# Silver star
def FindEmptyNorth(l, c):
	result = l
	for i in range(l - 1, -1, -1):
		if chart[i][c] == '.':
			result = i
		else:
			break
	return result

def MoveNorth(l, c):
	if l == 0:
		return
	new_line = FindEmptyNorth(l, c)
	if new_line != l:
		chart[new_line][c] = 'O'
		chart[l][c] = '.'

def MoveNorthAll():
	for i, line in enumerate(chart):
		for j, char in enumerate(line):
			if char == 'O':
				MoveNorth(i, j)

def CountScore():
	current_line_score = len(chart)
	total_score = 0
	for line in chart:
		for char in line:
			if char == 'O':
				total_score += current_line_score
		current_line_score -= 1
	return total_score

MoveNorthAll()

with open('output_silver.txt', 'w') as write_file:
	for line in chart:
		write_file.write(''.join(line))
		write_file.write('\n')



print('Silver answer: ' + str(CountScore()))
# Silver answer: 109466

# Gold star
chart = [[char for char in line] for line in input_lines]

def FindEmptyWest(l, c):
	result = c
	for i in range(c - 1, -1, -1):
		if chart[l][i] == '.':
			result = i
		else:
			break
	return result

def MoveWest(l, c):
	if c == 0:
		return
	new_col = FindEmptyWest(l, c)
	if new_col != c:
		chart[l][new_col] = 'O'
		chart[l][c] = '.'

def MoveWestAll():
	for i, line in enumerate(chart):
		for j, char in enumerate(line):
			if char == 'O':
				MoveWest(i, j)

def FindEmptySouth(l, c):
	result = l
	for i in range(l + 1, len(chart)):
		if chart[i][c] == '.':
			result = i
		else:
			break
	return result

def MoveSouth(l, c):
	if l == len(chart) - 1:
		return
	new_line = FindEmptySouth(l, c)
	if new_line != l:
		chart[new_line][c] = 'O'
		chart[l][c] = '.'

def MoveSouthAll():
	for i, line in list(enumerate(chart))[::-1]:
		for j, char in enumerate(line):
			if char == 'O':
				MoveSouth(i, j)

def FindEmptyEast(l, c):
	result = c
	for i in range(c + 1, len(chart[0])):
		if chart[l][i] == '.':
			result = i
		else:
			break
	return result

def MoveEast(l, c):
	if c == len(chart[0]):
		return
	new_col = FindEmptyEast(l, c)
	if new_col != c:
		chart[l][new_col] = 'O'
		chart[l][c] = '.'
	return chart

def MoveEastAll():
	for i, line in enumerate(chart):
		for j, char in list(enumerate(line))[::-1]:
			if char == 'O':
				MoveEast(i, j)

scores = {}
scores_list = []
start = time.time()
for i in range(10000):
	MoveNorthAll()
	MoveWestAll()
	MoveSouthAll()
	MoveEastAll()
	if i % 100 == 0:
		print(i)
	score = CountScore()
	scores_list.append(score)
	if score in scores:
		scores[score] += 1
	else:
		scores[score] = 1
end = time.time()

with open('output.txt', 'w') as write_file:
	for line in chart:
		write_file.write(''.join(line))
		write_file.write('\n')

print('Gold answer: ' + str(CountScore()))

print(f'Elasped time: {end - start:.2}')

# best guess gold
for i in sorted(list(scores.items()), key=lambda x: x[1], reverse=True):
	print(f'{i[0]:4}: {i[1]}')

print('Last 10 scores', scores_list[-10:])