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
	if result is None:
		return None, None
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
	output = f'[Day {task:0>2} Answer]'
	if results[0] is None:
		output += f'  Silver: {"None":>18}'
	else:
		output += f'  Silver: {results[0]:18}'
	if results[1] is None:
		output += f'  | Gold: {"None":>18}'
	else:
		output += f'  | Gold: {results[1]:18}'
	print(output)

def printTime(times, task):
	output = f'[Day {task:0>2} Time (s)]'
	if times[0] is None:
		output += f'  Silver: {"None":>15}'
	else:
		output += f'  Silver: {times[0] // 100000 / 10000:15.4f}'
	if times[1] is None:
		output += f'  | Gold: {"None":>15}'
	else:
		output += f'  | Gold: {times[1] // 100000 / 10000:15.4f}'
	print(output)

def runSingle(year, day, isOutputTime, isOutputAnswers, runs_count):
	results, times = launchSolution(year, day)
	if runs_count > 1:
		run_times = times
		for i in range(1, runs_count):
			_, times = launchSolution(year, day)
			run_times = (run_times[0] + times[0], run_times[1] + times[1])
		times = (run_times[0] / runs_count, run_times[1] / runs_count)

	if isOutputAnswers:
		printAnswers(results, int(day))
	if isOutputTime:
		printTime(times, int(day))

def runAll(year, isOutputTime, isOutputAnswers, runs_count):
	days = getAllDays(year)
	for day in days:
		runSingle(year, day, isOutputTime, isOutputAnswers, runs_count)
		
def setup(year, day):
	# create directory
	directory = os.path.join(os.getcwd(), f'20{year}', f'{int(day):0>2}')
	if not os.path.isdir(directory):
		print(f'Folder \'{directory}\' created')
		os.makedirs(directory)
	filename = f'{int(day)}.py'
	full_path = os.path.join(directory, filename)
	if os.path.isfile(filename):
		print(f'File \'{full_path}\' already exists')
		return
	with open(full_path, 'w') as seed_file:
		seed_file.write('import Util.input\n')
		seed_file.write('\n')
		seed_file.write('def getInput(filename):\n')
		seed_file.write('	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))\n')
		seed_file.write('\n')
		seed_file.write('def silver(input_lines):\n')
		seed_file.write('	pass\n')
		seed_file.write('\n')
		seed_file.write('def gold(input_lines):\n')
		seed_file.write('	pass\n')
		print(f'File \'{full_path}\' created')
	filename = f'input.txt'
	full_path = os.path.join(directory, filename)
	with open(full_path, 'w') as input_file:
		input_file.write('')
		print(f'File \'{full_path}\' created')

def main():
	parser = argparse.ArgumentParser(prog='Advent of Code', description='Advent of Code solution runner')
	parser.add_argument('year', help='2-digit year number')
	parser.add_argument('day', help='day number, "all" to run all days')
	parser.add_argument('-t', '--time', action='store_true', help='output time taken')
	parser.add_argument('-m', '--multiple-runs', action='store', help='number of runs to make for averaging time taken, useful for very small times (default=1)', default=1, type=int)
	parser.add_argument('-a', '--answers', action='store_false', help='do not output answers (default=True)', default=True)
	parser.add_argument('-s', '--setup', action='store_true', help='create folder and initial file for specific day')
	args = parser.parse_args()
	if args.setup:
		setup(args.year, args.day)
		return
	if not args.time and not args.answers:
		print("At least one output mode must be selected. -a and -t options are both false.")
		return
	if args.day == 'all':
		runAll(args.year, args.time, args.answers, args.multiple_runs)
	else:
		runSingle(args.year, args.day, args.time, args.answers, args.multiple_runs)

if __name__ == '__main__':
	main()
