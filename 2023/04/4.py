input_lines = []
with open('input.txt', 'r') as input_file:
	for line in input_file:
		input_lines.append(line)

def ParseInputLine(line):
	split1 = line.split(': ')
	card_id = int(split1[0].split(' ')[-1])
	split2 = split1[1].split(' | ')
	winning_numbers = [int(i) for i in split2[0].split(' ') if i != '']
	selected_numbers = [int(i) for i in split2[1].split(' ') if i != '']
	return {'card': card_id, 'winning': winning_numbers, 'selected': selected_numbers}

parsed = []
for line in input_lines:
	parsed.append(ParseInputLine(line))

# Silver star
ticket_sum = 0
for ticket in parsed:
	matching = len(set(ticket['selected']) & set(ticket['winning']))
	if matching == 0:
		continue
	else:
		ticket_sum += (2 ** (matching - 1))

print('Silver answer: ' + str(ticket_sum))

# Gold star
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

print('Gold answer: ' + str(tickets_count))
