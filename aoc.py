# Runner for all Advent of Code solutions
import importlib.util
import argparse
import os

def runSolution(year, day):
	day_number = int(day)

	full_filename = f'{os.getcwd()}\\20{year}\\{day_number:0>2}\\{str(day_number)}.py'
	spec = importlib.util.spec_from_file_location(str(day_number), full_filename)
	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)

	input_lines = module.getInput('input.txt')
	result_silver = module.silver(input_lines)
	print('Silver answer: ' + str(result_silver))
	result_gold = module.gold(input_lines)
	print('Gold answer: ' + str(result_gold))


if __name__ == '__main__':
	parser = argparse.ArgumentParser(prog='Advent of Code', description='Advent of Code solution runner')
	parser.add_argument('year', help='2-digit year number')
	parser.add_argument('day', help='day number')
	args = parser.parse_args()
	runSolution(args.year, args.day)