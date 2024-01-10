import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parseLine(line):
	split1 = line.split(': ')
	card_id = int(split1[0].split(' ')[-1])
	split2 = split1[1].split(' | ')
	winning_numbers = [int(i) for i in split2[0].split(' ') if i != '']
	selected_numbers = [int(i) for i in split2[1].split(' ') if i != '']
	return {'card': card_id, 'winning': winning_numbers, 'selected': selected_numbers}

def silver(input_lines):
	parsed = Util.input.ParseInputLines(input_lines, _parseLine)
	ticket_sum = 0
	for ticket in parsed:
		matching = len(set(ticket['selected']) & set(ticket['winning']))
		if matching == 0:
			continue
		else:
			ticket_sum += (2 ** (matching - 1))
	return ticket_sum

def gold(input_lines):
	parsed = Util.input.ParseInputLines(input_lines, _parseLine)
	match_table = {}
	ticket_table = {}
	for ticket in parsed:
		match_table[ticket['card']] = len(set(ticket['selected']) & set(ticket['winning']))
		ticket_table[ticket['card']] = 1

	for ticket in parsed:
		for i in range(1, match_table[ticket['card']] + 1):
			ticket_table[ticket['card'] + i] += ticket_table[ticket['card']]

	tickets_count = 0
	for ticket in parsed:
		tickets_count += ticket_table[ticket['card']]

	return tickets_count
