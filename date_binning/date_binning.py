import datetime
from collections import OrderedDict
from decimal import Decimal
from itertools import accumulate, cycle, pairwise

from dateutil.relativedelta import relativedelta


class Period:
	def __init__(self, start_date=None, end_date=None, periodicity="ISO Week"):
		self.start_date = start_date
		self.end_date = end_date
		self.periodicity = periodicity

	def get_iso_start_dates(self, start_date, end_date, step):
		"""
		Returns a list of datetime.date objects representing the starting date of all ISO periods
		falling within the time span defined by `start_date` to `end_date`. If `start_date` is not
		a Monday (the starting weekday for an ISO week), then the first dates in the returned
		sequence will reflect a partial ("stub") week (`start_date` to Sunday). All other dates
		will reflect full periods.

		:param start_date: datetime.date object; the date to start binning from
		:param end_date: datetime.date object; the date to end binning
		:param step: tuple of str, int or sequence of ints; the string indicates the portion of
		the date that is changing via step (this function assumes "weeks"), and the integer or
		sequence of integers is the step for period dates generated within the time span. If
		`step` is a sequence, it will cycle continuously over the values to get the current step
		to collect the start dates of the periods.
		Example: ISO Month (4 + 5 + 4) would use (4, 5, 4) as the `step`, so the returned sequence
		of dates represent months that are 4 ISO weeks, then 5 ISO weeks, then 4 ISO weeks, with
		that pattern continuing through to the `end_date`
		:return: list of datetime.date objects
		"""
		period, delta = step
		r = []

		if type(delta) is int:
			delta = [delta]
		seq = cycle(delta)

		# Check if start_date is first day of period (a Monday), if not, reset it to prior Monday then add step
		if start_date.isoweekday() != 1:
			r.append(start_date)
			start_date = datetime.date.fromisocalendar(
				start_date.isocalendar().year, start_date.isocalendar().week, 1
			) + relativedelta(weeks=next(seq))

		while start_date < end_date:
			r.append(start_date)
			start_date += relativedelta(weeks=next(seq))

		return r

	def get_iso_annual_start_dates(self, start_date, end_date, step):
		"""
		Returns a list of datetime.date objects representing the starting date of all ISO years
		falling within the time span defined by `start_date` to `end_date`. If `start_date` is not
		the first day of that ISO year, the first dates in the returned sequence will reflect a
		partial ("stub") year (`start_date` to year end). All other dates will reflect full
		periods.

		:param start_date: datetime.date object; the date to start binning from
		:param end_date: datetime.date object; the date to end binning
		:param step: tuple of str, int; the string indicates the portion of the date that is
		changing via step, and the integer is the step
		:return: list of datetime.date objects
		"""
		period, delta = step
		r = []
		iso_yr_start_date = datetime.date.fromisocalendar(start_date.year, 1, 1)

		if period != "years":
			raise ValueError(f"A value of {period} was passed, function requires a step based on 'years'.")

		# Start_date falls before the first day of that ISO year
		if start_date < iso_yr_start_date:
			r.append(start_date)
			start_date = iso_yr_start_date
		# Start_date falls after the first day of that ISO year
		elif start_date > iso_yr_start_date:
			r.append(start_date)
			start_date = datetime.date.fromisocalendar(start_date.year + delta, 1, 1)

		while start_date < end_date:
			r.append(start_date)
			start_date = datetime.date.fromisocalendar(start_date.year + delta, 1, 1)

		return r

	def get_cal_start_dates(self, start_date, end_date, step):
		"""
		Returns a list of datetime.date objects representing the starting date of all calendar-
		based periods falling within the time span defined by `start_date` to `end_date`. The step
		tuple is determined by periodicity.

		A step of "days" or "weeks" will not include a "stub" (incomplete) week - the returned
		sequence of dates starts with the given `start_date` and calculates from there.

		:param start_date: datetime.date object; the date to start binning from
		:param end_date: datetime.date object; the date to end binning (non-inclusive)
		:param step: tuple of str, int; the string indicates the portion of the date that is
		changing via step, and the integer is the step
		:return: list of datetime.date objects
		"""
		period, delta = step
		r = []

		if period == "days":
			while start_date < end_date:
				r.append(start_date)
				start_date += relativedelta(days=delta)

		elif period == "weeks":
			while start_date < end_date:
				r.append(start_date)
				start_date += relativedelta(weeks=delta)

		elif period == "months":
			# Check if start_date is first day of period, if not, reset it to prior period start then add step
			if start_date.day != 1:
				r.append(start_date)
				start_date = start_date.replace(day=1) + relativedelta(months=delta)

			while start_date < end_date:
				r.append(start_date)
				start_date += relativedelta(months=delta)

		elif period == "years":
			while start_date < end_date:
				r.append(start_date)
				start_date += relativedelta(years=delta)

		elif period == "years-cy":
			# Check if start_date is first day of period, if not, reset it to prior period start then add step
			if start_date.day != 1 or start_date.month != 1:
				r.append(start_date)
				start_date = start_date.replace(month=1, day=1) + relativedelta(years=delta)

			while start_date < end_date:
				r.append(start_date)
				start_date += relativedelta(years=delta)

		return r

	def get_period_end_dates(self, start_dates):
		"""
		Accepts a sequence of period start dates and adds the period end date for each item, which
		is the day prior to the next start date in the sequence. Assumes the final date is the
		(exclusive) end date for the entire sequence.

		:param start_dates: sequence of datetime.date objects
		:return: list of tuples of datetime.date objects; each tuple represents the start and end
		dates of end-to-end periods
		"""
		# Generate (from, to) period pairs off start dates
		return [(p[0], p[1] + relativedelta(days=-1)) for p in pairwise(start_dates)]

	def get_date_bins(
		self, start_date=None, end_date=None, periodicity=None, inclusive=False, custom_days=None
	):
		"""
		Gets the starting dates for all periods falling within the time span from `start_date` to
		`end_date`, then returns a list of tuples with the start and end dates for each date bin
		spanning the required period.

		:param start_date: datetime.date object; the date to start binning from
		:param end_date: datetime.date object; the date to end binning
		:param periodicity: str | None; determines the binning periods within the time span from
		`start_date` to `end_date`. Default is "ISO Week"

		Supports the following options for `periodicity`. For all ISO periodicity options, if
		`start_date` is not a Monday or the first of an ISO year, the first bin will represent a
		partial ("stub") period. For periodicity options of "Calendar Month", "Calendar Quarter",
		and "Calendar Year", if `start_date` is not the first of that month/year, the first bin
		will represent a partial month/year.
		    - "ISO Week" (default): weekly bins starting on a Monday
		    - "ISO Biweekly": bins of 2 ISO week periods
		    - "ISO Month (4 Weeks)": monthly bins of 4 ISO week periods
		    - "ISO Month (4 + 5 + 4)": monthly bins of ISO week periods following a pattern where
		          the first month is 4 ISO weeks long, the next is 5 ISO weeks long, the next is 4 ISO
		          weeks long, repeating until `end_date`
		    - "ISO Month (4 + 4 + 5)": monthly bins of ISO week periods following a pattern where
		          the first month is 4 ISO weeks long, the next is 4 ISO weeks long, the next is 5 ISO
		          weeks long, repeating until `end_date`
		    - "ISO Quarter (13 Weeks)": quarterly bins of 13 ISO week periods
		    - "ISO Semiannual (26 Weeks)": semiannual bins of 26 ISO week periods
		    - "ISO Annual": bins of full ISO years. If `start_date` is not the first day of the ISO
		          year, the first bin will be a partial year
		        - "Custom Days": bins starting on `start_date` with a number of days between them as
		          given by `custom_days`
		    - "Weekly": weekly bins starting on `start_date`'s weekday
		    - "Biweekly": bins of 2-week periods, starting on `start_date`'s weekday
		    - "Calendar Month": bins by calendar month. If `start_date` is not the first of the
		          month, the first bin will be a partial month
		    - "Calendar Quarter": bins of 3 calendar month periods. If `start_date` is not the
		          first of the month, the first month of the first bin will be a partial month
		    - "Calendar Year": calendar year bins (Jan-Dec). If `start_date`
		          is not Jan 1, the first bin will be a partial year
		    - "Annually": yearly bins starting from `start_date`
		    - "Entire Period": one bin from `start_date` to either `end_date` (if
		          inclusive=True) or the day prior to `end_date` (if inclusive=False)
		:param inclusive: bool; if the time span being binned includes the end_date (inclusive=
		True) or ends the day before (inclusive=False)
		:param custom_days: int | None; number of days per bin, only applicable only if "Custom
		Days" periodicity is selected
		:return: list of tuples in form `(datetime.date object, datetime.date object)`
		"""
		start_date = start_date or self.start_date
		end_date = end_date or self.end_date
		periodicity = periodicity or self.periodicity

		if start_date is None or type(start_date) != datetime.date:
			raise ValueError("Please provide a valid start date.")

		if end_date is None or type(end_date) != datetime.date:
			raise ValueError("Please provide a valid end date.")

		if end_date <= start_date:
			raise ValueError("End date must be after start date.")

		if periodicity == "Custom Days" and not isinstance(custom_days, int):
			raise ValueError("Custom Days periodicity requires an integer value for custom_days.")

		effective_end_date = end_date if not inclusive else end_date + relativedelta(days=1)
		periodicity = self.periodicity if not periodicity else periodicity
		is_iso = "iso" in periodicity.lower()

		steps = {
			"ISO Week": ("weeks", 1),
			"ISO Biweekly": ("weeks", 2),
			"ISO Month (4 Weeks)": ("weeks", 4),
			"ISO Month (4 + 5 + 4)": ("weeks", (4, 5, 4)),
			"ISO Month (4 + 4 + 5)": ("weeks", (4, 4, 5)),
			"ISO Quarter (13 Weeks)": ("weeks", 13),
			"ISO Semiannual (26 Weeks)": ("weeks", 26),
			"ISO Annual": ("years", 1),  # edge case (years can be 52 or 53 weeks)
			"Custom Days": ("days", custom_days),
			"Weekly": ("weeks", 1),
			"Biweekly": ("weeks", 2),
			"Calendar Month": ("months", 1),
			"Calendar Quarter": ("months", 3),
			# assumes Jan-Dec year (accommodates partial years on front or back end)
			"Calendar Year": ("years-cy", 1),
			# assumes 1 year from date given (accommodates non-calendar FYs)
			"Annually": ("years", 1),
		}

		if periodicity == "Entire Period":
			return [(start_date, end_date if inclusive else end_date + relativedelta(days=-1))]

		step = steps.get(periodicity, steps["ISO Week"])

		if is_iso:
			if periodicity == "ISO Annual":
				r = self.get_iso_annual_start_dates(start_date, effective_end_date, step)
			else:
				r = self.get_iso_start_dates(start_date, effective_end_date, step)
		else:
			r = self.get_cal_start_dates(start_date, effective_end_date, step)

		r.append(effective_end_date)
		r = self.get_period_end_dates(r)
		return r

	def convert_dates(self, bins, periodicity="ISO Week", custom_days=None):
		"""
		Converts date bins from their original periodicity into bins for new given `periodicity`
		over the same time span.

		:param bins: list of tuples in form `(datetime.date object, datetime.date object)`
		:param periodicity: str; how to determine the periods within the time span from
		`start_date` to `end_date`. Default is "ISO Week"
		:return: list of tuples in form `(datetime.date object, datetime.date object)`
		"""
		if not bins:
			return []
		start_date = bins[0][0]
		end_date = bins[-1][-1]
		return self.get_date_bins(
			start_date=start_date,
			end_date=end_date,
			periodicity=periodicity,
			inclusive=True,
			custom_days=custom_days,
		)

	def redistribute_data(self, data, bins, periodicity="ISO Week"):
		"""
		Redistributes numeric `data` for the periods specified by `bins` into new date periods
		based on `periodicity`. Returns an OrderedDict where the keys are the new period bins and
		the values are the redistributed data. Assumes data are uniformly distributed over the
		days within the original periods.

		:param data: sequence of numeric data points
		:param bins: list of tuples in form `(datetime.date object, datetime.date object)` that
		represent the date ranges aligning with the given numeric data
		:param periodicity: str; how to determine the periods within the same time span as `bins`.
		Default is "ISO Week"
		:return: OrderedDict; the keys are tuples of datetime.date objects representing the bins
		for the new periodicity, the values are the redistributed numeric data in Decimal format
		"""
		if len(data) != len(bins):
			raise ValueError("Data length must match with bin length.")

		# Build data by day
		n_days = [(b[1] - b[0]).days + 1 for b in bins]
		d_per_day = []
		for d, n in zip([Decimal(d) for d in data], n_days):
			d_per_day += [d / n] * n

		# Get new bins
		new_bins = self.convert_dates(bins, periodicity)

		# Get number of days of new bins and convert to cumulative indices
		indices = accumulate([(b[1] - b[0]).days + 1 for b in new_bins], initial=0)

		# Rebuild data by summing over data by day using cumulative indices as breakpoints
		new_data = [sum(d_per_day[i[0] : i[1]]) for i in pairwise(indices)]

		return OrderedDict(zip(new_bins, new_data))

	def get_period_labels(
		self, bins, periodicity=None, date_format_string="", use_bin_start_date_for_label=True
	):
		"""
		Returns the formatted date labels for the provided bins.

		:param bins: list of tuples in form (datetime.date object, datetime.date object); the date
		bins from which to generate the labels
		:param periodicity: str | None; ignored if `date_format_string` provided, otherwise
		determines the label format for the given `bins`. Uses the class periodicity as a fallback
		:param date_format_string: a custom date format string to apply to the bins to generate
		labels. Can support any Python strftime formatters
		:param use_bin_start_date_for_label: bool; only applies if `date_format_string` provided.
		Date bins are pairs of datetime.date objects that represent the start date and end date of
		each bin. If True, the custom format string is applied to the start date of the pair, if
		False, it's applied the the end date. If `date_format_string` isn't provided, the labels
		use the start date for ISO-based periodicities and the end date for Calendar-based ones
		:return: list of str; the labels for the given date bins

		If `date_format_string` isn't provided, function returns the following built-in formats by
		periodicity:
		- "ISO Week": "Week N-YY" (where N is the ISO week number)
		- "ISO Biweekly": "Weeks N-N YY" (where N-N are the 2 ISO week numbers the bin spans)
		- "ISO Month (4 Weeks)": "MMM-YY"
		- "ISO Month (4 + 5 + 4)": "MMM-YY"
		- "ISO Month (4 + 4 + 5)": "MMM-YY"
		- "ISO Quarter (13 Weeks)": "QN-YY" (where N is 1-4)
		- "ISO Semiannual (26 Weeks)": "HYN-YY" (where N is 1-2)
		- "ISO Annual": "YYYY"
		- "Custom Days": "MM/DD/YY"
		- "Weekly": "MM/DD/YY"
		- "Biweekly": "MM/DD/YY"
		- "Calendar Month": "MMM-YY"
		- "Calendar Quarter": "MM-YYQ"
		- "Calendar Year": "MM/DD/YY"
		- "Annually": "MM/DD/YY"
		- "Entire Period": "MM/DD/YY-MM/DD/YY"
		"""
		periodicity = periodicity or self.periodicity
		date_idx = int(not use_bin_start_date_for_label)

		if not bins:
			return []

		if not periodicity and not date_format_string:
			raise ValueError(
				"Please provide either a periodicity or a custom date format string to generate the period labels."
			)

		if "iso" in periodicity.lower():
			iso_data = [self.get_iso_week_and_year(p[0]) for p in bins]

		if date_format_string:
			return [p[date_idx].strftime(date_format_string) for p in bins]

		# ISO Month, Quarter, and Semiannual labels lookup by week number
		iso_buckets = {
			1: {
				"ISO Month (4 Weeks)": "Jan",
				"ISO Month (4 + 5 + 4)": "Jan",
				"ISO Month (4 + 4 + 5)": "Jan",
				"ISO Quarter (13 Weeks)": "Q1",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			2: {
				"ISO Month (4 Weeks)": "Jan",
				"ISO Month (4 + 5 + 4)": "Jan",
				"ISO Month (4 + 4 + 5)": "Jan",
				"ISO Quarter (13 Weeks)": "Q1",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			3: {
				"ISO Month (4 Weeks)": "Jan",
				"ISO Month (4 + 5 + 4)": "Jan",
				"ISO Month (4 + 4 + 5)": "Jan",
				"ISO Quarter (13 Weeks)": "Q1",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			4: {
				"ISO Month (4 Weeks)": "Jan",
				"ISO Month (4 + 5 + 4)": "Jan",
				"ISO Month (4 + 4 + 5)": "Jan",
				"ISO Quarter (13 Weeks)": "Q1",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			5: {
				"ISO Month (4 Weeks)": "Feb",
				"ISO Month (4 + 5 + 4)": "Feb",
				"ISO Month (4 + 4 + 5)": "Feb",
				"ISO Quarter (13 Weeks)": "Q1",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			6: {
				"ISO Month (4 Weeks)": "Feb",
				"ISO Month (4 + 5 + 4)": "Feb",
				"ISO Month (4 + 4 + 5)": "Feb",
				"ISO Quarter (13 Weeks)": "Q1",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			7: {
				"ISO Month (4 Weeks)": "Feb",
				"ISO Month (4 + 5 + 4)": "Feb",
				"ISO Month (4 + 4 + 5)": "Feb",
				"ISO Quarter (13 Weeks)": "Q1",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			8: {
				"ISO Month (4 Weeks)": "Feb",
				"ISO Month (4 + 5 + 4)": "Feb",
				"ISO Month (4 + 4 + 5)": "Feb",
				"ISO Quarter (13 Weeks)": "Q1",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			9: {
				"ISO Month (4 Weeks)": "Mar",
				"ISO Month (4 + 5 + 4)": "Feb",
				"ISO Month (4 + 4 + 5)": "Mar",
				"ISO Quarter (13 Weeks)": "Q1",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			10: {
				"ISO Month (4 Weeks)": "Mar",
				"ISO Month (4 + 5 + 4)": "Mar",
				"ISO Month (4 + 4 + 5)": "Mar",
				"ISO Quarter (13 Weeks)": "Q1",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			11: {
				"ISO Month (4 Weeks)": "Mar",
				"ISO Month (4 + 5 + 4)": "Mar",
				"ISO Month (4 + 4 + 5)": "Mar",
				"ISO Quarter (13 Weeks)": "Q1",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			12: {
				"ISO Month (4 Weeks)": "Mar",
				"ISO Month (4 + 5 + 4)": "Mar",
				"ISO Month (4 + 4 + 5)": "Mar",
				"ISO Quarter (13 Weeks)": "Q1",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			13: {
				"ISO Month (4 Weeks)": "Apr",
				"ISO Month (4 + 5 + 4)": "Mar",
				"ISO Month (4 + 4 + 5)": "Mar",
				"ISO Quarter (13 Weeks)": "Q1",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			14: {
				"ISO Month (4 Weeks)": "Apr",
				"ISO Month (4 + 5 + 4)": "Apr",
				"ISO Month (4 + 4 + 5)": "Apr",
				"ISO Quarter (13 Weeks)": "Q2",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			15: {
				"ISO Month (4 Weeks)": "Apr",
				"ISO Month (4 + 5 + 4)": "Apr",
				"ISO Month (4 + 4 + 5)": "Apr",
				"ISO Quarter (13 Weeks)": "Q2",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			16: {
				"ISO Month (4 Weeks)": "Apr",
				"ISO Month (4 + 5 + 4)": "Apr",
				"ISO Month (4 + 4 + 5)": "Apr",
				"ISO Quarter (13 Weeks)": "Q2",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			17: {
				"ISO Month (4 Weeks)": "May",
				"ISO Month (4 + 5 + 4)": "Apr",
				"ISO Month (4 + 4 + 5)": "Apr",
				"ISO Quarter (13 Weeks)": "Q2",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			18: {
				"ISO Month (4 Weeks)": "May",
				"ISO Month (4 + 5 + 4)": "May",
				"ISO Month (4 + 4 + 5)": "May",
				"ISO Quarter (13 Weeks)": "Q2",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			19: {
				"ISO Month (4 Weeks)": "May",
				"ISO Month (4 + 5 + 4)": "May",
				"ISO Month (4 + 4 + 5)": "May",
				"ISO Quarter (13 Weeks)": "Q2",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			20: {
				"ISO Month (4 Weeks)": "May",
				"ISO Month (4 + 5 + 4)": "May",
				"ISO Month (4 + 4 + 5)": "May",
				"ISO Quarter (13 Weeks)": "Q2",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			21: {
				"ISO Month (4 Weeks)": "Jun",
				"ISO Month (4 + 5 + 4)": "May",
				"ISO Month (4 + 4 + 5)": "May",
				"ISO Quarter (13 Weeks)": "Q2",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			22: {
				"ISO Month (4 Weeks)": "Jun",
				"ISO Month (4 + 5 + 4)": "May",
				"ISO Month (4 + 4 + 5)": "Jun",
				"ISO Quarter (13 Weeks)": "Q2",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			23: {
				"ISO Month (4 Weeks)": "Jun",
				"ISO Month (4 + 5 + 4)": "Jun",
				"ISO Month (4 + 4 + 5)": "Jun",
				"ISO Quarter (13 Weeks)": "Q2",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			24: {
				"ISO Month (4 Weeks)": "Jun",
				"ISO Month (4 + 5 + 4)": "Jun",
				"ISO Month (4 + 4 + 5)": "Jun",
				"ISO Quarter (13 Weeks)": "Q2",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			25: {
				"ISO Month (4 Weeks)": "Jul",
				"ISO Month (4 + 5 + 4)": "Jun",
				"ISO Month (4 + 4 + 5)": "Jun",
				"ISO Quarter (13 Weeks)": "Q2",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			26: {
				"ISO Month (4 Weeks)": "Jul",
				"ISO Month (4 + 5 + 4)": "Jun",
				"ISO Month (4 + 4 + 5)": "Jun",
				"ISO Quarter (13 Weeks)": "Q2",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			27: {
				"ISO Month (4 Weeks)": "Jul",
				"ISO Month (4 + 5 + 4)": "Jul",
				"ISO Month (4 + 4 + 5)": "Jul",
				"ISO Quarter (13 Weeks)": "Q3",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			28: {
				"ISO Month (4 Weeks)": "Jul",
				"ISO Month (4 + 5 + 4)": "Jul",
				"ISO Month (4 + 4 + 5)": "Jul",
				"ISO Quarter (13 Weeks)": "Q3",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			29: {
				"ISO Month (4 Weeks)": "Aug",
				"ISO Month (4 + 5 + 4)": "Jul",
				"ISO Month (4 + 4 + 5)": "Jul",
				"ISO Quarter (13 Weeks)": "Q3",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			30: {
				"ISO Month (4 Weeks)": "Aug",
				"ISO Month (4 + 5 + 4)": "Jul",
				"ISO Month (4 + 4 + 5)": "Jul",
				"ISO Quarter (13 Weeks)": "Q3",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			31: {
				"ISO Month (4 Weeks)": "Aug",
				"ISO Month (4 + 5 + 4)": "Aug",
				"ISO Month (4 + 4 + 5)": "Aug",
				"ISO Quarter (13 Weeks)": "Q3",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			32: {
				"ISO Month (4 Weeks)": "Aug",
				"ISO Month (4 + 5 + 4)": "Aug",
				"ISO Month (4 + 4 + 5)": "Aug",
				"ISO Quarter (13 Weeks)": "Q3",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			33: {
				"ISO Month (4 Weeks)": "Sep",
				"ISO Month (4 + 5 + 4)": "Aug",
				"ISO Month (4 + 4 + 5)": "Aug",
				"ISO Quarter (13 Weeks)": "Q3",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			34: {
				"ISO Month (4 Weeks)": "Sep",
				"ISO Month (4 + 5 + 4)": "Aug",
				"ISO Month (4 + 4 + 5)": "Aug",
				"ISO Quarter (13 Weeks)": "Q3",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			35: {
				"ISO Month (4 Weeks)": "Sep",
				"ISO Month (4 + 5 + 4)": "Aug",
				"ISO Month (4 + 4 + 5)": "Sep",
				"ISO Quarter (13 Weeks)": "Q3",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			36: {
				"ISO Month (4 Weeks)": "Sep",
				"ISO Month (4 + 5 + 4)": "Sep",
				"ISO Month (4 + 4 + 5)": "Sep",
				"ISO Quarter (13 Weeks)": "Q3",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			37: {
				"ISO Month (4 Weeks)": "Oct",
				"ISO Month (4 + 5 + 4)": "Sep",
				"ISO Month (4 + 4 + 5)": "Sep",
				"ISO Quarter (13 Weeks)": "Q3",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			38: {
				"ISO Month (4 Weeks)": "Oct",
				"ISO Month (4 + 5 + 4)": "Sep",
				"ISO Month (4 + 4 + 5)": "Sep",
				"ISO Quarter (13 Weeks)": "Q3",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			39: {
				"ISO Month (4 Weeks)": "Oct",
				"ISO Month (4 + 5 + 4)": "Sep",
				"ISO Month (4 + 4 + 5)": "Sep",
				"ISO Quarter (13 Weeks)": "Q3",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			40: {
				"ISO Month (4 Weeks)": "Oct",
				"ISO Month (4 + 5 + 4)": "Oct",
				"ISO Month (4 + 4 + 5)": "Oct",
				"ISO Quarter (13 Weeks)": "Q4",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			41: {
				"ISO Month (4 Weeks)": "Nov",
				"ISO Month (4 + 5 + 4)": "Oct",
				"ISO Month (4 + 4 + 5)": "Oct",
				"ISO Quarter (13 Weeks)": "Q4",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			42: {
				"ISO Month (4 Weeks)": "Nov",
				"ISO Month (4 + 5 + 4)": "Oct",
				"ISO Month (4 + 4 + 5)": "Oct",
				"ISO Quarter (13 Weeks)": "Q4",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			43: {
				"ISO Month (4 Weeks)": "Nov",
				"ISO Month (4 + 5 + 4)": "Oct",
				"ISO Month (4 + 4 + 5)": "Oct",
				"ISO Quarter (13 Weeks)": "Q4",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			44: {
				"ISO Month (4 Weeks)": "Nov",
				"ISO Month (4 + 5 + 4)": "Nov",
				"ISO Month (4 + 4 + 5)": "Nov",
				"ISO Quarter (13 Weeks)": "Q4",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			45: {
				"ISO Month (4 Weeks)": "Dec",
				"ISO Month (4 + 5 + 4)": "Nov",
				"ISO Month (4 + 4 + 5)": "Nov",
				"ISO Quarter (13 Weeks)": "Q4",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			46: {
				"ISO Month (4 Weeks)": "Dec",
				"ISO Month (4 + 5 + 4)": "Nov",
				"ISO Month (4 + 4 + 5)": "Nov",
				"ISO Quarter (13 Weeks)": "Q4",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			47: {
				"ISO Month (4 Weeks)": "Dec",
				"ISO Month (4 + 5 + 4)": "Nov",
				"ISO Month (4 + 4 + 5)": "Nov",
				"ISO Quarter (13 Weeks)": "Q4",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			48: {
				"ISO Month (4 Weeks)": "Dec",
				"ISO Month (4 + 5 + 4)": "Nov",
				"ISO Month (4 + 4 + 5)": "Dec",
				"ISO Quarter (13 Weeks)": "Q4",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			49: {
				"ISO Month (4 Weeks)": "M13",
				"ISO Month (4 + 5 + 4)": "Dec",
				"ISO Month (4 + 4 + 5)": "Dec",
				"ISO Quarter (13 Weeks)": "Q4",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			50: {
				"ISO Month (4 Weeks)": "M13",
				"ISO Month (4 + 5 + 4)": "Dec",
				"ISO Month (4 + 4 + 5)": "Dec",
				"ISO Quarter (13 Weeks)": "Q4",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			51: {
				"ISO Month (4 Weeks)": "M13",
				"ISO Month (4 + 5 + 4)": "Dec",
				"ISO Month (4 + 4 + 5)": "Dec",
				"ISO Quarter (13 Weeks)": "Q4",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			52: {
				"ISO Month (4 Weeks)": "M13",
				"ISO Month (4 + 5 + 4)": "Dec",
				"ISO Month (4 + 4 + 5)": "Dec",
				"ISO Quarter (13 Weeks)": "Q4",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			53: {
				"ISO Month (4 Weeks)": "M13",
				"ISO Month (4 + 5 + 4)": "Dec",
				"ISO Month (4 + 4 + 5)": "Dec",
				"ISO Quarter (13 Weeks)": "Q4",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
		}

		# Entire period
		if periodicity == "Entire Period":
			# Returns format: "MM/DD/YY-MM/DD/YY"
			p = bins[0]
			return [f"{p[0].strftime('%m/%d/%y')}-{p[1].strftime('%m/%d/%y')}"]

		# ISO-based periodicity - labels created off the start date from each bin
		elif periodicity == "ISO Week":
			# Returns format: "Week N-YY"
			return [f"Week {iso_w}-{str(iso_y)[-2:]}" for iso_w, iso_y in iso_data]
		elif periodicity == "ISO Biweekly":
			# Returns format: "Weeks N-N YY"
			return [f"Weeks {iso_w}-{iso_w + 1} {str(iso_y)[-2:]}" for iso_w, iso_y in iso_data]
		elif periodicity == "ISO Annual":
			# Returns format: "YYYY"
			return [f"{iso_y}" for iso_w, iso_y in iso_data]
		elif "ISO" in periodicity:
			# Returns format: "MMM-YY", "QN-YY", or "HYN-YY" for month, quarter, or semiannual periodicity
			return [f"{iso_buckets[iso_w][periodicity]}-{str(iso_y)[-2:]}" for iso_w, iso_y in iso_data]

		# Calendar-based periodicity - labels created off the end date from each bin
		elif periodicity == "Calendar Month":
			# Returns format: "MMM-YY"
			return [p[1].strftime("%b-%y") for p in bins]
		elif periodicity == "Calendar Quarter":
			# Returns format: "MM-YYQ"
			return [f"{p[1].strftime('%m-%y')}Q" for p in bins]
		else:  # periodicity in ("Custom Days", "Weekly", "Biweekly", "Calendar Year", "Annually")
			# Returns format: "MM/DD/YY"
			return [p[1].strftime("%m/%d/%y") for p in bins]

	def get_iso_week_and_year(self, date):
		"""
		Given a datetime.date object, returns the ISO week and ISO year.

		:param date: datetime.date object
		:return: tuple (int, int); (ISO week, ISO year) for given date
		"""
		dt = datetime.datetime.combine(date, datetime.time())
		iso_date = dt.isocalendar()
		return iso_date.week, iso_date.year
