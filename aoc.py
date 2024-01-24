# Runner for all Advent of Code solutions
import importlib.util
# I could have used importlib.import_module, but the catch is to use dots '.' instead of slashes...
import argparse
import os
import time

def timedExecution(func, input_lines):
	start_time = time.perf_counter_ns()
	result = func(input_lines)
	end_time = time.perf_counter_ns()
	return result, end_time - start_time

def runSolution(year, day):
	day_number = int(day)

	full_filename = f'{os.getcwd()}\\20{year}\\{day_number:0>2}\\{str(day_number)}.py'
	spec = importlib.util.spec_from_file_location(str(day_number), full_filename)
	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)

	input_lines = module.getInput('input.txt')
	result_silver, time_silver = timedExecution(module.silver, input_lines)
	result_gold, time_gold = timedExecution(module.gold, input_lines)
	return (result_silver, result_gold), (time_silver, time_gold)

def printAnswers(results):
	print(f'[Answer]  Silver {results[0]:18}  | Gold: {results[1]:18}')

def printTime(times):
	print(f'[Time (s)]  Silver {times[0] // 100000 / 10000:15.4f}  | Gold: {times[1] // 100000 / 10000:15.4f}')

def main():
	parser = argparse.ArgumentParser(prog='Advent of Code', description='Advent of Code solution runner')
	parser.add_argument('year', help='2-digit year number')
	parser.add_argument('day', help='day number')
	parser.add_argument('-t', '--time', action='store_true', help='output time taken')
	parser.add_argument('-a', '--answers', action='store_false', help='do not output answers (default=True)', default=True)
	args = parser.parse_args()
	if not args.time and not args.answers:
		print("At least one output mode must be selected. -a and -t options are both false.")
		return
	results, times = runSolution(args.year, args.day)
	if args.answers:
		printAnswers(results)
	if args.time:
		printTime(times)

if __name__ == '__main__':
	main()
