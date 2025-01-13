import Util.input
from itertools import combinations_with_replacement

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(input_lines):
	ingredients = {}
	for line in input_lines:
		split_line = line.split(': ')
		ingredients[split_line[0]] = {}
		for i in split_line[1].split(', '):
			parameter = i.split(' ') 
			ingredients[split_line[0]][parameter[0]] = int(parameter[1])
	return ingredients

def _ingredient_score_silver(ingredients, ingredient_counts):
	counts = {'capacity': 0, 'durability': 0, 'flavor': 0, 'texture': 0}
	for parameter in counts.keys():
		for ingredient in ingredient_counts:
			counts[parameter] += ingredient_counts[ingredient] * ingredients[ingredient][parameter]
		if counts[parameter] <= 0:
			return 0
	return counts['capacity'] * counts['durability'] * counts['flavor'] * counts['texture']

def _ingredient_score_gold(ingredients, ingredient_counts):
	counts = {'capacity': 0, 'durability': 0, 'flavor': 0, 'texture': 0, 'calories': 0}
	for parameter in counts.keys():
		for ingredient in ingredient_counts:
			counts[parameter] += ingredient_counts[ingredient] * ingredients[ingredient][parameter]
		if counts[parameter] <= 0:
			return 0
	if counts['calories'] != 500:
		return 0
	return counts['capacity'] * counts['durability'] * counts['flavor'] * counts['texture']

def _solve(input_lines, counting_function):
	ingredients = _parse(input_lines)
	max_score = 0
	for combination in combinations_with_replacement(ingredients.keys(), 100):
		ingredient_counts = {i: combination.count(i) for i in ingredients.keys()}
		score = counting_function(ingredients, ingredient_counts)
		if score > max_score:
			max_score = score
	return max_score

def silver(input_lines):
	return _solve(input_lines, _ingredient_score_silver)

def gold(input_lines):
	return _solve(input_lines, _ingredient_score_gold)
