# Copyright (c) 2024, AgriTheory and contributors
# For license information, please see license.txt"


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

		self.date_math_patterns = {
			# ISO pattern: [ISO week number period break points]
			"ISO Week": list(range(1, 54)),
			"ISO Biweekly": list(range(1, 54, 2)),
			"ISO Month (4 Weeks)": [1, 5, 9, 13, 17, 21, 25, 29, 33, 37, 41, 45, 49],
			"ISO Month (4 + 5 + 4)": [1, 5, 10, 14, 18, 23, 27, 31, 36, 40, 44, 49],
			"ISO Month (4 + 4 + 5)": [1, 5, 9, 14, 18, 22, 27, 31, 35, 40, 44, 48],
			"ISO Quarter (13 Weeks)": [1, 14, 27, 40],
			"ISO Semiannual (26 Weeks)": [1, 27],
			"ISO Annual": [1],
			# Calendar pattern: (date part to increment, step to increment by)
			# "Custom Days" and "Fiscal Weeks" updated in get_date_bins as needed
			"Custom Days": ("days", 1),
			"Weekly": ("weeks", 1),
			"Biweekly": ("weeks", 2),
			"Fiscal Weeks": ("weeks", 1),
			"Calendar Month": ("months", 1),
			"Monthly": ("months", 1),
			"Calendar Quarter": ("months", 3),
			"Quarterly": ("months", 3),
			"Calendar Year": ("years", 1),
			"Annually": ("years", 1),
		}

	def _get_iso_week_pattern(self, start_date: datetime.date, periodicity: str) -> list[int]:
		iso_week = start_date.isocalendar().week
		pattern = self.date_math_patterns[periodicity]

		# Split pattern based on where start_date falls so cycle starts with the next period
		index = 0
		for i, n in enumerate(pattern):
			if iso_week < n:
				index = i
				break
		return pattern[index:] + pattern[:index]

	def _get_iso_start_dates(
		self, start_date: datetime.date, end_date: datetime.date, periodicity: str
	) -> list[datetime.date]:
		"""
		Returns a list of datetime.date objects representing the starting date of all ISO periods
		falling within the time span defined by `start_date` to `end_date`. If `start_date` is not
		a Monday (the starting weekday for an ISO week), then the first dates in the returned
		sequence will reflect a partial ("stub") week (`start_date` to Sunday). Likewise if
		`end_date` is not a Sunday. All other dates will reflect full periods.

		:param start_date: the date from which to start binning
		:param end_date: the date to which to end binning
		:param periodicity: determines the binning periods within the time span from `start_date`
		to `end_date`
		:return: list bin start dates
		"""
		r = []
		pattern = self._get_iso_week_pattern(start_date, periodicity)
		seq = cycle(pattern)
		iso_year = start_date.isocalendar().year

		while start_date < end_date:
			r.append(start_date)
			week = next(seq)

			# Advance year if pattern wraps
			if start_date.isocalendar().week > week or periodicity == "ISO Annual":
				iso_year += 1

			try:
				start_date = datetime.date.fromisocalendar(iso_year, week, 1)
			except ValueError:
				# No W53 in current year (weekly calcs only) - advance pattern and increment year
				week = next(seq)
				iso_year += 1
				start_date = datetime.date.fromisocalendar(iso_year, week, 1)

		return r

	def _get_current_quarter_start(self, date: datetime.date) -> datetime.date:
		"""
		Given a `date`, finds the calendar quarter it falls in and returns that quarter's starting
		date.

		:param date: the date to use to find the quarter start date
		:return: the start date of the quarter `date` falls in
		"""
		cy = date.year
		calendar_quarters = [
			(datetime.date(cy, 1, 1), datetime.date(cy, 3, 31)),
			(datetime.date(cy, 4, 1), datetime.date(cy, 6, 30)),
			(datetime.date(cy, 7, 1), datetime.date(cy, 9, 30)),
			(datetime.date(cy, 10, 1), datetime.date(cy, 12, 31)),
		]
		for sq, eq in calendar_quarters:
			if date <= eq:
				result = sq
				break

		return result

	def _get_cal_start_dates(
		self, start_date: datetime.date, end_date: datetime.date, periodicity: str
	) -> list[datetime.date]:
		"""
		Returns a list of datetime.date objects representing the starting date of all calendar-
		based periods (per periodicity) falling within the time span defined by `start_date` to
		`end_date`.

		A step of "days", "weeks", or "months" will not include a "stub" (incomplete) week - the
		returned sequence of dates starts with the given `start_date` and calculates from there.

		:param start_date: the date from which to start binning
		:param end_date: the date to which to end binning
		:param periodicity: determines the binning periods within the time span from `start_date`
		to `end_date`
		:return: list bin start dates
		"""
		period, delta = self.date_math_patterns[periodicity]
		delta = [delta] if isinstance(delta, int) else delta
		seq = cycle(delta)

		r = []

		if period == "days":
			while start_date < end_date:
				r.append(start_date)
				start_date += relativedelta(days=next(seq))

		elif period == "weeks":
			while start_date < end_date:
				r.append(start_date)
				start_date += relativedelta(weeks=next(seq))

		# For "Calendar" periodicities, adjust start_date before incrementing if not first day of period
		elif period == "months":
			if periodicity == "Calendar Month" and start_date.day != 1:
				r.append(start_date)
				start_date = start_date.replace(day=1) + relativedelta(months=next(seq))
			elif periodicity == "Calendar Quarter":
				r.append(start_date)
				start_date = self._get_current_quarter_start(start_date) + relativedelta(months=next(seq))

			while start_date < end_date:
				r.append(start_date)
				start_date += relativedelta(months=next(seq))

		elif period == "years":
			if periodicity == "Calendar Year" and (start_date.day != 1 or start_date.month != 1):
				r.append(start_date)
				start_date = start_date.replace(month=1, day=1) + relativedelta(years=next(seq))

			while start_date < end_date:
				r.append(start_date)
				start_date += relativedelta(years=next(seq))

		return r

	def _get_period_end_dates(
		self, start_dates: list[datetime.date]
	) -> list[tuple[datetime.date, datetime.date]]:
		"""
		Accepts a sequence of period start dates and adds the period end date for each item, which
		is the day prior to the next start date in the sequence. Assumes the final date is the
		(exclusive) end date for the entire sequence.

		:param start_dates: sequence of datetime.date objects
		:return: list of tuples of datetime.date objects; each tuple represents the start and end
		dates of end-to-end periods
		"""
		# Generate (from, to) period pairs off start dates
		return [(p[0], p[1] - relativedelta(days=1)) for p in pairwise(start_dates)]

	def get_date_bins(
		self,
		start_date: datetime.date | None = None,
		end_date: datetime.date | None = None,
		periodicity: str | None = None,
		inclusive: bool = True,
		custom_period: int | list[int] = 1,
	) -> list[tuple[datetime.date, datetime.date]]:
		"""
		Gets the starting dates for all periods falling within the time span from `start_date` to
		`end_date`, then returns a list of tuples with the start and end dates for each date bin
		spanning the required period.

		:param start_date: the date from which to start binning
		:param end_date: the date to which to end binning
		:param periodicity: determines the binning periods within the time span from `start_date`
		to `end_date`. If None, uses class periodicity (default is "ISO Week")

		Supports the following options for `periodicity`. For all "ISO" periodicity options, if
		`start_date` is not a Monday or the first of that ISO period, the first bin will represent
		a stub period. For "Calendar" periodicity options, if `start_date` is not the first of
		that month/quarter/year, the first bin will represent a stub period. For other periodicity
		options, there's no concept of a stub period - it starts binning with `start_date` and
		increments from there.
		    - "ISO Week" (default): weekly bins starting on a Monday
		    - "ISO Biweekly": bins of 2 ISO week periods
		    - "ISO Month (4 Weeks)": monthly bins of 4 ISO week periods assuming ISO weeks are put
		    in months with a pattern of 4 weeks each
		    - "ISO Month (4 + 5 + 4)": monthly bins of ISO week periods assuming ISO weeks are put
		    in months with a pattern of 4 weeks, 5 weeks, then 4 weeks, repeating
		    - "ISO Month (4 + 4 + 5)": monthly bins of ISO week periods assuming ISO weeks are put
		    n months with a pattern of 4 weeks, 4 weeks, then 5 weeks, repeating
		    - "ISO Quarter (13 Weeks)": quarterly bins of 13 ISO week periods
		    - "ISO Semiannual (26 Weeks)": semiannual bins of 26 ISO week periods
		    - "ISO Annual": bins by ISO year
		    - "Custom Days": bins starting on `start_date` with a number of days between them as
		    given by `custom_period` (may be a single integer or sequence that's cycled over). The
		        default value is 1 to produce daily bins
		    - "Weekly": weekly bins starting on `start_date`'s weekday
		    - "Biweekly": bins of 2-week periods, starting on `start_date`'s weekday
		    - "Fiscal Weeks": bins starting on `start_date` with a number of weeks between them as
		    given by `custom_period` (may be a single integer or sequence that's cycled over). The
		        default value is 1 to produce weekly bins
		    - "Calendar Month": bins by calendar month
		    - "Monthly": monthly bins starting on `start_date`
		    - "Calendar Quarter": bins of 3-month periods based on a calendar year (Jan-Mar, Apr-
		    Jun, etc.)
		    - "Quarterly": bins of 3-month periods starting on `start_date`
		    - "Calendar Year": calendar year bins (Jan-Dec)
		    - "Annually": yearly bins starting from `start_date`
		    - "Entire Period": one bin from `start_date` to either `end_date` (if
		    inclusive=True) or the day prior to `end_date` (if inclusive=False)
		:param inclusive: if resulting bins include the end_date (inclusive=True) or ends the day
		before (inclusive=False)
		:param custom_period: a single or sequence of integers that specifies the number of days
		(for "Custom Days") or weeks (for "Fiscal Weeks") in a bin. Ignored for other periodicity
		options
		:return: list of tuples in form `(datetime.date object, datetime.date object)`
		"""
		start_date = start_date or self.start_date
		end_date = end_date or self.end_date
		periodicity = periodicity or self.periodicity

		if start_date is None or not isinstance(start_date, datetime.date):
			raise ValueError("Please provide a valid start date.")

		if end_date is None or not isinstance(end_date, datetime.date):
			raise ValueError("Please provide a valid end date.")

		if end_date <= start_date:
			raise ValueError("End date must be after start date.")

		if periodicity in ["Custom Days", "Fiscal Weeks"]:
			if not (isinstance(custom_period, int) or isinstance(custom_period, list)) or (
				isinstance(custom_period, list) and not all([isinstance(n, int) for n in custom_period])
			):
				raise ValueError("custom_period must be an integer or list of integers.")

			if isinstance(custom_period, int) and custom_period < 1:
				raise ValueError(f"{periodicity} periodicity requires an integer value > 0 for custom_period.")

			if isinstance(custom_period, list) and any([n < 1 for n in custom_period]):
				raise ValueError(f"{periodicity} periodicity requires integer values > 0 for custom_period.")

		effective_end_date = end_date if not inclusive else end_date + relativedelta(days=1)
		is_iso = "iso" in periodicity.lower()

		if periodicity == "Custom Days":
			self.date_math_patterns.update({"Custom Days": ("days", custom_period)})

		if periodicity == "Fiscal Weeks":
			self.date_math_patterns.update({"Fiscal Weeks": ("weeks", custom_period)})

		if periodicity == "Entire Period":
			return [(start_date, end_date if inclusive else end_date - relativedelta(days=1))]

		if is_iso:
			r = self._get_iso_start_dates(start_date, effective_end_date, periodicity)
		else:
			r = self._get_cal_start_dates(start_date, effective_end_date, periodicity)

		r.append(effective_end_date)
		results = self._get_period_end_dates(r)
		return results

	def convert_dates(
		self,
		bins: list[tuple[datetime.date, datetime.date]],
		periodicity: str = "ISO Week",
		custom_period: int | list[int] = 1,
	) -> list[tuple[datetime.date, datetime.date]]:
		"""
		Converts date bins from their original periodicity into bins for new given `periodicity`
		over the same time span.

		:param bins: list of tuples in form `(datetime.date object, datetime.date object)`
		:param periodicity: str; how to determine the periods within the time span from
		`start_date` to `end_date`. Default is "ISO Week"
		:param custom_period: a single or sequence of integers that specifies the number of days
		(for "Custom Days") or weeks (for "Fiscal Weeks") in a bin. Ignored for other periodicity
		options
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
			custom_period=custom_period,
		)

	def redistribute_data(
		self,
		data,
		bins: list[tuple[datetime.date, datetime.date]],
		periodicity: str = "ISO Week",
		custom_period: int | list[int] = 1,
	):
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
		:param custom_period: a single or sequence of integers that specifies the number of days
		(for "Custom Days") or weeks (for "Fiscal Weeks") in a bin. Ignored for other periodicity
		options
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
		new_bins = self.convert_dates(bins, periodicity, custom_period)

		# Get number of days of new bins and convert to cumulative indices
		indices = accumulate([(b[1] - b[0]).days + 1 for b in new_bins], initial=0)

		# Rebuild data by summing over data by day using cumulative indices as breakpoints
		new_data = [sum(d_per_day[i[0] : i[1]]) for i in pairwise(indices)]

		return OrderedDict(zip(new_bins, new_data))

	def get_period_labels(
		self,
		bins: list[tuple[datetime.date, datetime.date]],
		periodicity: str | None = None,
		date_format_string: str = "",
		use_bin_start_date_for_label: bool | None = None,
	) -> list[str]:
		"""
		Returns the formatted date labels for the provided bins.

		:param bins: list of tuples in form (datetime.date object, datetime.date object); the date
		bins from which to generate the labels
		:param periodicity: ignored if `date_format_string` provided, otherwise determines the
		label format for the given `bins`. Uses the class periodicity as a fallback
		:param date_format_string: a custom date format string to apply to the bins to generate
		labels. Can support any Python strftime formatters
		:param use_bin_start_date_for_label: Date bins are pairs of datetime.date objects that
		represent the start date and end date of each bin. If True, it uses the bin's start date
		to create the label, if False it uses the bin's end date. If None, it uses the start date
		for any ISO-based periodicity and it uses the end date for all other periodicity options
		:return: the labels for the given date bins

		If `date_format_string` isn't provided, function returns the following built-in formats by
		periodicity:
		- "ISO Week": "Week N-YY" (where N is the ISO week number)
		- "ISO Biweekly": "Weeks N-N YY" (where N-N are the 2 ISO week numbers the bin spans)
		- "ISO Month (4 Weeks)": "MMM (4w)-YY"
		- "ISO Month (4 + 5 + 4)": "MMM (Nw)-YY" (where N is the number of weeks in the month)
		- "ISO Month (4 + 4 + 5)": "MMM (Nw)-YY" (where N is the number of weeks in the month)
		- "ISO Quarter (13 Weeks)": "QN-YY" (where N is 1-4)
		- "ISO Semiannual (26 Weeks)": "HYN-YY" (where N is 1-2)
		- "ISO Annual": "YYYY"
		- "Custom Days": "MM/DD/YY"
		- "Weekly": "MM/DD/YY"
		- "Biweekly": "MM/DD/YY"
		- "Fiscal Weeks": "I (Nw)-YY" (where I is the 1-based bin index, N is the number of weeks
		in the bin group), the year is calculated per `use_bin_start_date_for_label`
		- "Calendar Month": "MMM-YY"
		- "Calendar Quarter": "MM-YYQ"
		- "Calendar Year": "MM/DD/YY"
		- "Annually": "MM/DD/YY"
		- "Entire Period": "MM/DD/YY-MM/DD/YY"
		"""
		periodicity = periodicity or self.periodicity
		is_iso = "iso" in periodicity.lower()
		date_idx = (
			int(not is_iso)
			if use_bin_start_date_for_label is None
			else int(not use_bin_start_date_for_label)
		)

		if not bins:
			return []

		if is_iso:
			iso_data: list[tuple[int, int]] = [self._get_iso_week_and_year(p[date_idx]) for p in bins]

		if date_format_string:
			return [p[date_idx].strftime(date_format_string) for p in bins]

		# ISO Month, Quarter, and Semiannual labels lookup by week number
		iso_buckets = {
			1: {
				"ISO Month (4 Weeks)": "Jan (4w)",
				"ISO Month (4 + 5 + 4)": "Jan (4w)",
				"ISO Month (4 + 4 + 5)": "Jan (4w)",
				"ISO Quarter (13 Weeks)": "Q1",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			2: {
				"ISO Month (4 Weeks)": "Jan (4w)",
				"ISO Month (4 + 5 + 4)": "Jan (4w)",
				"ISO Month (4 + 4 + 5)": "Jan (4w)",
				"ISO Quarter (13 Weeks)": "Q1",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			3: {
				"ISO Month (4 Weeks)": "Jan (4w)",
				"ISO Month (4 + 5 + 4)": "Jan (4w)",
				"ISO Month (4 + 4 + 5)": "Jan (4w)",
				"ISO Quarter (13 Weeks)": "Q1",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			4: {
				"ISO Month (4 Weeks)": "Jan (4w)",
				"ISO Month (4 + 5 + 4)": "Jan (4w)",
				"ISO Month (4 + 4 + 5)": "Jan (4w)",
				"ISO Quarter (13 Weeks)": "Q1",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			5: {
				"ISO Month (4 Weeks)": "Feb (4w)",
				"ISO Month (4 + 5 + 4)": "Feb (5w)",
				"ISO Month (4 + 4 + 5)": "Feb (4w)",
				"ISO Quarter (13 Weeks)": "Q1",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			6: {
				"ISO Month (4 Weeks)": "Feb (4w)",
				"ISO Month (4 + 5 + 4)": "Feb (5w)",
				"ISO Month (4 + 4 + 5)": "Feb (4w)",
				"ISO Quarter (13 Weeks)": "Q1",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			7: {
				"ISO Month (4 Weeks)": "Feb (4w)",
				"ISO Month (4 + 5 + 4)": "Feb (5w)",
				"ISO Month (4 + 4 + 5)": "Feb (4w)",
				"ISO Quarter (13 Weeks)": "Q1",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			8: {
				"ISO Month (4 Weeks)": "Feb (4w)",
				"ISO Month (4 + 5 + 4)": "Feb (5w)",
				"ISO Month (4 + 4 + 5)": "Feb (4w)",
				"ISO Quarter (13 Weeks)": "Q1",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			9: {
				"ISO Month (4 Weeks)": "Mar (4w)",
				"ISO Month (4 + 5 + 4)": "Feb (5w)",
				"ISO Month (4 + 4 + 5)": "Mar (5w)",
				"ISO Quarter (13 Weeks)": "Q1",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			10: {
				"ISO Month (4 Weeks)": "Mar (4w)",
				"ISO Month (4 + 5 + 4)": "Mar (4w)",
				"ISO Month (4 + 4 + 5)": "Mar (5w)",
				"ISO Quarter (13 Weeks)": "Q1",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			11: {
				"ISO Month (4 Weeks)": "Mar (4w)",
				"ISO Month (4 + 5 + 4)": "Mar (4w)",
				"ISO Month (4 + 4 + 5)": "Mar (5w)",
				"ISO Quarter (13 Weeks)": "Q1",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			12: {
				"ISO Month (4 Weeks)": "Mar (4w)",
				"ISO Month (4 + 5 + 4)": "Mar (4w)",
				"ISO Month (4 + 4 + 5)": "Mar (5w)",
				"ISO Quarter (13 Weeks)": "Q1",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			13: {
				"ISO Month (4 Weeks)": "Apr (4w)",
				"ISO Month (4 + 5 + 4)": "Mar (4w)",
				"ISO Month (4 + 4 + 5)": "Mar (5w)",
				"ISO Quarter (13 Weeks)": "Q1",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			14: {
				"ISO Month (4 Weeks)": "Apr (4w)",
				"ISO Month (4 + 5 + 4)": "Apr (4w)",
				"ISO Month (4 + 4 + 5)": "Apr (4w)",
				"ISO Quarter (13 Weeks)": "Q2",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			15: {
				"ISO Month (4 Weeks)": "Apr (4w)",
				"ISO Month (4 + 5 + 4)": "Apr (4w)",
				"ISO Month (4 + 4 + 5)": "Apr (4w)",
				"ISO Quarter (13 Weeks)": "Q2",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			16: {
				"ISO Month (4 Weeks)": "Apr (4w)",
				"ISO Month (4 + 5 + 4)": "Apr (4w)",
				"ISO Month (4 + 4 + 5)": "Apr (4w)",
				"ISO Quarter (13 Weeks)": "Q2",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			17: {
				"ISO Month (4 Weeks)": "May (4w)",
				"ISO Month (4 + 5 + 4)": "Apr (4w)",
				"ISO Month (4 + 4 + 5)": "Apr (4w)",
				"ISO Quarter (13 Weeks)": "Q2",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			18: {
				"ISO Month (4 Weeks)": "May (4w)",
				"ISO Month (4 + 5 + 4)": "May (5w)",
				"ISO Month (4 + 4 + 5)": "May (4w)",
				"ISO Quarter (13 Weeks)": "Q2",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			19: {
				"ISO Month (4 Weeks)": "May (4w)",
				"ISO Month (4 + 5 + 4)": "May (5w)",
				"ISO Month (4 + 4 + 5)": "May (4w)",
				"ISO Quarter (13 Weeks)": "Q2",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			20: {
				"ISO Month (4 Weeks)": "May (4w)",
				"ISO Month (4 + 5 + 4)": "May (5w)",
				"ISO Month (4 + 4 + 5)": "May (4w)",
				"ISO Quarter (13 Weeks)": "Q2",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			21: {
				"ISO Month (4 Weeks)": "Jun (4w)",
				"ISO Month (4 + 5 + 4)": "May (5w)",
				"ISO Month (4 + 4 + 5)": "May (4w)",
				"ISO Quarter (13 Weeks)": "Q2",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			22: {
				"ISO Month (4 Weeks)": "Jun (4w)",
				"ISO Month (4 + 5 + 4)": "May (5w)",
				"ISO Month (4 + 4 + 5)": "Jun (5w)",
				"ISO Quarter (13 Weeks)": "Q2",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			23: {
				"ISO Month (4 Weeks)": "Jun (4w)",
				"ISO Month (4 + 5 + 4)": "Jun (4w)",
				"ISO Month (4 + 4 + 5)": "Jun (5w)",
				"ISO Quarter (13 Weeks)": "Q2",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			24: {
				"ISO Month (4 Weeks)": "Jun (4w)",
				"ISO Month (4 + 5 + 4)": "Jun (4w)",
				"ISO Month (4 + 4 + 5)": "Jun (5w)",
				"ISO Quarter (13 Weeks)": "Q2",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			25: {
				"ISO Month (4 Weeks)": "Jul (4w)",
				"ISO Month (4 + 5 + 4)": "Jun (4w)",
				"ISO Month (4 + 4 + 5)": "Jun (5w)",
				"ISO Quarter (13 Weeks)": "Q2",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			26: {
				"ISO Month (4 Weeks)": "Jul (4w)",
				"ISO Month (4 + 5 + 4)": "Jun (4w)",
				"ISO Month (4 + 4 + 5)": "Jun (5w)",
				"ISO Quarter (13 Weeks)": "Q2",
				"ISO Semiannual (26 Weeks)": "HY1",
			},
			27: {
				"ISO Month (4 Weeks)": "Jul (4w)",
				"ISO Month (4 + 5 + 4)": "Jul (4w)",
				"ISO Month (4 + 4 + 5)": "Jul (4w)",
				"ISO Quarter (13 Weeks)": "Q3",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			28: {
				"ISO Month (4 Weeks)": "Jul (4w)",
				"ISO Month (4 + 5 + 4)": "Jul (4w)",
				"ISO Month (4 + 4 + 5)": "Jul (4w)",
				"ISO Quarter (13 Weeks)": "Q3",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			29: {
				"ISO Month (4 Weeks)": "Aug (4w)",
				"ISO Month (4 + 5 + 4)": "Jul (4w)",
				"ISO Month (4 + 4 + 5)": "Jul (4w)",
				"ISO Quarter (13 Weeks)": "Q3",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			30: {
				"ISO Month (4 Weeks)": "Aug (4w)",
				"ISO Month (4 + 5 + 4)": "Jul (4w)",
				"ISO Month (4 + 4 + 5)": "Jul (4w)",
				"ISO Quarter (13 Weeks)": "Q3",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			31: {
				"ISO Month (4 Weeks)": "Aug (4w)",
				"ISO Month (4 + 5 + 4)": "Aug (5w)",
				"ISO Month (4 + 4 + 5)": "Aug (4w)",
				"ISO Quarter (13 Weeks)": "Q3",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			32: {
				"ISO Month (4 Weeks)": "Aug (4w)",
				"ISO Month (4 + 5 + 4)": "Aug (5w)",
				"ISO Month (4 + 4 + 5)": "Aug (4w)",
				"ISO Quarter (13 Weeks)": "Q3",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			33: {
				"ISO Month (4 Weeks)": "Sep (4w)",
				"ISO Month (4 + 5 + 4)": "Aug (5w)",
				"ISO Month (4 + 4 + 5)": "Aug (4w)",
				"ISO Quarter (13 Weeks)": "Q3",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			34: {
				"ISO Month (4 Weeks)": "Sep (4w)",
				"ISO Month (4 + 5 + 4)": "Aug (5w)",
				"ISO Month (4 + 4 + 5)": "Aug (4w)",
				"ISO Quarter (13 Weeks)": "Q3",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			35: {
				"ISO Month (4 Weeks)": "Sep (4w)",
				"ISO Month (4 + 5 + 4)": "Aug (5w)",
				"ISO Month (4 + 4 + 5)": "Sep (5w)",
				"ISO Quarter (13 Weeks)": "Q3",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			36: {
				"ISO Month (4 Weeks)": "Sep (4w)",
				"ISO Month (4 + 5 + 4)": "Sep (4w)",
				"ISO Month (4 + 4 + 5)": "Sep (5w)",
				"ISO Quarter (13 Weeks)": "Q3",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			37: {
				"ISO Month (4 Weeks)": "Oct (4w)",
				"ISO Month (4 + 5 + 4)": "Sep (4w)",
				"ISO Month (4 + 4 + 5)": "Sep (5w)",
				"ISO Quarter (13 Weeks)": "Q3",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			38: {
				"ISO Month (4 Weeks)": "Oct (4w)",
				"ISO Month (4 + 5 + 4)": "Sep (4w)",
				"ISO Month (4 + 4 + 5)": "Sep (5w)",
				"ISO Quarter (13 Weeks)": "Q3",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			39: {
				"ISO Month (4 Weeks)": "Oct (4w)",
				"ISO Month (4 + 5 + 4)": "Sep (4w)",
				"ISO Month (4 + 4 + 5)": "Sep (5w)",
				"ISO Quarter (13 Weeks)": "Q3",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			40: {
				"ISO Month (4 Weeks)": "Oct (4w)",
				"ISO Month (4 + 5 + 4)": "Oct (4w)",
				"ISO Month (4 + 4 + 5)": "Oct (4w)",
				"ISO Quarter (13 Weeks)": "Q4",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			41: {
				"ISO Month (4 Weeks)": "Nov (4w)",
				"ISO Month (4 + 5 + 4)": "Oct (4w)",
				"ISO Month (4 + 4 + 5)": "Oct (4w)",
				"ISO Quarter (13 Weeks)": "Q4",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			42: {
				"ISO Month (4 Weeks)": "Nov (4w)",
				"ISO Month (4 + 5 + 4)": "Oct (4w)",
				"ISO Month (4 + 4 + 5)": "Oct (4w)",
				"ISO Quarter (13 Weeks)": "Q4",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			43: {
				"ISO Month (4 Weeks)": "Nov (4w)",
				"ISO Month (4 + 5 + 4)": "Oct (4w)",
				"ISO Month (4 + 4 + 5)": "Oct (4w)",
				"ISO Quarter (13 Weeks)": "Q4",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			44: {
				"ISO Month (4 Weeks)": "Nov (4w)",
				"ISO Month (4 + 5 + 4)": "Nov (5w)",
				"ISO Month (4 + 4 + 5)": "Nov (4w)",
				"ISO Quarter (13 Weeks)": "Q4",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			45: {
				"ISO Month (4 Weeks)": "Dec (4w)",
				"ISO Month (4 + 5 + 4)": "Nov (5w)",
				"ISO Month (4 + 4 + 5)": "Nov (4w)",
				"ISO Quarter (13 Weeks)": "Q4",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			46: {
				"ISO Month (4 Weeks)": "Dec (4w)",
				"ISO Month (4 + 5 + 4)": "Nov (5w)",
				"ISO Month (4 + 4 + 5)": "Nov (4w)",
				"ISO Quarter (13 Weeks)": "Q4",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			47: {
				"ISO Month (4 Weeks)": "Dec (4w)",
				"ISO Month (4 + 5 + 4)": "Nov (5w)",
				"ISO Month (4 + 4 + 5)": "Nov (4w)",
				"ISO Quarter (13 Weeks)": "Q4",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			48: {
				"ISO Month (4 Weeks)": "Dec (4w)",
				"ISO Month (4 + 5 + 4)": "Nov (5w)",
				"ISO Month (4 + 4 + 5)": "Dec (5w)",
				"ISO Quarter (13 Weeks)": "Q4",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			49: {
				"ISO Month (4 Weeks)": "M13 (4w)",
				"ISO Month (4 + 5 + 4)": "Dec (4w)",
				"ISO Month (4 + 4 + 5)": "Dec (5w)",
				"ISO Quarter (13 Weeks)": "Q4",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			50: {
				"ISO Month (4 Weeks)": "M13 (4w)",
				"ISO Month (4 + 5 + 4)": "Dec (4w)",
				"ISO Month (4 + 4 + 5)": "Dec (5w)",
				"ISO Quarter (13 Weeks)": "Q4",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			51: {
				"ISO Month (4 Weeks)": "M13 (4w)",
				"ISO Month (4 + 5 + 4)": "Dec (4w)",
				"ISO Month (4 + 4 + 5)": "Dec (5w)",
				"ISO Quarter (13 Weeks)": "Q4",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			52: {
				"ISO Month (4 Weeks)": "M13 (4w)",
				"ISO Month (4 + 5 + 4)": "Dec (4w)",
				"ISO Month (4 + 4 + 5)": "Dec (5w)",
				"ISO Quarter (13 Weeks)": "Q4",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
			53: {
				"ISO Month (4 Weeks)": "M13 (5w)",
				"ISO Month (4 + 5 + 4)": "Dec (5w)",
				"ISO Month (4 + 4 + 5)": "Dec (6w)",
				"ISO Quarter (13 Weeks)": "Q4",
				"ISO Semiannual (26 Weeks)": "HY2",
			},
		}

		# Entire period
		if periodicity == "Entire Period":
			# Returns format: "MM/DD/YY-MM/DD/YY"
			p = bins[0]
			return [f"{p[0].strftime('%m/%d/%y')}-{p[1].strftime('%m/%d/%y')}"]

		# ISO-based periodicity
		elif periodicity == "ISO Week":
			# Returns format: "Week N-YY"
			return [f"Week {iso_w}-{str(iso_y)[-2:]}" for iso_w, iso_y in iso_data]
		elif periodicity == "ISO Biweekly":
			# Returns format: "Weeks N-N YY"
			return [
				f"Weeks {p[0].isocalendar().week}-{p[1].isocalendar().week} {str(p[date_idx].isocalendar().year)[-2:]}"
				for p in bins
			]
		elif periodicity == "ISO Annual":
			# Returns format: "YYYY"
			return [f"{iso_y}" for iso_w, iso_y in iso_data]
		elif "ISO" in periodicity:
			# Returns format: "MMM (Nw)-YY", "QN-YY", or "HYN-YY" for month, quarter, or semiannual periodicity
			return [f"{iso_buckets[iso_w][periodicity]}-{str(iso_y)[-2:]}" for iso_w, iso_y in iso_data]

		# Fiscal Weeks
		elif periodicity == "Fiscal Weeks":
			# Returns format: "I (Nw)-YY"
			return [
				f"{i} ({int(((p[1] - p[0]).days + 1) / 7)}w)-{p[date_idx].strftime('%y')}"
				for i, p in enumerate(bins, start=1)
			]

		# Calendar-based periodicity
		elif periodicity in ["Calendar Month", "Monthly"]:
			# Returns format: "MMM-YY"
			return [p[date_idx].strftime("%b-%y") for p in bins]
		elif periodicity in ["Calendar Quarter", "Quarterly"]:
			# Returns format: "MM-YYQ"
			return [f"{p[date_idx].strftime('%m-%y')}Q" for p in bins]
		else:  # periodicity in ("Custom Days", "Weekly", "Biweekly", "Calendar Year", "Annually")
			# Returns format: "MM/DD/YY"
			return [p[date_idx].strftime("%m/%d/%y") for p in bins]

	def _get_iso_week_and_year(self, date: datetime.date) -> tuple[int, int]:
		"""
		Given a datetime.date object, returns the ISO week and ISO year.

		:param date: datetime.date object for which to get ISO data
		:return: (ISO week, ISO year) for given date
		"""
		iso_year, iso_week, _ = date.isocalendar()
		return iso_week, iso_year
