import Util.input

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(line):
	blueprint = {}
	split_line = line.split(' ')
	blueprint['id'] = int(split_line[1].removesuffix(':'))
	blueprint['ore_price_ore'] = int(split_line[6])
	blueprint['clay_price_ore'] = int(split_line[12])
	blueprint['obsidian_price_ore'] = int(split_line[18])
	blueprint['obsidian_price_clay'] = int(split_line[21])
	blueprint['geode_price_ore'] = int(split_line[27])
	blueprint['geode_price_obsidian'] = int(split_line[30])
	return blueprint

def _mineTime(needed, current, rate):
	if current >= needed:
		return 0
	missing = needed - current
	return missing // rate + (1 if missing % rate != 0 else 0)

def _move(current_time, resources, collection_rate, blueprint, max_time, path):
	max_result = -1
	max_path = path
	if collection_rate['obsidian'] > 0:
		mine_time = max(_mineTime(blueprint['geode_price_ore'], resources['ore'], collection_rate['ore']),
			_mineTime(blueprint['geode_price_obsidian'], resources['obsidian'], collection_rate['obsidian']))
		if current_time + mine_time + 1 < max_time:
			new_collection_rate = collection_rate.copy()
			new_collection_rate['geode'] += 1
			new_resources = {
				'ore': resources['ore'] + collection_rate['ore'] * (mine_time + 1) - blueprint['geode_price_ore'],
				'clay': resources['clay'] + collection_rate['clay'] * (mine_time + 1),
				'obsidian': resources['obsidian'] + collection_rate['obsidian'] * (mine_time + 1) - blueprint['geode_price_obsidian'],
				'geode': resources['geode'] + collection_rate['geode'] * (mine_time + 1)}
			result, p = _move(current_time + mine_time + 1, new_resources, new_collection_rate, blueprint, max_time, path + ['Geod' + str(current_time + mine_time + 1)])
			if result > max_result:
				max_result = result
				max_path = p
	if collection_rate['clay'] > 0 and collection_rate['obsidian'] < blueprint['geode_price_obsidian']:
		mine_time = max(_mineTime(blueprint['obsidian_price_ore'], resources['ore'], collection_rate['ore']),
			_mineTime(blueprint['obsidian_price_clay'], resources['clay'], collection_rate['clay']))
		if current_time + mine_time + 1 < max_time:
			new_collection_rate = collection_rate.copy()
			new_collection_rate['obsidian'] += 1
			new_resources = {
				'ore': resources['ore'] + collection_rate['ore'] * (mine_time + 1) - blueprint['obsidian_price_ore'],
				'clay': resources['clay'] + collection_rate['clay'] * (mine_time + 1) - blueprint['obsidian_price_clay'],
				'obsidian': resources['obsidian'] + collection_rate['obsidian'] * (mine_time + 1),
				'geode': resources['geode'] + collection_rate['geode'] * (mine_time + 1)}
			result, p = _move(current_time + mine_time + 1, new_resources, new_collection_rate, blueprint, max_time, path + ['Obs' + str(current_time + mine_time + 1)])
			if result > max_result:
				max_result = result
				max_path = p
	if collection_rate['clay'] < blueprint['obsidian_price_clay']:
		mine_time = _mineTime(blueprint['clay_price_ore'], resources['ore'], collection_rate['ore'])
		if current_time + mine_time + 1 < max_time:
			new_collection_rate = collection_rate.copy()
			new_collection_rate['clay'] += 1
			new_resources = {
				'ore': resources['ore'] + collection_rate['ore'] * (mine_time + 1) - blueprint['clay_price_ore'],
				'clay': resources['clay'] + collection_rate['clay'] * (mine_time + 1),
				'obsidian': resources['obsidian'] + collection_rate['obsidian'] * (mine_time + 1),
				'geode': resources['geode'] + collection_rate['geode'] * (mine_time + 1)}
			result, p = _move(current_time + mine_time + 1, new_resources, new_collection_rate, blueprint, max_time, path + ['Clay' + str(current_time + mine_time + 1)])
			if result > max_result:
				max_result = result
				max_path = p
	if collection_rate['ore'] < collection_rate['ore_max']:
		mine_time = _mineTime(blueprint['ore_price_ore'], resources['ore'], collection_rate['ore'])
		if current_time + mine_time + 1 < max_time:
			new_collection_rate = collection_rate.copy()
			new_collection_rate['ore'] += 1
			new_resources = {
				'ore': resources['ore'] + collection_rate['ore'] * (mine_time + 1) - blueprint['ore_price_ore'],
				'clay': resources['clay'] + collection_rate['clay'] * (mine_time + 1),
				'obsidian': resources['obsidian'] + collection_rate['obsidian'] * (mine_time + 1),
				'geode': resources['geode'] + collection_rate['geode'] * (mine_time + 1)}
			result, p = _move(current_time + mine_time + 1, new_resources, new_collection_rate, blueprint, max_time, path + ['Ore' + str(current_time + mine_time + 1)])
			if result > max_result:
				max_result = result
				max_path = p
	if max_result == -1:
		return resources['geode'] + collection_rate['geode'] * (max_time - current_time), path
	else:
		return max_result, max_path

def _solve(blueprint, max_time):
	max_ore_needed = max(blueprint['clay_price_ore'], blueprint['obsidian_price_ore'], blueprint['geode_price_ore'])
	collection_rate = {'ore': 1, 'clay': 0, 'obsidian': 0, 'geode': 0, 'ore_max': max_ore_needed}
	resources = {'ore': 0, 'clay': 0, 'obsidian': 0, 'geode': 0}
	return _move(0, resources, collection_rate, blueprint, max_time, [])

def silver(input_lines):
	blueprints = Util.input.ParseInputLines(input_lines, _parse)
	result = 0
	for blueprint in blueprints:
		max_geodes, path = _solve(blueprint, 24)
		result += (max_geodes * blueprint['id'])
	return result

def gold(input_lines):
	blueprints = Util.input.ParseInputLines(input_lines, _parse)
	result = 1
	for blueprint in blueprints[:3]:
		max_geodes, path = _solve(blueprint, 32)
		result *= max_geodes
	return result
