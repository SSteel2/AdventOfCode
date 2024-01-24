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

def launchSolution(year, day):
	day_number = int(day)

	full_filename = f'{os.getcwd()}\\20{year}\\{day_number:0>2}\\{str(day_number)}.py'
	spec = importlib.util.spec_from_file_location(str(day_number), full_filename)
	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)

	input_lines = module.getInput('input.txt')
	result_silver, time_silver = timedExecution(module.silver, input_lines)
	result_gold, time_gold = timedExecution(module.gold, input_lines)
	return (result_silver, result_gold), (time_silver, time_gold)

def getAllDays(year):
	return next(os.walk(f'20{year}'))[1]

def printAnswers(results, task):
	print(f'[Day {task:0>2} Answer]  Silver {results[0]:18}  | Gold: {results[1]:18}')

def printTime(times, task):
	print(f'[Day {task:0>2} Time (s)]  Silver {times[0] // 100000 / 10000:15.4f}  | Gold: {times[1] // 100000 / 10000:15.4f}')

def runSingle(year, day, isOutputTime, isOutputAnswers):
	results, times = launchSolution(year, day)
	if isOutputAnswers:
		printAnswers(results, int(day))
	if isOutputTime:
		printTime(times, int(day))

def runAll(year, isOutputTime, isOutputAnswers):
	days = getAllDays(year)
	for day in days:
		runSingle(year, day, isOutputTime, isOutputAnswers)

def main():
	parser = argparse.ArgumentParser(prog='Advent of Code', description='Advent of Code solution runner')
	parser.add_argument('year', help='2-digit year number')
	parser.add_argument('day', help='day number, "all" to run all days')
	parser.add_argument('-t', '--time', action='store_true', help='output time taken')
	parser.add_argument('-a', '--answers', action='store_false', help='do not output answers (default=True)', default=True)
	args = parser.parse_args()
	if not args.time and not args.answers:
		print("At least one output mode must be selected. -a and -t options are both false.")
		return
	if args.day == 'all':
		runAll(args.year, args.time, args.answers)
	else:
		runSingle(args.year, args.day, args.time, args.answers)

if __name__ == '__main__':
	main()
