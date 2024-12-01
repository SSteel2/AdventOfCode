import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

class BlizzardLine:
	def __init__(self, line_length):
		self.line_length = line_length

conversions = {
	'^': 'U',
	'>': 'R',
	'v': 'D',
	'<': 'L',
}

def _parse(input_lines):
	blizzards = []
	ground = [['.' for i in j] for j in input_lines]
	for l, line in enumerate(input_lines):
		for c, char in enumerate(line):
			if char == '#':
				ground[l][c] = '#'
			elif char != '.':
				blizzards.append((l, c, conversions[char]))
	return ground, blizzards

def arrange_blizzards(blizzards, ground):
	vertical_blizzard_lines = [BlizzardLine(len(ground) - 2) for _ in range(len(ground[0]) - 2)]
	horizontal_blizzard_lines = [BlizzardLine(len(ground[0]) - 2) for _ in range(len(ground) - 2)]
	for blizzard in blizzards:
		if blizzard[2] == 'U' or blizzard[2] == 'D':
			vertical_blizzard_lines[blizzard[1] - 1].AddBlizzard(blizzard[0] - 1, False if blizzard[2] == 'D' else True)
		elif blizzard[2] == 'L' or blizzard[2] == 'R':
			vertical_blizzard_lines[blizzard[0] - 1].AddBlizzard(blizzard[1] - 1, False if blizzard[2] == 'R' else True)

def silver(input_lines):
	ground, blizzards = _parse(input_lines)

def gold(input_lines):
	pass
