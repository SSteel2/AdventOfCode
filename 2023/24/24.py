import math
import Util.input
import Util.math

def getInput(filename):
	return Util.input.LoadInput(Util.input.GetInputFile(__file__, filename))

def _parse(line):
	points = line.split(' @ ')
	position = points[0].split(', ')
	velocity = points[1].split(', ')
	return {'px': int(position[0]), 'py': int(position[1]), 'pz': int(position[2]), 'vx': int(velocity[0]), 'vy': int(velocity[1]), 'vz': int(velocity[2])}

def _intercept(bullet_a, bullet_b):
	pxa = bullet_a['px']
	pya = bullet_a['py']
	vxa = bullet_a['vx']
	vya = bullet_a['vy']
	pxb = bullet_b['px']
	pyb = bullet_b['py']
	vxb = bullet_b['vx']
	vyb = bullet_b['vy']
	# velocity multiplier to reach intersection point for bullet a and b
	if vxa / vya * vyb - vxb == 0:
		return (math.inf, math.inf, math.inf, math.inf)
	b = (pxb - pxa - (vxa / vya) * (pyb - pya)) / (vxa / vya * vyb - vxb)
	a = (pyb + b * vyb - pya) / vya
	return (a, b, pxa + vxa * a, pya + vya * a)

# test area for sample input:
# test_area = (7, 27)

def silver(input_lines):
	hail = Util.input.ParseInputLines(input_lines, _parse)
	test_area = (200000000000000, 400000000000000)

	result = 0
	for i, bullet_a in enumerate(hail):
		for j, bullet_b in enumerate(hail[i + 1:]):
			colision = _intercept(bullet_a, bullet_b)
			if colision[0] < 0 or colision[1] < 0:
				continue  # happened in the past
			if colision[2] < test_area[0] or colision[2] > test_area[1] or colision[3] < test_area[0] or colision[3] > test_area[1]:
				continue  # outside test area
			result += 1
	return result

def _subtract(matrix, line_a, line_b, multiplier):
	for i in range(len(matrix[line_a])):
		matrix[line_b][i] = matrix[line_b][i] - matrix[line_a][i] * multiplier

def _multiply(matrix, line, multiplier):
	for i in range(len(matrix[line])):
		matrix[line][i] *= multiplier

def _divide(matrix, line, divisor):
	for i in range(len(matrix[line])):
		matrix[line][i] //= divisor

def _makeZero(matrix, line_int, line_zero, col):
	if matrix[line_zero][col] % matrix[line_int][col] == 0:
		_subtract(matrix, line_int, line_zero, matrix[line_zero][col] // matrix[line_int][col])
	else:
		mult = Util.math.lcm(abs(matrix[line_zero][col]), abs(matrix[line_int][col]))
		mult_zero = mult // matrix[line_zero][col]
		mult_int = mult // matrix[line_int][col]
		_multiply(matrix, line_zero, mult_zero)
		_multiply(matrix, line_int, mult_int)
		_subtract(matrix, line_int, line_zero, matrix[line_zero][col] // matrix[line_int][col])
		_divide(matrix, line_int, mult_int)


def _gausianElimination(e1, e2, e3, e4, e5):
	# out of 5 line definitions the point is to get 4 line equations with 4 variables
	# variables in order: vx, px, vy, py
	matrix = [[0 for _ in range(5)] for _ in range(4)]
	matrix[0][0] = e1['py'] - e2['py']
	matrix[0][1] = e2['vy'] - e1['vy']
	matrix[0][2] = e2['px'] - e1['px']
	matrix[0][3] = e1['vx'] - e2['vx']
	matrix[0][4] = e2['px'] * e2['vy'] - e2['py'] * e2['vx'] - e1['px'] * e1['vy'] + e1['py'] * e1['vx'] 
	matrix[1][0] = e1['py'] - e3['py']
	matrix[1][1] = e3['vy'] - e1['vy']
	matrix[1][2] = e3['px'] - e1['px']
	matrix[1][3] = e1['vx'] - e3['vx']
	matrix[1][4] = e3['px'] * e3['vy'] - e3['py'] * e3['vx'] - e1['px'] * e1['vy'] + e1['py'] * e1['vx'] 
	matrix[2][0] = e1['py'] - e4['py']
	matrix[2][1] = e4['vy'] - e1['vy']
	matrix[2][2] = e4['px'] - e1['px']
	matrix[2][3] = e1['vx'] - e4['vx']
	matrix[2][4] = e4['px'] * e4['vy'] - e4['py'] * e4['vx'] - e1['px'] * e1['vy'] + e1['py'] * e1['vx'] 
	matrix[3][0] = e1['py'] - e5['py']
	matrix[3][1] = e5['vy'] - e1['vy']
	matrix[3][2] = e5['px'] - e1['px']
	matrix[3][3] = e1['vx'] - e5['vx']
	matrix[3][4] = e5['px'] * e5['vy'] - e5['py'] * e5['vx'] - e1['px'] * e1['vy'] + e1['py'] * e1['vx'] 
	_makeZero(matrix, 0, 1, 0)
	_makeZero(matrix, 0, 2, 0)
	_makeZero(matrix, 0, 3, 0)
	_makeZero(matrix, 1, 2, 1)
	_makeZero(matrix, 1, 3, 1)
	_makeZero(matrix, 2, 3, 2)
	_divide(matrix, 3, matrix[3][3])
	_makeZero(matrix, 3, 2, 3)
	_divide(matrix, 2, matrix[2][2])
	_makeZero(matrix, 3, 1, 3)
	_makeZero(matrix, 2, 1, 2)
	_divide(matrix, 1, matrix[1][1])
	_makeZero(matrix, 3, 0, 3)
	_makeZero(matrix, 2, 0, 2)
	_makeZero(matrix, 1, 0, 1)
	_divide(matrix, 0, matrix[0][0])
	return {'vx': matrix[0][4], 'px': matrix[1][4], 'vy': matrix[2][4], 'py': matrix[3][4]}

def gold(input_lines):
	hail = Util.input.ParseInputLines(input_lines, _parse)
	result = _gausianElimination(hail[0], hail[1], hail[2], hail[3], hail[4])
	# calculate z values
	pay = hail[1]['py']
	paz = hail[1]['pz']
	vay = hail[1]['vy']
	vaz = hail[1]['vz']
	pby = hail[2]['py']
	pbz = hail[2]['pz']
	vby = hail[2]['vy']
	vbz = hail[2]['vz']
	py = result['py']
	vy = result['vy']

	t1 = (pay - py) // (vy - vay)
	t2 = (pby - py) // (vy - vby)
	result['vz'] = (pbz + vbz * t2 - paz - vaz * t1) // (t2 - t1)
	result['pz'] = paz + vaz * t1 - result['vz'] * t1
	return result['px'] + result['py'] + result['pz']
