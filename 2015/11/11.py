import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _is_valid_password(password):
	if any([i in [ord('i'), ord('o'), ord('l')] for i in password]):
		return False
	differences = [password[i + 1] - password[i] for i in range(len(password) - 1)]
	last_zero = -2
	last_one = -2
	contains_two_pairs = False
	contains_sequence = False
	for index, number in enumerate(differences):
		if number == 0:
			if last_zero == -2 or last_zero + 1 == index:
				last_zero = index
			else:
				contains_two_pairs = True
		if number == 1:
			if last_one != -1 and last_one + 1 == index:
				contains_sequence = True
			else:
				last_one = index
	return contains_sequence and contains_two_pairs

def _incremet(password_numbers):
	password_numbers[-1] += 1
	for i in range(len(password_numbers) - 1, -1, -1):
		if password_numbers[i] >= 26:
			password_numbers[i] = 0
			password_numbers[i - 1] += 1
		else:
			break
	return password_numbers

def _find_next_password(password):
	password_numbers = [ord(i) - 97 for i in password]
	password_numbers = _incremet(password_numbers)
	while not _is_valid_password(password_numbers):
		password_numbers = _incremet(password_numbers)
	return ''.join([chr(i + 97) for i in password_numbers])

def silver(input_lines):
	return _find_next_password(input_lines[0])

def gold(input_lines):
	return _find_next_password(_find_next_password(input_lines[0]))
