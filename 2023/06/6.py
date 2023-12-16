input_lines = []
with open('input_gold.txt', 'r') as input_file:
	for line in input_file:
		input_lines.append(line.removesuffix('\n'))

# Parse input
times = [i for i in input_lines[0].split(' ') if i != ''][1:]
distances = [i for i in input_lines[1].split(' ') if i != ''][1:]
games = [{'time': int(i[0]), 'distance': int(i[1])} for i in zip(times, distances)]

# Silver star
answers = []
for game in games:
	answer = 0
	for i in range(game['time']):
		if i * (game['time'] - i) > game['distance']:
			answer += 1
	answers.append(answer)

product = 1
for i in answers:
	product *= i

print('Silver answer: ' + str(product))

# Gold star
#print('Gold answer: ' + str(current_location_ranges[0].start))
