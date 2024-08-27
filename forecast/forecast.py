# Copyright (c) 2024, AgriTheory and contributors
# For license information, please see license.txt"


import typing
from decimal import Decimal

##############################


class Forecast:
	"""
	The input data must be Decimal objects.
	"""

	data: list = []
	forecast: list | None = None

	##############################

	def __init__(self, **kwargs):
		self.__dvzero = Decimal("0.0")
		self.__dvone = Decimal("1.0")
		self.__dvtwo = Decimal("2.0")
		self.__dvhundred = Decimal("100.0")
		self(**kwargs)

	##############################

	def __call__(
		self, data: typing.Sequence[typing.Sequence[Decimal]] | None, **kwargs
	) -> "Forecast":
		if not self.data and not data:
			raise Exception("There is no data to forecast.")

		# Replace None values with 0.0
		self.data = [[n if n else self.__dvzero for n in lst] for lst in data] if data else []

		# Verify data is of Decimal type
		for n in self.data:
			for m in n:
				if not isinstance(m, Decimal):
					raise TypeError("Data must be of type Decimal.")

		return self

	##############################

	def percent_over_previous_period(self, percent: Decimal) -> "Forecast":
		if not isinstance(percent, Decimal):
			raise TypeError("Percent must be of type Decimal.")

		self.forecast = [
			period * (self.__dvone + (percent / self.__dvhundred)) if percent else self.__dvzero
			for period in self.data[-1]
		]

		return self

	##############################

	def calculated_percent_over_previous_period(self) -> "Forecast":
		n_minus_2_data = sum(self.data[-2])
		n_minus_1_data = sum(self.data[-1])
		percent = ((n_minus_1_data / n_minus_2_data) - self.__dvone) * self.__dvhundred
		self.forecast = [
			n * (self.__dvone + (percent / self.__dvhundred)) if percent else self.__dvzero
			for n in self.data[-1]
		]

		return self

	##############################

	def previous_period_to_current_period(self) -> "Forecast":
		self.forecast = self.data[-1]

		return self

	##############################

	def moving_average(self, periods: int) -> "Forecast":
		_data = self.__flat_data if periods > len(self.data[-1]) else self.data[-1]
		if (periods - 1) > len(self.__flat_data):
			raise Exception("Cannot forecast for more periods than existing in data.")

		moving_average = [n for n in _data]
		for i in range(periods):
			moving_average.append(mean(moving_average[-periods:]))

		del moving_average[:periods]
		self.forecast = moving_average

		return self

	##############################

	def linear_approximation(self, periods: int) -> "Forecast":
		_data = self.__flat_data if periods > len(self.data[-1]) else self.data[-1]
		if (periods - 1) > len(_data):
			raise Exception("Cannot forecast for more periods than existing in data.")
		slope = (_data[-1] - _data[-periods + 1]) / Decimal(periods)
		self.forecast = [_data[-1] + (slope * Decimal(i + 1)) for i in range(periods)]

		return self

	##############################

	def least_squares_regression(self, periods: int) -> "Forecast":
		x = [Decimal(i) for i in range(1, periods + 1)]
		_data = self.__flat_data if periods > len(self.data[-1]) else self.data[-1]
		if (periods - 1) > len(_data):
			raise Exception("Cannot forecast for more periods than existing in data.")
		y = _data[-periods:]

		slope, intercept, _, _, _ = linregress(x, y)
		self.forecast = [
			(Decimal(i) * slope) + intercept for i in range(periods + 1, periods + 13)
		]

		return self

	##############################

	def second_degree_approximiation(self, periods: int) -> "Forecast":
		x = [Decimal(i) for i in range(1, periods + 1)]
		_data = self.__flat_data if periods > len(self.data[-1]) else self.data[-1]
		if (periods - 1) > len(_data):
			raise Exception("Cannot forecast for more periods than existing in data.")
		y = _data[-periods:]
		c, b, a = polyfit(x, y, deg=2)
		self.forecast = [
			a + (b * Decimal(i)) + (c * (Decimal(i) ** 2))
			for i in range(periods + 1, periods + 13)
		]

		return self

	##############################

	def flexible_method(self, percent: Decimal, periods: int) -> "Forecast":
		# Confirm percent is of Decimal type
		if not isinstance(percent, Decimal):
			raise TypeError("percent must be of type Decimal.")

		_data = self.__flat_data if periods > len(self.data[-1]) else self.data[-1]
		if (periods - 1) > len(_data):
			raise Exception("Cannot forecast for more periods than existing in data.")

		flexible_method = _data
		for i in range(periods):
			flexible_method.append(
				flexible_method[i] * (self.__dvone + (percent / self.__dvhundred))
			)
		del flexible_method[:periods]

		self.forecast = flexible_method

		return self

	##############################

	def weighted_moving_average(self, periods: int, weights: list | tuple) -> "Forecast":
		# Confirm weights are of Decimal type
		for n in weights:
			if not isinstance(n, Decimal):
				raise TypeError("Weights must be of type Decimal.")

		_data = self.__flat_data if periods > len(self.data[-1]) else self.data[-1]
		if (periods - 1) > len(_data):
			raise Exception("Cannot forecast for more periods than existing in data.")
		if sum(weights) != self.__dvone:
			raise Exception("Total of weights must be exactly 1.")
		if len(weights) != periods:
			raise Exception(
				f"Weights must have as many elements as periods. Weights: {len(weights)} Periods: {periods}."
			)

		weighted_moving_average_data = _data[-periods:]

		for i in range(periods):
			weighted_moving_average_data.append(
				sum(
					weights[j] * weighted_moving_average_data[i : i + periods][j]
					for j in range(len(weights))
				)
			)

		# Remove the historical data needed for the first several forecast period calcs
		del weighted_moving_average_data[:periods]
		self.forecast = weighted_moving_average_data

		return self

	##############################

	def linear_smoothing(self, periods: int) -> "Forecast":
		_data = self.__flat_data if periods > len(self.data[-1]) else self.data[-1]
		if (periods - 1) > len(_data):
			raise Exception("Cannot forecast for more periods than existing in data.")

		W = ((Decimal(periods) ** 2) + Decimal(periods)) / self.__dvtwo
		weights = [Decimal(n) / W for n in range(1, periods + 1)]
		linear_smoothing_data = [i for i in _data[-periods:]]

		for i in range(12):
			linear_smoothing_data.append(
				sum(
					weights[j] * linear_smoothing_data[i : i + periods][j] for j in range(len(weights))
				)
			)

		del linear_smoothing_data[:periods]
		self.forecast = linear_smoothing_data

		return self

	##############################

	def exponential_smoothing(self, periods: int, alpha: Decimal) -> "Forecast":
		if not isinstance(alpha, Decimal):
			raise TypeError("alpha must be of type Decimal.")

		_data = self.__flat_data if periods > len(self.data[-1]) else self.data[-1]
		if (periods - 1) > len(_data):
			raise Exception("Cannot forecast for more periods than existing in data.")
		smoothed = [_data[-periods]]
		values = _data[-periods + 1 :]

		for i, d in enumerate(values):
			smoothed.append(alpha * d + (self.__dvone - alpha) * smoothed[i])

		self.forecast = [smoothed[-1]] * 12

		return self

	##############################

	def exponential_smoothing_with_trend_and_seasonality(
		self,
		season: int,
		periods: int,
		alpha: Decimal,
		beta: Decimal,
	) -> "Forecast":
		if not isinstance(alpha, Decimal):
			raise TypeError("alpha must be of type Decimal.")
		if not isinstance(beta, Decimal):
			raise TypeError("beta must be of type Decimal.")

		# Calculate seasonality indices
		total_units = sum(self.data[-2]) + sum(self.data[-1])
		seasonality = [
			((data_n_minus_1 + self.data[-2][i]) / total_units) * Decimal(periods)
			for i, data_n_minus_1 in enumerate(self.data[-1])
		]

		averages = [self.data[-1][0] / seasonality[0]]
		trends = [self.__dvzero]

		for i in range(periods):
			A_t = (alpha * (self.data[-1][i] / seasonality[i])) + (
				(self.__dvone - alpha) * (averages[i - 1] + trends[i - 1])
			)
			T_t = beta * (A_t - averages[i - 1]) + ((self.__dvone - beta) * trends[i - 1])
			averages.append(A_t)
			trends.append(T_t)

		exponential_smoothing_trend_seasonality = []
		for m in range(periods):
			F = (averages[-1] + (trends[-1] * Decimal(m))) * seasonality[m - 1]
			exponential_smoothing_trend_seasonality.append(F)

		self.forecast = exponential_smoothing_trend_seasonality

		return self

	##############################

	@property
	def __flat_data(self):
		return [item for sublist in self.data for item in sublist]


##############################


def mean(x):
	"""Calculate the mean value of list of Decimal objects."""
	if len(x) == 0:
		raise ValueError("List must not be empty.")

	return sum(x) / Decimal(len(x))


##############################


def polyfit(xdata, ydata, deg, rcond=None, full=False, w=None):
	"""
	Least-squares fit of polynomial to data.
	Replacement for np.polyfit.
	xdata and ydata are list of Decimal objects.
	"""

	if not isinstance(deg, int):
		raise TypeError("deg must be an integer.")

	# We have rcond and w equal to None in our case
	if rcond:
		raise ValueError("rcond must be None.")
	if w:
		raise ValueError("w must be None.")

	dvzero = Decimal("0.0")

	xlen = len(xdata)
	ylen = len(ydata)

	if xlen == 0:
		raise TypeError("Expected non-empty vector for xdata.")

	if ylen == 0:
		raise TypeError("Expected non-empty vector for y.")

	if xlen != ylen:
		raise TypeError("Expected xdata and ydata to have the same length.")

	n = deg
	N = xlen

	xmat = [dvzero for i in range((2 * n) + 1)]
	for i in range((2 * n) + 1):
		xmat[i] = dvzero
		for j in range(N):
			# This work-around is due to a bug in the decimal package
			# 0.0 ** 0.0 should be 1 instead getting an error
			if i == 0 and xdata[j] == dvzero:
				t = Decimal("1.0")
			else:
				t = xdata[j] ** i
			xmat[i] = xmat[i] + t

	bmat = [[dvzero for i in range(n + 2)] for j in range(n + 1)]
	for i in range(n + 1):
		for j in range(n + 1):
			bmat[i][j] = xmat[i + j]

	ymat = [dvzero for i in range(n + 1)]
	for i in range(n + 1):
		ymat[i] = dvzero
		for j in range(N):
			# This work-around is due to a bug in the decimal package
			# 0.0 ** 0.0 should be 1 instead getting an error
			if i == 0 and xdata[j] == dvzero:
				t = Decimal("1.0")
			else:
				t = xdata[j] ** i
			ymat[i] = ymat[i] + (t * ydata[j])

	for i in range(n + 1):
		bmat[i][n + 1] = ymat[i]

	n = n + 1
	for i in range(n):
		for k in range(i + 1, n):
			if bmat[i][i] < bmat[k][i]:
				for j in range(n + 1):
					bmat[i][j], bmat[k][j] = bmat[k][j], bmat[i][j]

	# Gaussian elimination
	for i in range(n - 1):
		for k in range(i + 1, n):
			t = bmat[k][i] / bmat[i][i]
			for j in range(n + 1):
				bmat[k][j] = bmat[k][j] - (t * bmat[i][j])

	# Back substitution
	a = [dvzero for i in range(n + 1)]
	for i in range(n - 1, -1, -1):
		a[i] = bmat[i][n]

		for j in range(n):
			if j != i:
				a[i] = a[i] - (bmat[i][j] * a[j])

		a[i] = a[i] / bmat[i][i]

	return a[-2::-1]


##############################


def linregress(x, y, alternative="two-sided"):
	"""Calculate a linear least-squares regression for two sets of measurements.
	x and y must be list of Decimal objects
	The implementation copies that of scipy.linregress.
	Implementation of rvalue, pvalue, slope_stderr is not complete as it is not used in our calculations.
	"""

	xlen = Decimal(len(x))
	ylen = Decimal(len(y))

	if xlen == 0 or ylen == 0:
		raise ValueError("Lists must not be empty.")

	if xlen != ylen:
		raise ValueError("Both lists must be of the same size.")

	dvzero = Decimal("0.0")
	dvone = Decimal("1.0")
	dvtwo = Decimal("2.0")
	dvnegone = Decimal("-1.0")
	dvtiny = Decimal("1.0e-20")

	# Mean value
	xmean = mean(x)
	ymean = mean(y)

	# Average sums of square differences from the mean
	ssxm = mean([(i - xmean) * (i - xmean) for i in x])
	ssym = mean([(i - ymean) * (i - ymean) for i in y])
	ssxym = mean([(x[i] - xmean) * (y[i] - ymean) for i in range(len(x))])

	# R-value
	# rvalue = ssxym / sqrt(ssxm * ssym)
	if ssxm == dvzero or ssym == dvzero:
		rvalue = dvzero
	else:
		rvalue = ssxym / (ssxm * ssym).sqrt()
		# Test for numerical error propagation (make sure -1.0 < rvalue < 1.0)
		if rvalue > dvone:
			rvalue = dvone
		elif rvalue < dvnegone:
			rvalue = dvnegone

	slope = ssxym / ssxm
	intercept = ymean - (slope * xmean)

	if xlen == 2:
		# Handle the case when only two points are passed in
		if y[0] == y[1]:
			pvalue = dvone
		else:
			pvalue = dvzero

		slope_stderr = dvzero
		intercept_stderr = dvzero
	else:
		df = xlen - dvtwo
		t = rvalue * (df / ((dvone - rvalue + dvtiny) * (dvone + rvalue + dvtiny))).sqrt()
		# Not implemented, setting values to zero
		# t, pvalue = ???
		# slope_stderr = (((dvone - (rvalue ** 2)) * ssym / ssxm) / df).sqrt()
		# intercept_stderr = slope_stderr * (ssxm * xmean * xmean).sqrt()
		# Setting values to zero
		pvalue = dvzero
		slope_stderr = dvzero
		intercept_stderr = dvzero

	return slope, intercept, rvalue, pvalue, slope_stderr
