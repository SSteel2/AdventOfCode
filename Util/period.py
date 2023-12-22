def CalculatePeriod(history):
	period = None
	for t in range(1, len(history)):
		found_period = True
		for i in range(len(history)):
			if history[i] != history[i % t]:
				found_period = False
				break
		if found_period:
			period = t
			break
	return period