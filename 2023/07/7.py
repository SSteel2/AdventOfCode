input_lines = []
with open('input.txt', 'r') as input_file:
	for line in input_file:
		input_lines.append(line.removesuffix('\n'))

# Parse input
cards = [{'cards': i.split(' ')[0], 'bid': int(i.split(' ')[1])} for i in input_lines]

# Silver star
def GetType(cards):
	frequencies = {}
	for i in cards:
		if i in frequencies:
			frequencies[i] += 1
		else:
			frequencies[i] = 1
	sorted_values = sorted(frequencies.values(), reverse=True)
	if sorted_values[0] == 5:
		return 7
	elif sorted_values[0] == 4:
		return 6
	elif sorted_values[0] == 3 and sorted_values[1] == 2:
		return 5
	elif sorted_values[0] == 3:
		return 4
	elif sorted_values[0] == 2 and sorted_values[1] == 2:
		return 3
	elif sorted_values[0] == 2:
		return 2
	else:
		return 1

order_value = {
	'2': 1,
	'3': 2,
	'4': 3,
	'5': 4,
	'6': 5,
	'7': 6,
	'8': 7,
	'9': 8,
	'T': 9,
	'J': 10,
	'Q': 11,
	'K': 12,
	'A': 13
}

def GetRawValue(cards):
	value = 0
	for index, card in enumerate(cards):
		value += order_value[card] * (15 ** (4 - index))
	return value

for i in cards:
	i['type'] = GetType(i['cards'])
	i['value'] = GetRawValue(i['cards'])

cards.sort(key=lambda x : x['value'])
cards.sort(key=lambda x : x['type'])

result = 0
for i, card in enumerate(cards):
	result += card['bid'] * (i + 1)

print('Silver answer: ' + str(result))

# Gold star

# Parse input
cardsJokers = [{'cards': i.split(' ')[0], 'bid': int(i.split(' ')[1])} for i in input_lines]

order_value_jokers = {
	'J': 1,
	'2': 2,
	'3': 3,
	'4': 4,
	'5': 5,
	'6': 6,
	'7': 7,
	'8': 8,
	'9': 9,
	'T': 10,
	'Q': 11,
	'K': 12,
	'A': 13
}

def GetRawValueJokers(cards):
	value = 0
	for index, card in enumerate(cards):
		value += order_value_jokers[card] * (15 ** (4 - index))
	return value

def GetTypeJokers(cards):
	frequencies = {}
	joker_count = 0
	for i in cards:
		if i == 'J':
			joker_count += 1
			continue
		if i in frequencies:
			frequencies[i] += 1
		else:
			frequencies[i] = 1
	sorted_values = sorted(frequencies.values(), reverse=True)
	if len(sorted_values) == 0:
		sorted_values = [0]
	sorted_values[0] += joker_count
	if sorted_values[0] == 5:
		return 7
	elif sorted_values[0] == 4:
		return 6
	elif sorted_values[0] == 3 and sorted_values[1] == 2:
		return 5
	elif sorted_values[0] == 3:
		return 4
	elif sorted_values[0] == 2 and sorted_values[1] == 2:
		return 3
	elif sorted_values[0] == 2:
		return 2
	else:
		return 1

for i in cards:
	i['type'] = GetTypeJokers(i['cards'])
	i['value'] = GetRawValueJokers(i['cards'])

cards.sort(key=lambda x : x['value'])
cards.sort(key=lambda x : x['type'])

resultJokers = 0
for i, card in enumerate(cards):
	resultJokers += card['bid'] * (i + 1)

print('Gold answer: ' + str(resultJokers))
