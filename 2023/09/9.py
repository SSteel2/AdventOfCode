import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def silver(input_lines):
	readings = [[int(j) for j in i.split(' ')] for i in input_lines]
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
	return sum(predictions)

def gold(input_lines):
	readings = [[int(j) for j in i.split(' ')] for i in input_lines]
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
	return sum(predictions)
