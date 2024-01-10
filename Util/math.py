def gcd(a, b):
	if a == 0 or b == 0:
		return None
	while a != 0:
		if b > a:
			a, b = b, a
		a -= b
	return b

def lcm(a, b):
	return a * b // gcd(a, b)