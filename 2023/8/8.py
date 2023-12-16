from functools import reduce

input_lines = []
with open('input.txt', 'r') as input_file:
	for line in input_file:
		input_lines.append(line.removesuffix('\n'))

# Parse input
instructions = input_lines[0]

roads = {i[0:3]: {'L': i[7:10], 'R': i[12:15]} for i in input_lines[2:]}

# Silver star
steps = 0
current = 'AAA'
while current != 'ZZZ':
	current = roads[current][instructions[steps % len(instructions)]]
	steps += 1

print('Silver answer: ' + str(steps))

# Gold star
def gcd(a, b):
	if a == 0 or b == 0:
		return None
	while a != 0:
		if b > a:
			a, b = b, a
		a -= b
	return b

def lcm(a, b):
	return a * b // gcd(a, b)

steps = []
starts = [i for i in roads if i[2] == 'A']
for start in starts:
	step_count = 0
	while start[-1] != 'Z':
		start = roads[start][instructions[step_count % len(instructions)]]
		step_count += 1
	steps.append(step_count)

print(steps)
result = reduce(lcm, steps)

print('Gold answer: ' + str(result))
