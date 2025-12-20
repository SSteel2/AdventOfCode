import Util.input
import Util.ranges

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(input_lines):
	is_first_part = True
	fresh_ranges = []
	products = []
	for line in input_lines:
		if is_first_part:
			if line == "":
				is_first_part = False
				continue
			fresh_ranges.append(tuple(int(i) for i in line.split('-')))
		else:
			products.append(int(line))
	return fresh_ranges, products

def _construct_fresh_sapns(fresh_ranges):
	fresh = Util.ranges.Spans()
	for i in fresh_ranges:
		fresh.add(Util.ranges.Span(i[0], i[1] + 1))
	fresh.union()
	return fresh

def silver(input_lines):
	fresh_ranges, products = _parse(input_lines)
	fresh = _construct_fresh_sapns(fresh_ranges)
	fresh_products_count = 0
	for product in products:
		if product in fresh:
			fresh_products_count += 1
	return fresh_products_count

def gold(input_lines):
	fresh_ranges, _ = _parse(input_lines)
	fresh = _construct_fresh_sapns(fresh_ranges)
	fresh_products_count = 0
	for span in fresh.spans:
		fresh_products_count += span.end - span.start
	return fresh_products_count
