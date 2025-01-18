import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _initialize_prime_table(threshold):
	prime_table = []
	for i in range(2, int(threshold ** 0.5)):
		is_prime = True
		for prime in prime_table:
			if i % prime == 0:
				is_prime = False
				break
		if is_prime:
			prime_table.append(i)
	return prime_table

def _prime_components(prime_table, number):
	components = {}
	for prime in prime_table:
		if prime > number:
			break
		while number % prime == 0:
			if prime in components:
				components[prime] += 1
			else:
				components[prime] = 1
			number //= prime
	if number > 1:
		components[number] = 1
	return components

def _get_next_divisor(prime_divisors):
	if len(prime_divisors) == 0:
		return
	current_key = [0 for i in range(len(prime_divisors))]
	max_key = list(prime_divisors.values())
	while current_key[-1] <= max_key[-1]:
		current_divisor = 1
		for index, prime in enumerate(prime_divisors):
			current_divisor *= prime ** current_key[index]
		yield current_divisor
		current_key[0] += 1
		for i in range(len(current_key) - 1):
			if current_key[i] > max_key[i]:
				current_key[i] = 0
				current_key[i + 1] += 1
			else:
				break

def _sum_divisors(prime_table, number, predicate):
	prime_divisors = _prime_components(prime_table, number)
	divisors_sum = 0
	for divisor in _get_next_divisor(prime_divisors):
		if predicate(divisor, number):
			divisors_sum += divisor
	return divisors_sum

def _solve(threshold, sum_function):
	prime_table = _initialize_prime_table(threshold)
	for i in range(1, threshold):
		divisors_sum = sum_function(prime_table, i)
		if divisors_sum >= threshold:
			return i

def silver(input_lines):
	threshold = int(input_lines[0]) // 10
	predicate = lambda divisor, number: True
	return _solve(threshold, lambda prime_table, test_number: _sum_divisors(prime_table, test_number, predicate))

def gold(input_lines):
	threshold = int(input_lines[0]) // 11 + 1
	predicate = lambda divisor, number: divisor * 50 >= number
	return _solve(threshold, lambda prime_table, test_number: _sum_divisors(prime_table, test_number, predicate))
