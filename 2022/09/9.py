import Util.input
import Util.directions

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(line):
	split_line = line.split(' ')
	return {'direction': split_line[0], 'move_count': int(split_line[1])}

def _follow(tail, head):
	if head[0] + 2 == tail[0] and head[1] + 2 == tail[1]:
		return (head[0] + 1, head[1] + 1)
	if head[0] - 2 == tail[0] and head[1] + 2 == tail[1]:
		return (head[0] - 1, head[1] + 1)
	if head[0] + 2 == tail[0] and head[1] - 2 == tail[1]:
		return (head[0] + 1, head[1] - 1)
	if head[0] - 2 == tail[0] and head[1] - 2 == tail[1]:
		return (head[0] - 1, head[1] - 1)
	if head[0] + 2 == tail[0]:
		return (head[0] + 1, head[1])
	if head[0] - 2 == tail[0]:
		return (head[0] - 1, head[1])
	if head[1] + 2 == tail[1]:
		return (head[0], head[1] + 1)
	if head[1] - 2 == tail[1]:
		return (head[0], head[1] - 1)
	return tail

def _solve(input_lines, rope_length):
	instructions = Util.input.ParseInputLines(input_lines, _parse)
	rope = [(0, 0) for i in range(rope_length)]
	visited = set()
	visited.add((0, 0))
	for instruction in instructions:
		for _ in range(instruction['move_count']):
			rope[0] = Util.directions.Move(rope[0], instruction['direction'])
			for i in range(1, rope_length):
				prev_rope = rope[i]
				rope[i] = _follow(rope[i], rope[i - 1])
				if rope[i] == prev_rope:
					break
			visited.add(rope[rope_length - 1])
	return len(visited)

def silver(input_lines):
	return _solve(input_lines, 2)

def gold(input_lines):
	return _solve(input_lines, 10)
