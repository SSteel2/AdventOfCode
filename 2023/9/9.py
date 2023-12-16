input_lines = []
with open('input.txt', 'r') as input_file:
	for line in input_file:
		input_lines.append(line.removesuffix('\n'))

# Parse input
readings = [[int(j) for j in i.split(' ')] for i in input_lines]

# Silver star
predictions = []
for reading in readings:
	current_reading = [reading[:]]
	while not all(i == 0 for i in current_reading[-1]) and len(current_reading[-1]) > 1:
		next_line = []
		for i in range(len(current_reading[-1]) - 1):
			next_line.append(current_reading[-1][i + 1] - current_reading[-1][i])
		current_reading.append(next_line)
	prediction = 0
	for i in current_reading:
		prediction += i[-1]
	predictions.append(prediction)

print('Silver answer: ' + str(sum(predictions)))

# Gold star
predictions = []
for reading in readings:
	current_reading = [reading[:]]
	while not all(i == 0 for i in current_reading[-1]) and len(current_reading[-1]) > 1:
		next_line = []
		for i in range(len(current_reading[-1]) - 1):
			next_line.append(current_reading[-1][i + 1] - current_reading[-1][i])
		current_reading.append(next_line)
	prediction = 0
	for i in current_reading[-2::-1]:
		prediction = i[0] - prediction
	predictions.append(prediction)

print('Gold answer: ' + str(sum(predictions)))
