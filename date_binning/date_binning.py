from collections import OrderedDict
from contextvars import ContextVar
import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from itertools import pairwise, cycle, accumulate


weekday_start = ContextVar('weekday_start', default=1)


class Period:
    def __init__(self, start_date=None, end_date=None, periodicity=None):
        self.start_date = start_date
        self.end_date = end_date
        self.periodicity = periodicity


    def get_iso_start_dates(self, start_date, end_date, step):
        """
        Returns a list of datetime.date objects representing the starting date of
            all ISO periods falling within the time span defined by `start_date` to
            `end_date`. If `start_date` is not a Monday (the starting weekday for
            an ISO week), then the first bin will begin with a partial week
            (`start_date` to Sunday). All following bins will consist of full
            periods.
        
        :param start_date: datetime.date object; the date to start binning from
        :param end_date: datetime.date object; the date to end binning
        :param step: tuple of str, int or sequence of ints; the string indicates
            the portion of the date that is changing via step (this function assumes
            "weeks"), and the integer or sequence of integers is the step for period
            dates generated within the time span. If `step` is a sequence, it will
            cycle continuously over the values to get the current step to collect
            the start dates of the periods.
            Example: ISO Month (4 + 5 + 4) would use (4, 5, 4) as the `step`, so
            the returned sequence of dates represent months that are 4 ISO weeks,
            then 5 ISO weeks, then 4 ISO weeks, with that pattern continuing through
            to the `end_date`
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
            start_date = (datetime.date.fromisocalendar(start_date.isocalendar().year, start_date.isocalendar().week, 1)
                          + relativedelta(weeks=next(seq)))
        
        while start_date < end_date:
            r.append(start_date) 
            start_date += relativedelta(weeks=next(seq))
        
        return r
    

    def get_iso_annual_start_dates(self, start_date, end_date, step):
        """
        Returns a list of datetime.date objects representing the starting date of
            all ISO years falling within the time span defined by `start_date` to
            `end_date`. If `start_date` is not the first day of that ISO year, the
            returned sequence will begin with a "stub" period (an incomplete year).
            The second date in the returned sequence will be the first day of the
            first full ISO year after `start_date`.
        
        :param start_date: datetime.date object; the date to start binning from
        :param end_date: datetime.date object; the date to end binning
        :param step: tuple of str, int; the string indicates the portion of the date
            that is changing via step, and the integer is the step
        :return: list of datetime.date objects
        """
        period, delta = step
        r = []        
        iso_yr_start_date = datetime.date.fromisocalendar(start_date.year, 1, 1)
        
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
        Returns a list of datetime.date objects representing the starting date of
            all calendar-based periods falling within the time span defined by
            `start_date` to `end_date`. The step tuple is determined by periodicity
            
            
            If `start_date` is not a Monday (the starting weekday for
            an ISO week), then the returned sequence will begin with a "stub" period
            (an incomplete week). The second date in the returned sequence will be
            the first Monday after `start_date`, and all following dates are Mondays.
        
        :param start_date: datetime.date object; the date to start binning from
        :param end_date: datetime.date object; the date to end binning
        :param step: tuple of str, int; the string indicates the portion of the date
            that is changing via step, and the integer is the step
        :return: list of datetime.date objects        
        """
        period, delta = step
        r = []

        if period == "weeks":
            # Check if start_date is first day of period, if not, reset it to prior period start then add step
            if start_date.isoweekday() != weekday_start.get():
                r.append(start_date)
                backstep = weekday_start.get() - start_date.isoweekday() if start_date.isoweekday() > weekday_start.get() else weekday_start.get() - start_date.isoweekday() - 7
                start_date += relativedelta(days=backstep) + relativedelta(weeks=delta)

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
            #TODO: Use contextvars to set FY (which will allow stub periods)?
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
        Accepts a sequence of period start dates and adds the period
            end date for each item, which is the day prior to the next
            start date in the sequence. Assumes the final date is the
            (exclusive) end date for the entire sequence.

        :param start_dates: sequence of datetime.date objects
        :return: list of tuples of datetime.date objects; each tuple 
            represents the start and end dates of end-to-end periods
        """
        # Generate (from, to) period pairs off start dates
        return [(p[0], p[1] + relativedelta(days=-1)) for p in pairwise(start_dates)]
    

    def get_dates(self, start_date=None, end_date=None, periodicity=None, inclusive=False):
        """
        Gets the starting dates for all periods falling within the time span
            from `start_date` to `end_date`, then returns a list of tuples
            with the start and end dates for each period.
        
        :param start_date: datetime.date object; the date to start binning from
        :param end_date: datetime.date object; the date to end binning
        :param periodicity: str or None; how to determine the periods within the
            time span from `start_date` to `end_date`. If None, assumes "ISO Week".
            Options (for all ISO periods, if `start_date` is not a Monday, the
            first bin will include a partial week (`start_date` to Sunday), with
            following bins generated with full ISO weeks):
            - "ISO Week": weekly bins starting on a Monday
            - "Weekly": weekly bins where the starting weekday is determined by
              `start_date`
            - "ISO Biweekly": bins of 2 ISO week periods
            - "Biweekly": bins of 2 week periods, starting on `start_date`'s weekday
            - "ISO Month (4 Weeks)": monthly bins of 4 ISO week periods
            - "ISO Month (4 + 5 + 4)": monthly bins of ISO week periods following a
              pattern where the first month is 4 ISO weeks long, the next is 5 ISO
              weeks long, the next is 4 ISO weeks long, repeating until `end_date`
            - "ISO Month (4 + 4 + 5)": monthly bins of ISO week periods following a
              pattern where the first month is 4 ISO weeks long, the next is 4 ISO
              weeks long, the next is 5 ISO weeks long, repeating until `end_date`
            - "Calendar Month": monthly bins by calendar. If `start_date` is not the
              first of the month, the first bin will be a partial month
            - "ISO Quarter (13 Weeks)": quarterly bins of 13 ISO week periods
            - "Calendar Quarter": bins of 3 calendar month periods. If `start_date`
              is not the first of the month, the first month of the first bin will
              be a partial month
            - "ISO Semiannual (26 Weeks)": semiannual bins of 26 ISO week periods
            - "ISO Annual": bins of full ISO years. If `start_date` is not the first
              day of the ISO year, the first bin will be a partial year
            - "Calendar Year": calendar year bins (Jan-Dec). If `start_date`
              is not Jan 1, the first bin will be a partial year
            - "Annually": yearly bins starting from `start_date`
            - "Entire Period": one bin from `start_date` to either `end_date` (if
              inclusive=True) or the day prior to `end_date` (if inclusive=False)
        :param inclusive: bool; if the time span being binned includes the end_date
            (inclsive=True) or ends the day before (inclusive=False).
        :return: list of tuples in form `(datetime.date object, datetime.date object)`
        """
        start_date = self.start_date if not start_date else start_date
        end_date = self.end_date if not end_date else end_date
        
        if (start_date is None or type(start_date) != datetime.date):
            raise ValueError("Please provide a valid start date.")

        if (end_date is None or type(end_date) != datetime.date):
            raise ValueError("Please provide a valid end date.")
        
        if end_date <= start_date:
            raise ValueError("End date must be after start date.")

        effective_end_date = end_date if not inclusive else end_date + relativedelta(days=1)
        periodicity = self.periodicity if not periodicity else periodicity
        is_iso = 'iso' in periodicity.lower() if periodicity is not None else True
        
        steps = {
            "ISO Week": ("weeks", 1),
            "ISO Biweekly": ("weeks", 2),
            "ISO Month (4 Weeks)": ("weeks", 4),
            "ISO Month (4 + 5 + 4)": ("weeks", (4, 5, 4)),
            "ISO Month (4 + 4 + 5)": ("weeks", (4, 4, 5)),
            "ISO Quarter (13 Weeks)": ("weeks", 13), 
            "ISO Semiannual (26 Weeks)": ("weeks", 26),
            "ISO Annual": ("years", 1),  # edge case (years can be 52 or 53 weeks)
            "Weekly": ("weeks", 1),
            "Biweekly": ("weeks", 2),
            "Calendar Month": ("months", 1),
            "Calendar Quarter": ("months", 3),
            "Calendar Year": ("years-cy", 1),  # assumes Jan-Dec year (accommodates partial years on front or back end)
            "Annually": ("years", 1),  # assumes 1 year from date given (accommodates non-calendar FYs)            
        }
        
        if periodicity == "Entire Period":
            return [(start_date, effective_end_date)]
        
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
    

    def convert_dates(self, bins, periodicity):
        """
        Converts date bins from their original periodicity into bins for new
            given `periodicity` over the same time span.
        
        :param bins: list of tuples in form `(datetime.date object,
            datetime.date object)`
        :param periodicity: str or None; how to determine the periods within the
            time span from `start_date` to `end_date`. If None, assumes "ISO Week"
        :return: list of tuples in form `(datetime.date object, datetime.date object)`
        """
        if not bins:
            return []
        start_date = bins[0][0]
        end_date = bins[-1][-1]
        return self.get_dates(start_date=start_date,
                              end_date=end_date,
                              periodicity=periodicity,
                              inclusive=True)


    def redistribute_data(self, data, bins, periodicity=None):
        """
        Redistributes financial `data` for the periods specified by `bins`
            into new date periods based on `periodicity`. Returns an OrderedDict
            where the keys are the new period bins and the values are
            the redistributed financial data. Assumes financials are uniformly
            distributed over the days within the original periods.
        
        :param data: sequence of financial data points
        :param bins: list of tuples in form `(datetime.date object,
            datetime.date object)`; must be of same length as data since it
            represents the date periods of the financials
        :param periodicity: str or None; how to determine the periods within the
            same time span as `bins`. If None, assumes "ISO Week"
        :return: OrderedDict; the keys are the date bins for the new periodicity,
            the values are the redistributed financials
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

        # Rebuild financials by summing over data by day using cumulative indices as breakpoints
        new_data = [sum(d_per_day[i[0]:i[1]]) for i in pairwise(indices)]

        return OrderedDict(zip(new_bins, new_data))
    

    def period_labels(self, periodicity):
        month_names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        if periodicity in ('ISO Week', 'Weekly', None):
            return [p.strftime("%m/%d/%Y") for p in self.get_dates(periodicity=periodicity)]
        if periodicity == "ISO Month (4 + 5 + 4)":
            start_month = self.start_date.month + 1 % 12
            month_sizes = ["4","5","4","4","5","4","4","5","4","4","5","4"]
            month_names = month_names[start_month:] + month_names[:start_month]
            return month_names
        elif periodicity == 'Calendar Month':
            # TODO: get start month, cycle over month names as needed
            return month_names
        elif periodicity == "ISO Quarter (13 Weeks)":
            # get quarter 
            return ['Q1', 'Q2', 'Q3', 'Q4']  # TODO: what if Q's are back end of their year and don't start at Q1? Use "Q-mm/dd/yy"?
        elif periodicity == 'Entire Period':
            return [self.start_date.strftime("%m/%d/%Y")]
