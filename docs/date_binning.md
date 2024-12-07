# Date Binning with the `Period` Class

The following code demonstrates various ways to use and apply the functionality in the `Period` class. In general, the class expects a date range defined with a `start_date` and `end_date`, and a `periodicity` (see options below). From there, it can generate date bins from `start_date` to `end_date` (inclusive by default) for the given `periodicity`. Date bins are in the form of a list of tuples, where each tuple contains that bin's start date and end date. The class can also convert given date bins from one periodicity to another, it can redistribute data from one periodicity to another given the data and original date bins, and can output pre-defined or custom labels.

The class supports the following options for `periodicity`. The ISO options follow the ISO-8601 Standard. If a `periodicity` isn't provided, the default is "ISO Week".

- "ISO Week" (default): weekly bins starting on a Monday
- "ISO Biweekly": bins of 2 ISO week periods, grouping weeks 01 and 02, then 03 with 04, etc.
- "ISO Month (4 Weeks)": monthly bins where months are defined by grouping ISO weeks within the ISO year in a pattern of 4 weeks each (this creates 13 months). Month 1 is weeks 01-04, month 2 is weeks 05-08, etc.
- "ISO Month (4 + 5 + 4)": monthly bins where months are defined by grouping ISO weeks within the ISO year in a pattern of 4 weeks, 5 weeks, then 4 weeks. Month 1 is weeks 01-04, month 2 is weeks 05-09, etc.
- "ISO Month (4 + 4 + 5)": monthly bins where months are defined by grouping ISO weeks within the ISO year in a pattern of 4 weeks, 4 weeks, then 5 weeks. Month 1 is weeks 01-04, month 2 is weeks 05-08, etc.
- "ISO Quarter (13 Weeks)": quarterly bins of 13 ISO week periods. Quarter 1 is weeks 01-13, quarter 2 is weeks 14-26, etc.
- "ISO Semiannual (26 Weeks)": semiannual bins of 26 ISO week periods. The first period is weeks 01-26 and second is weeks 27 to either 52 or 53, depending on the year
- "ISO Annual": bins of full ISO years. If `start_date` is not the first day of the ISO year, the first bin will be a partial year
- "Custom Days": bins starting on `start_date` with a number of days between them as given by `custom_days` parameter in `get_date_bins`
- "Weekly": weekly bins starting on `start_date`'s weekday
- "Biweekly": bins of 2-week periods, starting on `start_date`'s weekday
- "Calendar Month": bins by calendar month
- "Monthly": monthly bins starting on `start_date`
- "Calendar Quarter": bins of 3-month periods based on a calendar year (Jan-Mar, Apr-Jun, etc.)
- "Quarterly": bins of 3-month periods starting on `start_date`
- "Calendar Year": calendar year bins (Jan-Dec). If `start_date` is not Jan 1, the first bin will be a partial year
- "Annually": yearly bins starting from `start_date`
- "Entire Period": one bin spanning the given date range

## Partial ("Stub") Periods

The `Period` class respects the user-provided `start_date` and `end_date`, even if they don't respect the convention of the `periodicity`. For example, if the user wants bins by "Calendar Year", but the `start_date` they provide is not January 1st, then the first bin will be a stub year from `start_date` to December 31st.

For all ISO periodicity options, if `start_date` is not a Monday or week 01 of any other ISO period, the first bin will represent a stub period. For periodicity options of "Calendar Month" and "Calendar Year", if `start_date` is not the first of that year, the first bin will represent a partial month/year. For "Weekly", "Biweekly", "Calendar Quarter", and "Annually" options, there's no concept of a partial period - it starts binning with `start_date` and counts off bins from there.

Not all `periodicity` choices create stub periods. Any option with "ISO" or "Calendar" in the name will create stub periods, as they all have defined starting and ending points. The options for "Custom Days", "Weekly", "Biweekly", "Annually", and "Entire Period" don't create stub periods, as they start binning from the `start_date`, regardless of which day of the week/month/year it is.


```python
import datetime
from dateutil.relativedelta import relativedelta

from forecast import Period
```

## Using the `Period` Class


### Get Date Bins for ISO Week Periodicity

The following example creates date bins by ISO week for the current year. Since ISO years may have 52 or 53 weeks, the `n_weeks_in_cy` variable is used to get the week number for the final week of the year (December 28th is always in the last week of the ISO year).

The default `periodicity` for the `Period` class is "ISO Week", so it's not necessary to provide it.


```python
current_year = datetime.datetime.now().year
n_weeks_in_cy = datetime.date(current_year, 12, 28).isocalendar().week
start_date = datetime.date.fromisocalendar(current_year, 1, 1)
end_date = datetime.date.fromisocalendar(current_year, n_weeks_in_cy, 7)

# Create an instance of Period and generate the date bins
p = Period(start_date=start_date, end_date=end_date)
bins = p.get_date_bins()
bins
```




    [(datetime.date(2024, 1, 1), datetime.date(2024, 1, 7)),
     (datetime.date(2024, 1, 8), datetime.date(2024, 1, 14)),
     (datetime.date(2024, 1, 15), datetime.date(2024, 1, 21)),
     (datetime.date(2024, 1, 22), datetime.date(2024, 1, 28)),
     (datetime.date(2024, 1, 29), datetime.date(2024, 2, 4)),
     (datetime.date(2024, 2, 5), datetime.date(2024, 2, 11)),
     (datetime.date(2024, 2, 12), datetime.date(2024, 2, 18)),
     (datetime.date(2024, 2, 19), datetime.date(2024, 2, 25)),
     (datetime.date(2024, 2, 26), datetime.date(2024, 3, 3)),
     (datetime.date(2024, 3, 4), datetime.date(2024, 3, 10)),
     (datetime.date(2024, 3, 11), datetime.date(2024, 3, 17)),
     (datetime.date(2024, 3, 18), datetime.date(2024, 3, 24)),
     (datetime.date(2024, 3, 25), datetime.date(2024, 3, 31)),
     (datetime.date(2024, 4, 1), datetime.date(2024, 4, 7)),
     (datetime.date(2024, 4, 8), datetime.date(2024, 4, 14)),
     (datetime.date(2024, 4, 15), datetime.date(2024, 4, 21)),
     (datetime.date(2024, 4, 22), datetime.date(2024, 4, 28)),
     (datetime.date(2024, 4, 29), datetime.date(2024, 5, 5)),
     (datetime.date(2024, 5, 6), datetime.date(2024, 5, 12)),
     (datetime.date(2024, 5, 13), datetime.date(2024, 5, 19)),
     (datetime.date(2024, 5, 20), datetime.date(2024, 5, 26)),
     (datetime.date(2024, 5, 27), datetime.date(2024, 6, 2)),
     (datetime.date(2024, 6, 3), datetime.date(2024, 6, 9)),
     (datetime.date(2024, 6, 10), datetime.date(2024, 6, 16)),
     (datetime.date(2024, 6, 17), datetime.date(2024, 6, 23)),
     (datetime.date(2024, 6, 24), datetime.date(2024, 6, 30)),
     (datetime.date(2024, 7, 1), datetime.date(2024, 7, 7)),
     (datetime.date(2024, 7, 8), datetime.date(2024, 7, 14)),
     (datetime.date(2024, 7, 15), datetime.date(2024, 7, 21)),
     (datetime.date(2024, 7, 22), datetime.date(2024, 7, 28)),
     (datetime.date(2024, 7, 29), datetime.date(2024, 8, 4)),
     (datetime.date(2024, 8, 5), datetime.date(2024, 8, 11)),
     (datetime.date(2024, 8, 12), datetime.date(2024, 8, 18)),
     (datetime.date(2024, 8, 19), datetime.date(2024, 8, 25)),
     (datetime.date(2024, 8, 26), datetime.date(2024, 9, 1)),
     (datetime.date(2024, 9, 2), datetime.date(2024, 9, 8)),
     (datetime.date(2024, 9, 9), datetime.date(2024, 9, 15)),
     (datetime.date(2024, 9, 16), datetime.date(2024, 9, 22)),
     (datetime.date(2024, 9, 23), datetime.date(2024, 9, 29)),
     (datetime.date(2024, 9, 30), datetime.date(2024, 10, 6)),
     (datetime.date(2024, 10, 7), datetime.date(2024, 10, 13)),
     (datetime.date(2024, 10, 14), datetime.date(2024, 10, 20)),
     (datetime.date(2024, 10, 21), datetime.date(2024, 10, 27)),
     (datetime.date(2024, 10, 28), datetime.date(2024, 11, 3)),
     (datetime.date(2024, 11, 4), datetime.date(2024, 11, 10)),
     (datetime.date(2024, 11, 11), datetime.date(2024, 11, 17)),
     (datetime.date(2024, 11, 18), datetime.date(2024, 11, 24)),
     (datetime.date(2024, 11, 25), datetime.date(2024, 12, 1)),
     (datetime.date(2024, 12, 2), datetime.date(2024, 12, 8)),
     (datetime.date(2024, 12, 9), datetime.date(2024, 12, 15)),
     (datetime.date(2024, 12, 16), datetime.date(2024, 12, 22)),
     (datetime.date(2024, 12, 23), datetime.date(2024, 12, 29))]



If `start_date` is not a Monday, or `end_date` is not a Sunday, the first or last bin will be a stub period, respectively. The following example uses a Wednesday (weekday 3) in week 01 as `start_date` and a Friday (weekday 5) in week 04 as an `end_date`. The resulting first and last bins are partial weeks to respect the user's date range. The middle 2 bins are full ISO weeks starting on Monday.


```python
start_date = datetime.date.fromisocalendar(current_year, 1, 3)
end_date = datetime.date.fromisocalendar(current_year, 4, 5)

# Create an instance of Period and generate the date bins
p = Period(start_date=start_date, end_date=end_date)
bins = p.get_date_bins()
bins
```




    [(datetime.date(2024, 1, 3), datetime.date(2024, 1, 7)),
     (datetime.date(2024, 1, 8), datetime.date(2024, 1, 14)),
     (datetime.date(2024, 1, 15), datetime.date(2024, 1, 21)),
     (datetime.date(2024, 1, 22), datetime.date(2024, 1, 26))]



### Get Labels for Date Bins

The `Period` class has the `get_period_labels` method to generate labels for given date bins. It has built-in formats for all periodicity options, or the user can provide their own format string to suit their needs. The method supports any Python [strftime formatters](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes), which uses the 1989 C standard.

If a custom format is provided, the user can also indicate which date for each bin - the bin's start date or the bin's end date - to use to create the labels. The built-in formats use the bin's start date for ISO-based periodicity options and the bin's end date for the others, with the exception of the "Entire Period" periodicity, which uses both dates.


```python
# Get default-formatted labels
p.get_period_labels(bins, periodicity="ISO Week")
```




    ['Week 1-24', 'Week 2-24', 'Week 3-24', 'Week 4-24']




```python
# Get custom-formatted labels of form MMM-DD using the end date of each bin
p.get_period_labels(
    bins,
    periodicity="ISO Week",
    date_format_string="%b-%d",
    use_bin_start_date_for_label=False
)
```




    ['Jan-07', 'Jan-14', 'Jan-21', 'Jan-26']



### Convert Date Bins from One Periodicity to Another

The following example converts bins from "ISO Week" to "ISO Quarter (13 Weeks)".


```python
start_date = datetime.date.fromisocalendar(current_year, 1, 1)
end_date = datetime.date.fromisocalendar(current_year, n_weeks_in_cy, 7)

# Create an instance of Period and generate the date bins
p = Period(start_date=start_date, end_date=end_date)
iso_week_bins = p.get_date_bins()

# Convert ISO Week bins to ISO Quarter (13 Weeks) bins
iso_q_bins = p.convert_dates(iso_week_bins, "ISO Quarter (13 Weeks)")
iso_q_bins
```




    [(datetime.date(2024, 1, 1), datetime.date(2024, 3, 31)),
     (datetime.date(2024, 4, 1), datetime.date(2024, 6, 30)),
     (datetime.date(2024, 7, 1), datetime.date(2024, 9, 29)),
     (datetime.date(2024, 9, 30), datetime.date(2024, 12, 29))]




```python
p.get_period_labels(iso_q_bins, "ISO Quarter (13 Weeks)")
```




    ['Q1-24', 'Q2-24', 'Q3-24', 'Q4-24']



### Redistribute Data from One Bin to Another

Given numerical data and date bins of the same length, the `Period` class's `redistribute_data` method can convert the date bins and "re-bin" the numerical data values. Note that it assumes the data are distributed evenly across the days in their respective bins before they are redistributed to the new bins.

The resulting object has the new date bins as keys and the redistributed data as values.


```python
data = [100] * 13 + [200] * 13 + [300] * 13 + [100] * 13
data = data + ([100] if n_weeks_in_cy == 53 else [])

# Convert ISO Week data to ISO Quarter data
q_data = p.redistribute_data(data, iso_week_bins, "ISO Quarter (13 Weeks)")
q_data
```




    OrderedDict([((datetime.date(2024, 1, 1), datetime.date(2024, 3, 31)),
                  Decimal('1299.999999999999999999999995')),
                 ((datetime.date(2024, 4, 1), datetime.date(2024, 6, 30)),
                  Decimal('2600.000000000000000000000025')),
                 ((datetime.date(2024, 7, 1), datetime.date(2024, 9, 29)),
                  Decimal('3900.000000000000000000000010')),
                 ((datetime.date(2024, 9, 30), datetime.date(2024, 12, 29)),
                  Decimal('1299.999999999999999999999995'))])



## ISO Periodicity Date Bin Examples

The following examples illustrate the other ISO-based periodicity options for creating date bins. All examples use a `start_date` that is the last week of the prior ISO year and an `end_date` in the first week of the following ISO year. This is to show that the binning applies patterns of including specific ISO weeks in a defined "month", "quarter", half year, etc.

### ISO Biweekly

Note that the first bin is only 1 week, since it's a stub period of the last biweekly period in the prior ISO year, followed by 2-week bins that group ISO weeks 1 and 2, then 3 and 4, and so forth. The final bin is also a 1 week long stub period since the `end_date` splits that biweekly period.


```python
# `start_date` is the last week of the prior ISO year
start_date = datetime.date.fromisocalendar(current_year, 1, 1) - relativedelta(days=7)

# `end_date` is the first week of the following ISO year
end_date = datetime.date.fromisocalendar(current_year, n_weeks_in_cy, 7) + relativedelta(days=7)
print(f"Start Date: {start_date}, End Date: {end_date}")
```

    Start Date: 2023-12-25, End Date: 2025-01-05



```python
p = Period(start_date=start_date, end_date=end_date, periodicity="ISO Biweekly")
bins = p.get_date_bins()
bins
```




    [(datetime.date(2023, 12, 25), datetime.date(2023, 12, 31)),
     (datetime.date(2024, 1, 1), datetime.date(2024, 1, 14)),
     (datetime.date(2024, 1, 15), datetime.date(2024, 1, 28)),
     (datetime.date(2024, 1, 29), datetime.date(2024, 2, 11)),
     (datetime.date(2024, 2, 12), datetime.date(2024, 2, 25)),
     (datetime.date(2024, 2, 26), datetime.date(2024, 3, 10)),
     (datetime.date(2024, 3, 11), datetime.date(2024, 3, 24)),
     (datetime.date(2024, 3, 25), datetime.date(2024, 4, 7)),
     (datetime.date(2024, 4, 8), datetime.date(2024, 4, 21)),
     (datetime.date(2024, 4, 22), datetime.date(2024, 5, 5)),
     (datetime.date(2024, 5, 6), datetime.date(2024, 5, 19)),
     (datetime.date(2024, 5, 20), datetime.date(2024, 6, 2)),
     (datetime.date(2024, 6, 3), datetime.date(2024, 6, 16)),
     (datetime.date(2024, 6, 17), datetime.date(2024, 6, 30)),
     (datetime.date(2024, 7, 1), datetime.date(2024, 7, 14)),
     (datetime.date(2024, 7, 15), datetime.date(2024, 7, 28)),
     (datetime.date(2024, 7, 29), datetime.date(2024, 8, 11)),
     (datetime.date(2024, 8, 12), datetime.date(2024, 8, 25)),
     (datetime.date(2024, 8, 26), datetime.date(2024, 9, 8)),
     (datetime.date(2024, 9, 9), datetime.date(2024, 9, 22)),
     (datetime.date(2024, 9, 23), datetime.date(2024, 10, 6)),
     (datetime.date(2024, 10, 7), datetime.date(2024, 10, 20)),
     (datetime.date(2024, 10, 21), datetime.date(2024, 11, 3)),
     (datetime.date(2024, 11, 4), datetime.date(2024, 11, 17)),
     (datetime.date(2024, 11, 18), datetime.date(2024, 12, 1)),
     (datetime.date(2024, 12, 2), datetime.date(2024, 12, 15)),
     (datetime.date(2024, 12, 16), datetime.date(2024, 12, 29)),
     (datetime.date(2024, 12, 30), datetime.date(2025, 1, 5))]




```python
# Get default-formatted labels for date bins
p.get_period_labels(bins, "ISO Biweekly")
```




    ['Weeks 52-52 23',
     'Weeks 1-2 24',
     'Weeks 3-4 24',
     'Weeks 5-6 24',
     'Weeks 7-8 24',
     'Weeks 9-10 24',
     'Weeks 11-12 24',
     'Weeks 13-14 24',
     'Weeks 15-16 24',
     'Weeks 17-18 24',
     'Weeks 19-20 24',
     'Weeks 21-22 24',
     'Weeks 23-24 24',
     'Weeks 25-26 24',
     'Weeks 27-28 24',
     'Weeks 29-30 24',
     'Weeks 31-32 24',
     'Weeks 33-34 24',
     'Weeks 35-36 24',
     'Weeks 37-38 24',
     'Weeks 39-40 24',
     'Weeks 41-42 24',
     'Weeks 43-44 24',
     'Weeks 45-46 24',
     'Weeks 47-48 24',
     'Weeks 49-50 24',
     'Weeks 51-52 24',
     'Weeks 1-1 25']



### ISO Month (4 Weeks)

This periodicity defines months as equal, 4-ISO week periods for a total of 13 months. The default labels use "M13" for the final month's name. In the event the ISO year has 53 weeks, the final week is included in the last month.


```python
p = Period(start_date=start_date, end_date=end_date, periodicity="ISO Month (4 Weeks)")
bins = p.get_date_bins()
bins
```




    [(datetime.date(2023, 12, 25), datetime.date(2023, 12, 31)),
     (datetime.date(2024, 1, 1), datetime.date(2024, 1, 28)),
     (datetime.date(2024, 1, 29), datetime.date(2024, 2, 25)),
     (datetime.date(2024, 2, 26), datetime.date(2024, 3, 24)),
     (datetime.date(2024, 3, 25), datetime.date(2024, 4, 21)),
     (datetime.date(2024, 4, 22), datetime.date(2024, 5, 19)),
     (datetime.date(2024, 5, 20), datetime.date(2024, 6, 16)),
     (datetime.date(2024, 6, 17), datetime.date(2024, 7, 14)),
     (datetime.date(2024, 7, 15), datetime.date(2024, 8, 11)),
     (datetime.date(2024, 8, 12), datetime.date(2024, 9, 8)),
     (datetime.date(2024, 9, 9), datetime.date(2024, 10, 6)),
     (datetime.date(2024, 10, 7), datetime.date(2024, 11, 3)),
     (datetime.date(2024, 11, 4), datetime.date(2024, 12, 1)),
     (datetime.date(2024, 12, 2), datetime.date(2024, 12, 29)),
     (datetime.date(2024, 12, 30), datetime.date(2025, 1, 5))]




```python
# Get default-formatted labels for date bins
p.get_period_labels(bins, "ISO Month (4 Weeks)")
```




    ['M13 (4w)-23',
     'Jan (4w)-24',
     'Feb (4w)-24',
     'Mar (4w)-24',
     'Apr (4w)-24',
     'May (4w)-24',
     'Jun (4w)-24',
     'Jul (4w)-24',
     'Aug (4w)-24',
     'Sep (4w)-24',
     'Oct (4w)-24',
     'Nov (4w)-24',
     'Dec (4w)-24',
     'M13 (4w)-24',
     'Jan (4w)-25']



### ISO Month (4 + 5 + 4)

This periodicity defines months as grouped ISO weeks in the pattern of 4 weeks, 5 weeks, then 4 weeks, with the first month including ISO weeks 01-04 and so forth. In the event the ISO year has 53 weeks, the final week is included in the last month.


```python
p = Period(start_date=start_date, end_date=end_date, periodicity="ISO Month (4 + 5 + 4)")
bins = p.get_date_bins()
bins
```




    [(datetime.date(2023, 12, 25), datetime.date(2023, 12, 31)),
     (datetime.date(2024, 1, 1), datetime.date(2024, 1, 28)),
     (datetime.date(2024, 1, 29), datetime.date(2024, 3, 3)),
     (datetime.date(2024, 3, 4), datetime.date(2024, 3, 31)),
     (datetime.date(2024, 4, 1), datetime.date(2024, 4, 28)),
     (datetime.date(2024, 4, 29), datetime.date(2024, 6, 2)),
     (datetime.date(2024, 6, 3), datetime.date(2024, 6, 30)),
     (datetime.date(2024, 7, 1), datetime.date(2024, 7, 28)),
     (datetime.date(2024, 7, 29), datetime.date(2024, 9, 1)),
     (datetime.date(2024, 9, 2), datetime.date(2024, 9, 29)),
     (datetime.date(2024, 9, 30), datetime.date(2024, 10, 27)),
     (datetime.date(2024, 10, 28), datetime.date(2024, 12, 1)),
     (datetime.date(2024, 12, 2), datetime.date(2024, 12, 29)),
     (datetime.date(2024, 12, 30), datetime.date(2025, 1, 5))]




```python
# Get default-formatted labels for date bins
p.get_period_labels(bins, "ISO Month (4 + 5 + 4)")
```




    ['Dec (4w)-23',
     'Jan (4w)-24',
     'Feb (5w)-24',
     'Mar (4w)-24',
     'Apr (4w)-24',
     'May (5w)-24',
     'Jun (4w)-24',
     'Jul (4w)-24',
     'Aug (5w)-24',
     'Sep (4w)-24',
     'Oct (4w)-24',
     'Nov (5w)-24',
     'Dec (4w)-24',
     'Jan (4w)-25']



### ISO Month (4 + 4 + 5)

This periodicity defines months as grouped ISO weeks in the pattern of 4 weeks, 4 weeks, then 5 weeks, with the first month including ISO weeks 01-04 and so forth. In the event the ISO year has 53 weeks, the final week is included in the last month.


```python
p = Period(start_date=start_date, end_date=end_date, periodicity="ISO Month (4 + 4 + 5)")
bins = p.get_date_bins()
bins
```




    [(datetime.date(2023, 12, 25), datetime.date(2023, 12, 31)),
     (datetime.date(2024, 1, 1), datetime.date(2024, 1, 28)),
     (datetime.date(2024, 1, 29), datetime.date(2024, 2, 25)),
     (datetime.date(2024, 2, 26), datetime.date(2024, 3, 31)),
     (datetime.date(2024, 4, 1), datetime.date(2024, 4, 28)),
     (datetime.date(2024, 4, 29), datetime.date(2024, 5, 26)),
     (datetime.date(2024, 5, 27), datetime.date(2024, 6, 30)),
     (datetime.date(2024, 7, 1), datetime.date(2024, 7, 28)),
     (datetime.date(2024, 7, 29), datetime.date(2024, 8, 25)),
     (datetime.date(2024, 8, 26), datetime.date(2024, 9, 29)),
     (datetime.date(2024, 9, 30), datetime.date(2024, 10, 27)),
     (datetime.date(2024, 10, 28), datetime.date(2024, 11, 24)),
     (datetime.date(2024, 11, 25), datetime.date(2024, 12, 29)),
     (datetime.date(2024, 12, 30), datetime.date(2025, 1, 5))]




```python
# Get default-formatted labels for date bins
p.get_period_labels(bins, "ISO Month (4 + 4 + 5)")
```




    ['Dec (5w)-23',
     'Jan (4w)-24',
     'Feb (4w)-24',
     'Mar (5w)-24',
     'Apr (4w)-24',
     'May (4w)-24',
     'Jun (5w)-24',
     'Jul (4w)-24',
     'Aug (4w)-24',
     'Sep (5w)-24',
     'Oct (4w)-24',
     'Nov (4w)-24',
     'Dec (5w)-24',
     'Jan (4w)-25']



### ISO Quarter (13 Weeks)

This periodicity defines quarters as grouped ISO weeks in the pattern of 13 weeks each, with the first quarter including ISO weeks 01-13 and so forth. In the event the ISO year has 53 weeks, the final week is included in the last quarter.


```python
p = Period(start_date=start_date, end_date=end_date, periodicity="ISO Quarter (13 Weeks)")
bins = p.get_date_bins()
bins
```




    [(datetime.date(2023, 12, 25), datetime.date(2023, 12, 31)),
     (datetime.date(2024, 1, 1), datetime.date(2024, 3, 31)),
     (datetime.date(2024, 4, 1), datetime.date(2024, 6, 30)),
     (datetime.date(2024, 7, 1), datetime.date(2024, 9, 29)),
     (datetime.date(2024, 9, 30), datetime.date(2024, 12, 29)),
     (datetime.date(2024, 12, 30), datetime.date(2025, 1, 5))]




```python
# Get default-formatted labels for date bins
p.get_period_labels(bins, "ISO Quarter (13 Weeks)")
```




    ['Q4-23', 'Q1-24', 'Q2-24', 'Q3-24', 'Q4-24', 'Q1-25']



### ISO Semiannual (26 Weeks)

This periodicity defines a semi-annual period as grouped ISO weeks in the pattern of 26 weeks each, with the first half-year including ISO weeks 01-26 and the second half-year including weeks 27-52. In the event the ISO year has 53 weeks, the final week is included in the second half-year.


```python
p = Period(start_date=start_date, end_date=end_date, periodicity="ISO Semiannual (26 Weeks)")
bins = p.get_date_bins()
bins
```




    [(datetime.date(2023, 12, 25), datetime.date(2023, 12, 31)),
     (datetime.date(2024, 1, 1), datetime.date(2024, 6, 30)),
     (datetime.date(2024, 7, 1), datetime.date(2024, 12, 29)),
     (datetime.date(2024, 12, 30), datetime.date(2025, 1, 5))]




```python
# Get default-formatted labels for date bins
p.get_period_labels(bins, "ISO Semiannual (26 Weeks)")
```




    ['HY2-23', 'HY1-24', 'HY2-24', 'HY1-25']



### ISO Annual

This periodicity returns bins by ISO year.


```python
p = Period(start_date=start_date, end_date=end_date, periodicity="ISO Annual")
bins = p.get_date_bins()
bins
```




    [(datetime.date(2023, 12, 25), datetime.date(2023, 12, 31)),
     (datetime.date(2024, 1, 1), datetime.date(2024, 12, 29)),
     (datetime.date(2024, 12, 30), datetime.date(2025, 1, 5))]




```python
# Get default-formatted labels for date bins
p.get_period_labels(bins, "ISO Annual")
```




    ['2023', '2024', '2025']



## Calendar and Other Periodicity Date Bin Examples

The following examples illustrate the calendar-based and other periodicity options for creating date bins.

### Custom Days

The most flexible of the periodicity options, this one creates bins starting on `start_date` with a number of days between them as given by the additional `custom_days` parameter.


```python
start_date = datetime.datetime.now().date()
end_date = start_date + relativedelta(days=30)

p = Period(start_date=start_date, end_date=end_date, periodicity="Custom Days")
bins = p.get_date_bins(custom_days=5)
bins
```




    [(datetime.date(2024, 12, 7), datetime.date(2024, 12, 11)),
     (datetime.date(2024, 12, 12), datetime.date(2024, 12, 16)),
     (datetime.date(2024, 12, 17), datetime.date(2024, 12, 21)),
     (datetime.date(2024, 12, 22), datetime.date(2024, 12, 26)),
     (datetime.date(2024, 12, 27), datetime.date(2024, 12, 31)),
     (datetime.date(2025, 1, 1), datetime.date(2025, 1, 5)),
     (datetime.date(2025, 1, 6), datetime.date(2025, 1, 6))]




```python
p.get_period_labels(bins, "Custom Days")
```




    ['12/11/24',
     '12/16/24',
     '12/21/24',
     '12/26/24',
     '12/31/24',
     '01/05/25',
     '01/06/25']



### Weekly

This periodicity option creates weekly bins based on `start_date`'s weekday.


```python
start_date = datetime.date(current_year, 1, 15)
end_date = start_date + relativedelta(days=41)

p = Period(start_date=start_date, end_date=end_date, periodicity="Weekly")
bins = p.get_date_bins()
bins
```




    [(datetime.date(2024, 1, 15), datetime.date(2024, 1, 21)),
     (datetime.date(2024, 1, 22), datetime.date(2024, 1, 28)),
     (datetime.date(2024, 1, 29), datetime.date(2024, 2, 4)),
     (datetime.date(2024, 2, 5), datetime.date(2024, 2, 11)),
     (datetime.date(2024, 2, 12), datetime.date(2024, 2, 18)),
     (datetime.date(2024, 2, 19), datetime.date(2024, 2, 25))]




```python
p.get_period_labels(bins, "Weekly")
```




    ['01/21/24', '01/28/24', '02/04/24', '02/11/24', '02/18/24', '02/25/24']



### Biweekly

This periodicity option creates bins with lengths of 2 weeks starting from `start_date`.


```python
p = Period(start_date=start_date, end_date=end_date, periodicity="Biweekly")
bins = p.get_date_bins()
bins
```




    [(datetime.date(2024, 1, 15), datetime.date(2024, 1, 28)),
     (datetime.date(2024, 1, 29), datetime.date(2024, 2, 11)),
     (datetime.date(2024, 2, 12), datetime.date(2024, 2, 25))]




```python
p.get_period_labels(bins, "Biweekly")
```




    ['01/28/24', '02/11/24', '02/25/24']



### Calendar Month

This periodicity option creates calendar-month bins. If `start_date` doesn't fall on the first of the month, the first bin will be a stub period.


```python
start_date = datetime.date(current_year, 1, 15)
end_date = datetime.date(current_year, 6, 14)

p = Period(start_date=start_date, end_date=end_date, periodicity="Calendar Month")
bins = p.get_date_bins()
bins
```




    [(datetime.date(2024, 1, 15), datetime.date(2024, 1, 31)),
     (datetime.date(2024, 2, 1), datetime.date(2024, 2, 29)),
     (datetime.date(2024, 3, 1), datetime.date(2024, 3, 31)),
     (datetime.date(2024, 4, 1), datetime.date(2024, 4, 30)),
     (datetime.date(2024, 5, 1), datetime.date(2024, 5, 31)),
     (datetime.date(2024, 6, 1), datetime.date(2024, 6, 14))]




```python
p.get_period_labels(bins, "Calendar Month")
```




    ['Jan-24', 'Feb-24', 'Mar-24', 'Apr-24', 'May-24', 'Jun-24']



### Monthly

This periodicity option creates monthly bins starting from `start_date`.


```python
start_date = datetime.date(current_year, 1, 15)
end_date = datetime.date(current_year, 6, 14)

p = Period(start_date=start_date, end_date=end_date, periodicity="Monthly")
bins = p.get_date_bins()
bins
```




    [(datetime.date(2024, 1, 15), datetime.date(2024, 2, 14)),
     (datetime.date(2024, 2, 15), datetime.date(2024, 3, 14)),
     (datetime.date(2024, 3, 15), datetime.date(2024, 4, 14)),
     (datetime.date(2024, 4, 15), datetime.date(2024, 5, 14)),
     (datetime.date(2024, 5, 15), datetime.date(2024, 6, 14))]




```python
p.get_period_labels(bins, "Monthly")
```




    ['Feb-24', 'Mar-24', 'Apr-24', 'May-24', 'Jun-24']



### Calendar Quarter

This periodicity option creates quarterly bins (periods of 3 months) based on the calendar year. Quarter 1 is Jan-Mar, Q2 is Apr-Jun, Q3 is Jul-Sep, and Q4 is Oct-Dec. If `start_date` doesn't fall at the beginning of the quarter, the first bin will be a stub period.


```python
start_date = datetime.date(current_year, 1, 15)
end_date = datetime.date(current_year + 1, 3, 31)

p = Period(start_date=start_date, end_date=end_date, periodicity="Calendar Quarter")
bins = p.get_date_bins()
bins
```




    [(datetime.date(2024, 1, 15), datetime.date(2024, 3, 31)),
     (datetime.date(2024, 4, 1), datetime.date(2024, 6, 30)),
     (datetime.date(2024, 7, 1), datetime.date(2024, 9, 30)),
     (datetime.date(2024, 10, 1), datetime.date(2024, 12, 31)),
     (datetime.date(2025, 1, 1), datetime.date(2025, 3, 31))]




```python
p.get_period_labels(bins, "Calendar Quarter")
```




    ['03-24Q', '06-24Q', '09-24Q', '12-24Q', '03-25Q']



### Quarterly

This periodicity option creates quarterly bins (periods of 3 months) starting from `start_date`.


```python
start_date = datetime.date(current_year, 11, 15)
end_date = datetime.date(current_year + 1, 11, 14)

p = Period(start_date=start_date, end_date=end_date, periodicity="Quarterly")
bins = p.get_date_bins()
bins
```




    [(datetime.date(2024, 11, 15), datetime.date(2025, 2, 14)),
     (datetime.date(2025, 2, 15), datetime.date(2025, 5, 14)),
     (datetime.date(2025, 5, 15), datetime.date(2025, 8, 14)),
     (datetime.date(2025, 8, 15), datetime.date(2025, 11, 14))]




```python
p.get_period_labels(bins, "Quarterly")
```




    ['02-25Q', '05-25Q', '08-25Q', '11-25Q']



### Calendar Year

This periodicity option creates calendar year bins from Jan-Dec. If `start_date` doesn't fall at the beginning of the year, the first bin will be a stub period.


```python
start_date = datetime.date(current_year, 1, 15)
end_date = datetime.date(current_year + 2, 12, 31)

p = Period(start_date=start_date, end_date=end_date, periodicity="Calendar Year")
bins = p.get_date_bins()
bins
```




    [(datetime.date(2024, 1, 15), datetime.date(2024, 12, 31)),
     (datetime.date(2025, 1, 1), datetime.date(2025, 12, 31)),
     (datetime.date(2026, 1, 1), datetime.date(2026, 12, 31))]




```python
p.get_period_labels(bins, "Calendar Year")
```




    ['12/31/24', '12/31/25', '12/31/26']



### Annually

This periodicity option creates yearly bins starting from `start_date`.


```python
start_date = datetime.date(current_year, 7, 15)
end_date = datetime.date(current_year + 2, 7, 14)

p = Period(start_date=start_date, end_date=end_date, periodicity="Annually")
bins = p.get_date_bins()
bins
```




    [(datetime.date(2024, 7, 15), datetime.date(2025, 7, 14)),
     (datetime.date(2025, 7, 15), datetime.date(2026, 7, 14))]




```python
p.get_period_labels(bins, "Annually")
```




    ['07/14/25', '07/14/26']


