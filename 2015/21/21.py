import Util.input
from math import inf

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(input_lines):
	boss = {}
	for line in input_lines:
		split_line = line.split(': ')
		boss[split_line[0]] = int(split_line[1])	
	return boss

def _initialize_shop():
	weapons = []
	weapons.append({'name': 'Dagger', 'cost': 8, 'damage': 4})
	weapons.append({'name': 'Shortsword', 'cost': 10, 'damage': 5})
	weapons.append({'name': 'Warhammer', 'cost': 25, 'damage': 6})
	weapons.append({'name': 'Longsword', 'cost': 40, 'damage': 7})
	weapons.append({'name': 'Greataxe', 'cost': 74, 'damage': 8})
	armor = []
	armor.append({'name': 'Leather', 'cost': 13, 'armor': 1})
	armor.append({'name': 'Chainmail', 'cost': 31, 'armor': 2})
	armor.append({'name': 'Splintmail', 'cost': 53, 'armor': 3})
	armor.append({'name': 'Bandedmail', 'cost': 75, 'armor': 4})
	armor.append({'name': 'Platemail', 'cost': 102, 'armor': 5})
	rings = []
	rings.append({'name': 'Damage +1', 'cost': 25, 'damage': 1, 'armor': 0})
	rings.append({'name': 'Damage +2', 'cost': 50, 'damage': 2, 'armor': 0})
	rings.append({'name': 'Damage +3', 'cost': 100, 'damage': 3, 'armor': 0})
	rings.append({'name': 'Defense +1', 'cost': 20, 'damage': 0, 'armor': 1})
	rings.append({'name': 'Defense +2', 'cost': 40, 'damage': 0, 'armor': 2})
	rings.append({'name': 'Defense +3', 'cost': 80, 'damage': 0, 'armor': 3})
	return weapons, armor, rings

def _buy_item(player, item):
	if 'damage' in item:
		player['Damage'] += item['damage']
	if 'armor' in item:
		player['Armor'] += item['armor']
	return item['cost']

def _increment_key(current_key, max_key):
	current_key[0] += 1
	for i in range(len(current_key) - 1):
		if current_key[i] > max_key[i]:
			current_key[i] = 0
			current_key[i + 1] += 1
		else:
			break

def _shopping_list(weapons, armor, rings):
	# [weapon, armor, ring 1, ring 2]
	# 0 - no item (ignored for weapon), other number - shop item
	current_key = [0, 0, 0, 0]
	max_key = [len(weapons) - 1, len(armor), len(rings), len(rings)]
	while current_key[-1] <= max_key[-1]:
		player = {'Hit Points': 100, 'Damage': 0, 'Armor': 0}
		# print(current_key)
		cost = _buy_item(player, weapons[current_key[0]])
		if current_key[1] > 0:
			cost += _buy_item(player, armor[current_key[1] - 1])
		if current_key[2] > 0:
			cost += _buy_item(player, rings[current_key[2] - 1])
		if current_key[3] > 0:
			cost += _buy_item(player, rings[current_key[3] - 1])
		yield player, cost
		_increment_key(current_key, max_key)
		if current_key[2] == current_key[3] and current_key[2] != 0:
			current_key[2] += 1
			if current_key[2] > max_key[2]:
				current_key[2] = 0
				current_key[3] += 1
	return

def _is_boss_beatable(player, boss):
	effective_player_damage = max(player['Damage'] - boss['Armor'], 1)
	hits_to_kill = boss['Hit Points'] // effective_player_damage
	if boss['Hit Points'] % effective_player_damage != 0:
		hits_to_kill += 1
	effective_boss_damage = max(boss['Damage'] - player['Armor'], 1)
	hits_to_die = player['Hit Points'] // effective_boss_damage
	if player['Hit Points'] % effective_boss_damage != 0:
		hits_to_die += 1
	return hits_to_kill <= hits_to_die

def silver(input_lines):
	boss = _parse(input_lines)
	weapons, armor, rings = _initialize_shop()
	min_cost = inf
	for player, cost in _shopping_list(weapons, armor, rings):
		if cost < min_cost and _is_boss_beatable(player, boss):
			min_cost = cost
	return min_cost

def gold(input_lines):
	boss = _parse(input_lines)
	weapons, armor, rings = _initialize_shop()
	max_cost = 0
	for player, cost in _shopping_list(weapons, armor, rings):
		if cost > max_cost and not _is_boss_beatable(player, boss):
			max_cost = cost
	return max_cost
