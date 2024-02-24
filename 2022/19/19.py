import Util.input
import math

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

Robots = {
	'geode': {'primary_resource_price': 'geode_price_ore', 'secondary_resource_price': 'geode_price_obsidian', 'secondary_resource': 'obsidian'},
	'obsidian': {'primary_resource_price': 'obsidian_price_ore', 'secondary_resource_price': 'obsidian_price_clay', 'secondary_resource': 'clay'},
	'clay': {'primary_resource_price': 'clay_price_ore', 'secondary_resource_price': None, 'secondary_resource': None},
	'ore': {'primary_resource_price': 'ore_price_ore', 'secondary_resource_price': None, 'secondary_resource': None},
}

def _build(robot_key, mine_time, current_time, resources, collection_rate, current_max, blueprint, max_time):
	future_time = mine_time + 1
	if current_time + future_time < max_time:
		robot = Robots[robot_key]
		new_collection_rate = collection_rate.copy()
		new_collection_rate[robot_key] += 1
		new_resources = {
			'ore': resources['ore'] + collection_rate['ore'] * future_time - blueprint[robot['primary_resource_price']],
			'clay': resources['clay'] + collection_rate['clay'] * future_time - (blueprint[robot['secondary_resource_price']] if robot_key == 'obsidian' else 0),
			'obsidian': resources['obsidian'] + collection_rate['obsidian'] * future_time - (blueprint[robot['secondary_resource_price']] if robot_key == 'geode' else 0),
			'geode': resources['geode'] + collection_rate['geode'] * future_time}
		return _move(current_time + future_time, new_resources, new_collection_rate, current_max, blueprint, max_time)
	else:
		return None

def _mineTime(needed, current, rate):
	if rate == 0:
		return math.inf
	if current >= needed:
		return 0
	missing = needed - current
	return missing // rate + (1 if missing % rate != 0 else 0)

def _isBuildingOptimal(mine_time_target, mine_time_alternative, mine_time_double_ore):
	return not (mine_time_target > mine_time_alternative and mine_time_double_ore <= mine_time_target)

Conditions = [
	('geode', lambda blue, rate, mine_times: rate['obsidian'] > 0 and _isBuildingOptimal(mine_times['geode'], mine_times['obsidian'], mine_times['geode_obsidian'])),
	('obsidian', lambda blue, rate, mine_times: rate['clay'] > 0 and rate['obsidian'] < blue['geode_price_obsidian'] and _isBuildingOptimal(mine_times['obsidian'], mine_times['clay'], mine_times['obsidian_clay'])),
	('clay', lambda blue, rate, mine_times: rate['clay'] < blue['obsidian_price_clay']),
	('ore', lambda blue, rate, mine_times: rate['ore'] < rate['ore_max'] and rate['geode'] == 0),
]

def _move(current_time, resources, collection_rate, current_max, blueprint, max_time):
	time_left = max_time - current_time
	max_possibility = resources['geode'] + collection_rate['geode'] * time_left + (time_left + 1) * time_left // 2
	if max_possibility <= current_max:
		return None

	geode_ore_mine_time = _mineTime(blueprint['geode_price_ore'], resources['ore'], collection_rate['ore'])
	obsidian_ore_mine_time = _mineTime(blueprint['obsidian_price_ore'], resources['ore'], collection_rate['ore'])
	clay_ore_mine_time = _mineTime(blueprint['clay_price_ore'], resources['ore'], collection_rate['ore'])
	mine_times = {
		'geode': max(geode_ore_mine_time, _mineTime(blueprint['geode_price_obsidian'], resources['obsidian'], collection_rate['obsidian'])),
		'obsidian': max(obsidian_ore_mine_time, _mineTime(blueprint['obsidian_price_clay'], resources['clay'], collection_rate['clay'])),
		'clay': clay_ore_mine_time,
		'ore': _mineTime(blueprint['ore_price_ore'], resources['ore'], collection_rate['ore']),
		'geode_obsidian': geode_ore_mine_time + obsidian_ore_mine_time,
		'obsidian_clay': obsidian_ore_mine_time + clay_ore_mine_time
	}

	max_result = -1
	for condition in Conditions:
		if condition[1](blueprint, collection_rate, mine_times):
			result = _build(condition[0], mine_times[condition[0]], current_time, resources, collection_rate, current_max, blueprint, max_time)
			if result != None and result > max_result:
				max_result = result
				if max_result > current_max:
					current_max = max_result

	if max_result == -1:
		return resources['geode'] + collection_rate['geode'] * (max_time - current_time)
	else:
		return max_result

def _solve(blueprint, max_time):
	max_ore_needed = max(blueprint['clay_price_ore'], blueprint['obsidian_price_ore'], blueprint['geode_price_ore'])
	collection_rate = {'ore': 1, 'clay': 0, 'obsidian': 0, 'geode': 0, 'ore_max': max_ore_needed}
	resources = {'ore': 0, 'clay': 0, 'obsidian': 0, 'geode': 0}
	return _move(0, resources, collection_rate, 0, blueprint, max_time)

def silver(input_lines):
	blueprints = Util.input.ParseInputLines(input_lines, _parse)
	result = 0
	for blueprint in blueprints:
		max_geodes = _solve(blueprint, 24)
		result += (max_geodes * blueprint['id'])
	return result

def gold(input_lines):
	blueprints = Util.input.ParseInputLines(input_lines, _parse)
	result = 1
	for blueprint in blueprints[:3]:
		max_geodes = _solve(blueprint, 32)
		result *= max_geodes
	return result
