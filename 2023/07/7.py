import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def GetTypeFromSortedFrequencies(sorted_frequencies):
	if sorted_frequencies[0] == 5:
		return 7
	elif sorted_frequencies[0] == 4:
		return 6
	elif sorted_frequencies[0] == 3 and sorted_frequencies[1] == 2:
		return 5
	elif sorted_frequencies[0] == 3:
		return 4
	elif sorted_frequencies[0] == 2 and sorted_frequencies[1] == 2:
		return 3
	elif sorted_frequencies[0] == 2:
		return 2
	else:
		return 1

def GetType(cards):
	frequencies = {}
	for i in cards:
		if i in frequencies:
			frequencies[i] += 1
		else:
			frequencies[i] = 1
	sorted_values = sorted(frequencies.values(), reverse=True)
	return GetTypeFromSortedFrequencies(sorted_values)

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

def GetRawValue(cards, value_table):
	value = 0
	for index, card in enumerate(cards):
		value += value_table[card] * (15 ** (4 - index))
	return value

def silver(input_lines):
	cards = [{'cards': i.split(' ')[0], 'bid': int(i.split(' ')[1])} for i in input_lines]
	for i in cards:
		i['type'] = GetType(i['cards'])
		i['value'] = GetRawValue(i['cards'], order_value)

	cards.sort(key=lambda x : x['value'])
	cards.sort(key=lambda x : x['type'])

	result = 0
	for i, card in enumerate(cards):
		result += card['bid'] * (i + 1)
	return result

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
	return GetTypeFromSortedFrequencies(sorted_values)

def gold(input_lines):
	cards = [{'cards': i.split(' ')[0], 'bid': int(i.split(' ')[1])} for i in input_lines]
	for i in cards:
		i['type'] = GetTypeJokers(i['cards'])
		i['value'] = GetRawValue(i['cards'], order_value_jokers)

	cards.sort(key=lambda x : x['value'])
	cards.sort(key=lambda x : x['type'])

	result = 0
	for i, card in enumerate(cards):
		result += card['bid'] * (i + 1)
	return result
